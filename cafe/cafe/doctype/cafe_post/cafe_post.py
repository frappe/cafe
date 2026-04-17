# Copyright (c) 2026, Frappe and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class CafePost(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from cafe.cafe.doctype.cafe_post_tag_item.cafe_post_tag_item import (
			CafePostTagItem,
		)
		from frappe.types import DF

		content: DF.TextEditor
		publication: DF.Link | None
		tags: DF.TableMultiSelect[CafePostTagItem]
	# end: auto-generated types

	pass
