# Copyright (c) 2026, Frappe and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class CafePostTag(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		is_standard: DF.Check
		title: DF.Data
	# end: auto-generated types

	def validate(self):
		self.check_standard()

	def on_trash(self):
		self.check_standard()

	def check_standard(self):
		if (
			frappe.conf.developer_mode
			or frappe.flags.in_migrate
			or frappe.flags.in_install
			or frappe.flags.in_import
		):
			return

		if self.is_standard:
			frappe.throw(
				_("Standard tags can only be created or modified in Developer Mode.")
			)

		if not self.is_new():
			old_doc = self.get_doc_before_save()
			if old_doc and old_doc.is_standard:
				frappe.throw(_("Standard tags cannot be edited or deleted."))
