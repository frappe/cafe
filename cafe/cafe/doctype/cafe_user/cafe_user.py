# Copyright (c) 2026, Frappe and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class CafeUser(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from cafe.cafe.doctype.cafe_user_experience.cafe_user_experience import CafeUserExperience
		from frappe.types import DF

		company: DF.Data | None
		designation: DF.Data | None
		education: DF.Table[CafeUserExperience]
		user: DF.Link
		username: DF.Data
		work_history: DF.Table[CafeUserExperience]
	# end: auto-generated types

	pass
