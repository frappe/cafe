# Copyright (c) 2026, Frappe and contributors
# For license information, please see license.txt

from datetime import datetime

import frappe
from frappe.model.document import Document


class CafeUserExperience(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		description: DF.Data | None
		experience_type: DF.Literal["Work", "Education"]
		from_month: DF.Literal["", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
		from_year: DF.Int
		is_current: DF.Check
		organization: DF.Data
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		title: DF.Data
		to_month: DF.Literal["", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
		to_year: DF.Int
	# end: auto-generated types

	def validate(self):
		self.validate_years()

	def validate_years(self):
		min_year = 1900
		max_year = datetime.now().year

		if self.from_year and (self.from_year < min_year or self.from_year > max_year):
			frappe.throw(
				frappe._("From Year must be between {0} and {1}").format(
					min_year, max_year
				)
			)

		if self.to_year and (self.to_year < min_year or self.to_year > max_year):
			frappe.throw(
				frappe._("To Year must be between {0} and {1}").format(
					min_year, max_year
				)
			)
