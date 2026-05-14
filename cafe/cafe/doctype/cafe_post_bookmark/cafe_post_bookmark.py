# Copyright (c) 2026, Frappe and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class CafePostBookmark(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		post: DF.Link
	# end: auto-generated types

	def insert(self, *args, **kwargs):
		existing = frappe.db.get_value(
			"Cafe Post Bookmark",
			{"post": self.post, "owner": frappe.session.user},
			"name",
		)

		if existing:
			frappe.delete_doc("Cafe Post Bookmark", existing, ignore_permissions=True)
			return {"bookmarked_by_me": False}

		return {**super().insert(*args, **kwargs).as_dict(), "bookmarked_by_me": True}
