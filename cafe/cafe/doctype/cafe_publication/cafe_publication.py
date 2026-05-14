# Copyright (c) 2026, Frappe and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class CafePublication(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from cafe.cafe.doctype.cafe_publication_member.cafe_publication_member import CafePublicationMember
		from frappe.types import DF

		description: DF.Data | None
		handle: DF.Data
		image: DF.AttachImage | None
		members: DF.Table[CafePublicationMember]
		title: DF.Data
	# end: auto-generated types

	pass
