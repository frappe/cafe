# Copyright (c) 2026, Frappe and contributors
# For license information, please see license.txt

import re

import frappe
from frappe.model.document import Document
from frappe.query_builder.functions import Count
from frappe.utils import pretty_date, strip_html
from frappe.utils.data import cstr


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

	def validate(self):
		if self.title:
			# Strip HTML comments syntax
			self.title = re.sub(r"<!--|-->", "", self.title).strip()
			if len(self.title) > 60:
				frappe.throw(
					frappe._(
						"Title cannot exceed 60 characters. Current length: {0}"
					).format(len(self.title))
				)

		if self.description:
			# Strip HTML comments syntax
			self.description = re.sub(r"<!--|-->", "", self.description).strip()
			if len(self.description) > 250:
				frappe.throw(
					frappe._(
						"Description cannot exceed 250 characters. Current length: {0}"
					).format(len(self.description))
				)

	def before_save(self):
		if self.content:
			self.reading_time = self.calculate_reading_time()

		if not self.slug:
			self.slug = self.generate_slug()

	def on_update(self):
		before = self.get_doc_before_save()
		if not (before and before.published) and self.published:
			frappe.enqueue(
				"cafe.cafe.doctype.cafe_post.cafe_post.notify_subscribers",
				post_name=self.name,
			)

	def on_trash(self):
		# Delete bookmarks, replies and its likes before deleting the post
		comments = frappe.get_all(
			"Cafe Post Comment",
			filters={"post": self.name},
			fields=["name", "comment"],
		)

		like_or_filters = [["post", "=", self.name]]
		if comments:
			like_or_filters.append(["comment", "in", [c.name for c in comments]])
		likes = frappe.get_all(
			"Cafe Social Like", or_filters=like_or_filters, pluck="name"
		)
		for like in likes:
			frappe.delete_doc("Cafe Social Like", like, ignore_permissions=True)

		for comment in sorted(comments, key=lambda c: not c.comment):
			frappe.delete_doc(
				"Cafe Post Comment", comment.name, ignore_permissions=True
			)

		for bookmark in frappe.get_all(
			"Cafe Post Bookmark", filters={"post": self.name}, pluck="name"
		):
			frappe.delete_doc("Cafe Post Bookmark", bookmark, ignore_permissions=True)

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


def notify_subscribers(post_name: str):
	post = frappe.get_doc("Cafe Post", post_name)

	recipients = set()

	cafe_user = frappe.db.get_value(
		"Cafe User", {"user": post.owner}, ["name", "handle"], as_dict=True
	)
	if cafe_user:
		author_subs = frappe.get_all(
			"Cafe Subscription",
			filters={"user": cafe_user.name},
			pluck="owner",
		)
		recipients.update(author_subs)

	recipients.discard(post.owner)

	if not recipients:
		return

	site_url = frappe.utils.get_url()
	post_url = f"{site_url}/cafe/posts/{post.slug}"

	author_name = frappe.db.get_value("User", post.owner, "full_name") or post.owner
	author_handle = cafe_user.handle if cafe_user else None
	author_profile_url = (
		f"{site_url}/cafe/profile/{author_handle}"
		if author_handle
		else f"{site_url}/cafe/profile/{post.owner}"
	)

	tags = [t.tag for t in post.tags] if post.tags else []

	frappe.sendmail(
		recipients=list(recipients),
		subject=f"{post.title}",
		template="new_post_notification",
		args={
			"title": post.title,
			"description": post.description,
			"cover_image": post.cover_image,
			"post_url": post_url,
			"author_name": author_name,
			"author_handle": f"@{author_handle}" if author_handle else None,
			"author_profile_url": author_profile_url,
			"reading_time": post.reading_time,
			"publication": post.publication,
			"tags": tags,
			"site_name": cstr(frappe.local.site_name),
		},
		header=["New post on Cafe", "orange"],
	)


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
