// Copyright (c) 2026, Frappe and contributors
// For license information, please see license.txt

frappe.ui.form.on("Cafe Post Tag", {
	refresh(frm) {
		if (frm.doc.is_standard && !frappe.boot.developer_mode) {
			frm.disable_form();
		}
	},
});
