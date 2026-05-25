import frappe
from frappe import _
from frappe.auth import LoginAttemptTracker
from frappe.core.doctype.user.user import test_password_strength
from frappe.rate_limiter import rate_limit
from frappe.utils.password import check_password, update_password


@frappe.whitelist()
@rate_limit(limit=5, seconds=300)  # 5 attempts per 5 minutes per user/IP
def change_password(old_password: str, new_password: str):
	"""
	Change password for the current logged-in user.
	Uses Frappe's LoginAttemptTracker for attempt counting/lockout, and rate_limit for API abuse protection.
	"""
	user = frappe.session.user
	if user == "Guest":
		frappe.throw(
			_("You must be logged in to change your password"),
			frappe.AuthenticationError,
		)

	tracker = LoginAttemptTracker(user)
	if not tracker.is_user_allowed():
		frappe.throw(_("Too many failed attempts. Please try again after some time."))

	if old_password == new_password:
		frappe.throw(
			_(
				"New password cannot be the same as current password. Please choose a different password."
			)
		)

	try:
		check_password(user, old_password)
	except frappe.AuthenticationError:
		tracker.add_failure_attempt()
		frappe.throw(_("Incorrect current password. Please try again."))
	else:
		tracker.add_success_attempt()

	result = test_password_strength(new_password)
	feedback = result.get("feedback", {})
	if not feedback.get("password_policy_validation_passed", False):
		suggestions = feedback.get("suggestions", [])
		frappe.throw(
			_("Password is too weak. {0}").format(
				" ".join(suggestions) if suggestions else ""
			)
		)

	update_password(user=user, pwd=new_password, logout_all_sessions=False)
	return _("Password Updated Successfully")
