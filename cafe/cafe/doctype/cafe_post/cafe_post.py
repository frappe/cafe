# Copyright (c) 2026, Frappe and contributors
# For license information, please see license.txt

import re

import frappe
from frappe.model.document import Document
from frappe.query_builder.functions import Count
from frappe.utils import pretty_date, strip_html


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
		cover_image: DF.AttachImage | None
		description: DF.SmallText
		publication: DF.Link | None
		published: DF.Check
		reading_time: DF.Data | None
		slug: DF.Data | None
		tags: DF.TableMultiSelect[CafePostTagItem]
		title: DF.Data
	# end: auto-generated types

	def before_save(self):
		if self.content:
			self.reading_time = self.calculate_reading_time()

		if not self.slug:
			self.slug = self.generate_slug()

	def generate_slug(self) -> str:
		slug = self.title.lower()
		slug = re.sub(r"[^a-z0-9\s-]", "", slug)
		slug = re.sub(r"\s+", "-", slug).strip("-")
		slug = slug[:50].rstrip("-")

		return f"{slug}-{self.name}"

	def calculate_reading_time(self) -> str:
		WORDS_PER_MINUTE = 250

		text = strip_html(self.content or "")

		word_count = len(text.split())
		minutes = max(1, round(word_count / WORDS_PER_MINUTE))

		return f"{minutes} min read"


@frappe.whitelist(allow_guest=True)
def get_post_comments(post_id: str, start: int = 0, limit: int = 10):
	"""Get paginated comments for a post with user info and likes."""
	Comment = frappe.qb.DocType("Cafe Post Comment")
	CafeUser = frappe.qb.DocType("Cafe User")
	User = frappe.qb.DocType("User")

	comments = (
		frappe.qb.from_(Comment)
		.left_join(CafeUser)
		.on(Comment.owner == CafeUser.user)
		.left_join(User)
		.on(Comment.owner == User.name)
		.select(
			Comment.name,
			Comment.content,
			Comment.owner,
			Comment.creation,
			User.full_name,
			User.user_image,
			CafeUser.handle,
		)
		.where(Comment.post == post_id)
		.orderby(Comment.creation, order=frappe.qb.desc)
		.limit(limit)
		.offset(start)
		.run(as_dict=True)
	)

	if not comments:
		return []

	# Get likes count for comments
	comment_names = [c.name for c in comments]
	Like = frappe.qb.DocType("Cafe Social Like")
	likes_query = (
		frappe.qb.from_(Like)
		.select(Like.comment, Count(Like.name).as_("count"))
		.where(Like.comment.isin(comment_names))
		.groupby(Like.comment)
	)
	likes_result = likes_query.run(as_dict=True)
	likes_map = {row.comment: row.count for row in likes_result}

	for comment in comments:
		comment.likes = likes_map.get(comment.name, 0)
		comment.time_ago = pretty_date(comment.creation)
		comment.author_url = (
			f"/cafe/profile/{comment.handle}"
			if comment.handle
			else f"/cafe/profile/{comment.owner}"
		)
		comment.liked_by_me = bool(
			frappe.db.exists(
				"Cafe Social Like",
				{"comment": comment.name, "owner": frappe.session.user},
			)
		)

	return comments
