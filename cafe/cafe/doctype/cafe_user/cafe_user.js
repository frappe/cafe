// Copyright (c) 2026, Frappe and contributors
// For license information, please see license.txt

frappe.ui.form.on("Cafe User Experience", {
	work_history_add(frm, cdt, cdn) {
		frm.fields_dict.work_history.grid.update_docfield_property("experience_type", "options", [
			"Work",
		]);
		frappe.model.set_value(cdt, cdn, "experience_type", "Work");
	},

	education_add(frm, cdt, cdn) {
		frm.fields_dict.education.grid.update_docfield_property("experience_type", "options", [
			"Education",
		]);
		frappe.model.set_value(cdt, cdn, "experience_type", "Education");
	},

	from_year(frm, cdt, cdn) {
		validateYear(frm, cdt, cdn, "from_year");
	},

	to_year(frm, cdt, cdn) {
		validateYear(frm, cdt, cdn, "to_year");
	},
});

function validateYear(frm, cdt, cdn, fieldname) {
	const year = locals[cdt][cdn][fieldname];
	if (!year) return;

	const currentYear = new Date().getFullYear();
	if (year < 1900 || year > currentYear) {
		frappe.msgprint({
			title: __("Invalid Year"),
			message: __(`Year must be between 1900 and ${currentYear + 1}`),
			indicator: "red",
		});
		frappe.model.set_value(cdt, cdn, fieldname, null);
	}
}
