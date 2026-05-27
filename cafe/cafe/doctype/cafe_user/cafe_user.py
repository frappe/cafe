# Copyright (c) 2026, Frappe and contributors
# For license information, please see license.txt

import re

import frappe
from frappe.model.document import Document


class CafeUser(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from cafe.cafe.doctype.cafe_user_experience.cafe_user_experience import (
			CafeUserExperience,
		)
		from frappe.types import DF

		bio: DF.SmallText | None
		company: DF.Data | None
		designation: DF.Data | None
		education: DF.Table[CafeUserExperience]
		handle: DF.Data
		introduction: DF.SmallText | None
		user: DF.Link
		work_history: DF.Table[CafeUserExperience]
	# end: auto-generated types

	def validate(self):
		# self.validate_permission()
		if self.handle:
			self.handle = self.handle.lower()
		self.validate_handle()

	def validate_handle(self):
		if not self.handle:
			return

		if re.search(r"[^a-z0-9_-]", self.handle):
			frappe.throw(
				"Handle can only contain lowercase letters, numbers, hyphens, and underscores"
			)

		if len(self.handle) < 3:
			frappe.throw("Handle must be at least 3 characters long")

		if len(self.handle) > 30:
			frappe.throw("Handle must be at most 30 characters long")

		handle_exists = frappe.db.exists("Cafe User", {"handle": self.handle})
		if handle_exists:
			frappe.throw(
				f"Handle '{self.handle}' is already taken. Please choose a different one."
			)

	def validate_permission(self):
		if not frappe.session.user:
			frappe.throw("You must be logged in to perform this action")

		frappe_roles = frappe.get_roles(frappe.session.user)

		if "System Manager" in frappe_roles:
			return True

		if frappe.session.user != self.user:
			frappe.throw("You can only edit your own profile")

		return True
