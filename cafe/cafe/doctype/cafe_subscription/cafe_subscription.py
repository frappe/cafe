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
		filters = {"owner": frappe.session.user}
		count_filters = {}

		if self.publication:
			filters["publication"] = self.publication
			count_filters["publication"] = self.publication
		elif self.user:
			filters["user"] = self.user
			count_filters["user"] = self.user
		else:
			frappe.throw("Either a publication or user is required to subscribe")

		existing = frappe.db.get_value("Cafe Subscription", filters, "name")

		if existing:
			frappe.delete_doc("Cafe Subscription", existing, ignore_permissions=True)
			subscriber_count = frappe.db.count("Cafe Subscription", count_filters)
			return {"subscribed_by_me": False, "subscriber_count": subscriber_count}

		self.owner = frappe.session.user
		doc = super().insert(*args, **kwargs)
		subscriber_count = frappe.db.count("Cafe Subscription", count_filters)
		return {
			**doc.as_dict(),
			"subscribed_by_me": True,
			"subscriber_count": subscriber_count,
		}
