# Copyright (c) 2026, Frappe and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class CafeSocialLike(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		comment: DF.Link | None
		post: DF.Link | None
	# end: auto-generated types

	def insert(self, *args, **kwargs):
		user = frappe.session.user

		existing_like = None
		if self.post:
			existing_like = frappe.db.get_value(
				"Cafe Social Like", {"post": self.post, "owner": user}, "name"
			)
		elif self.comment:
			existing_like = frappe.db.get_value(
				"Cafe Social Like", {"comment": self.comment, "owner": user}, "name"
			)

		if existing_like:
			frappe.delete_doc(
				"Cafe Social Like", existing_like, ignore_permissions=True
			)
			if self.post:
				like_count = frappe.db.count("Cafe Social Like", {"post": self.post})
			elif self.comment:
				like_count = frappe.db.count(
					"Cafe Social Like", {"comment": self.comment}
				)
			else:
				like_count = 0

			return {"liked_by_me": False, "like_count": like_count}

		result = super().insert(*args, **kwargs).as_dict()

		if self.post:
			like_count = frappe.db.count("Cafe Social Like", {"post": self.post})
		elif self.comment:
			like_count = frappe.db.count("Cafe Social Like", {"comment": self.comment})
		else:
			like_count = 0

		return {**result, "liked_by_me": True, "like_count": like_count}
