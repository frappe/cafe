# Copyright (c) 2026, Frappe and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class CafeUserExperience(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		description: DF.Data | None
		experience_type: DF.Literal["Work", "Education"]
		from_month: DF.Literal[None]
		from_year: DF.Literal[None]
		is_current: DF.Check
		organization: DF.Data
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		title: DF.Data
		to_month: DF.Literal[None]
		to_year: DF.Literal[None]
	# end: auto-generated types

	pass
