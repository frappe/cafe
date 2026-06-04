# Copyright (c) 2026, Frappe and contributors
# For license information, please see license.txt

import re

import frappe
from frappe.model.document import Document


class CafeUser(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from cafe.cafe.doctype.cafe_user_experience.cafe_user_experience import (
			CafeUserExperience,
		)
		from frappe.types import DF

		bio: DF.SmallText | None
		company: DF.Data | None
		designation: DF.Data | None
		education: DF.Table[CafeUserExperience]
		handle: DF.Data
		introduction: DF.SmallText | None
		user: DF.Link
		work_history: DF.Table[CafeUserExperience]
	# end: auto-generated types

	def on_trash(self):
		self.delete_owned_content()

	def delete_owned_content(self):
		for post in frappe.get_all(
			"Cafe Post", filters={"owner": self.user}, pluck="name"
		):
			frappe.delete_doc("Cafe Post", post, ignore_permissions=True)

		for comment in frappe.get_all(
			"Cafe Post Comment", filters={"owner": self.user}, pluck="name"
		):
			frappe.delete_doc("Cafe Post Comment", comment, ignore_permissions=True)

		for like in frappe.get_all(
			"Cafe Social Like", filters={"owner": self.user}, pluck="name"
		):
			frappe.delete_doc("Cafe Social Like", like, ignore_permissions=True)

		for bookmark in frappe.get_all(
			"Cafe Post Bookmark", filters={"owner": self.user}, pluck="name"
		):
			frappe.delete_doc("Cafe Post Bookmark", bookmark, ignore_permissions=True)

		for subscription in frappe.get_all(
			"Cafe Subscription", filters={"user": self.name}, pluck="name"
		):
			frappe.delete_doc(
				"Cafe Subscription", subscription, ignore_permissions=True
			)

		member_rows = frappe.get_all(
			"Cafe Publication Member",
			filters={"user": self.name},
			fields=["parent"],
		)
		for publication in {row.parent for row in member_rows}:
			doc = frappe.get_doc("Cafe Publication", publication)
			doc.members = [m for m in doc.members if m.user != self.name]
			doc.save(ignore_permissions=True)

	def validate(self):
		# self.validate_permission()
		if self.handle:
			self.handle = self.handle.lower()

		self.validate_handle()

		if self.bio and len(self.bio) > 165:
			frappe.throw("Bio cannot exceed 165 characters")
		if self.introduction and len(self.introduction) > 500:
			frappe.throw("Introduction cannot exceed 500 characters")

	def validate_handle(self):
		if not self.handle or not self.has_value_changed("handle"):
			return

		if re.search(r"[^a-z0-9_-]", self.handle):
			frappe.throw(
				"Handle can only contain lowercase letters, numbers, hyphens, and underscores"
			)

		if len(self.handle) < 3:
			frappe.throw("Handle must be at least 3 characters long")

		handle_exists = frappe.db.get_value(
			"Cafe User", {"handle": self.handle}, "name"
		)
		if handle_exists:
			frappe.throw(
				f"Handle '{self.handle}' is already taken. Please choose a different one."
			)

	def validate_permission(self):
		if not frappe.session.user:
			frappe.throw("You must be logged in to perform this action")

		frappe_roles = frappe.get_roles(frappe.session.user)

		if "System Manager" in frappe_roles:
			return True

		if frappe.session.user != self.user:
			frappe.throw("You can only edit your own profile")

		return True
