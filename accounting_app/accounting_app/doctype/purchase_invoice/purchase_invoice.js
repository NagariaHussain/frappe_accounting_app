// Copyright (c) 2021, Mohammad Hussain Nagaria and contributors
// For license information, please see license.txt

frappe.ui.form.on('Purchase Invoice Item', {
	qty(frm, cdt, cdn) {
		update_amount(cdt, cdn);
	},
	rate(frm, cdt, cdn) {
		update_amount(cdt, cdn);
	}
});

function update_amount(cdt, cdn) {
	let item = frappe.get_doc(cdt, cdn);
	item.amount = item.qty * item.rate;
}
