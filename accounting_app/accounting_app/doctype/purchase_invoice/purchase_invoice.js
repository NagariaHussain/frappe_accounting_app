// Copyright (c) 2021, Mohammad Hussain Nagaria and contributors
// For license information, please see license.txt

frappe.ui.form.on('Purchase Invoice', {
	refresh: (doc) => {
		if (!doc.paid) {
			this.frm.add_custom_button(
				__('Payment'), 
				(frm) => { 
					return frappe.call({
						method: "accounting_app.accounting_app.doctype.payment_entry.payment_entry.get_payment_entry",
						args: {
							dt: this.frm.doc.doctype,
							dn: this.frm.doc.name
						},
						callback: function(r) {
							var doc = frappe.model.sync(r.message);
							frappe.set_route("Form", doc[0].doctype, doc[0].name);
						}
					});
				}, 
				__('Create')
			);
		} else {
			console.log("Paid");
		}
	}
});

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
