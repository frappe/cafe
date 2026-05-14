# Copyright (c) 2026, Frappe and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class CafePostComment(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		comment: DF.Link | None
		content: DF.Text
		post: DF.Link | None
	# end: auto-generated types

	def on_trash(self):
		likes = frappe.get_all(
			"Cafe Social Like", filters={"comment": self.name}, pluck="name"
		)
		for like in likes:
			frappe.delete_doc("Cafe Social Like", like, ignore_permissions=True)
