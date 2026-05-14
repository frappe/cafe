# Copyright (c) 2026, Frappe and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class CafeSubscription(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		publication: DF.Link | None
		user: DF.Link | None
	# end: auto-generated types

	def insert(self, *args, **kwargs):
		existing = frappe.db.get_value(
			"Cafe Subscription",
			{"publication": self.publication, "user": frappe.session.user},
			"name",
		)

		if existing:
			frappe.delete_doc("Cafe Subscription", existing, ignore_permissions=True)
			return {"subscribed_by_me": False}

		return {**super().insert(*args, **kwargs).as_dict(), "subscribed_by_me": True}
