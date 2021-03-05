// Copyright (c) 2021, Mohammad Hussain Nagaria and contributors
// For license information, please see license.txt

frappe.ui.form.on('COA Importer', {
	onload: function(frm) {
		frm.set_value("import_file", "");
	},
	refresh: function(frm) {
		frm.disable_save();
		create_import_button(frm);
	 }
});

var create_import_button = function(frm) {
	frm.page.set_primary_action(
		__("Import"), function() {
			frappe.call({
				method: "accounting_app.accounting_app.doctype.coa_importer.coa_importer.import_coa", 
				args: {
					filename: frm.doc.import_file
				},
				freeze: true,
				callback: function(r) {console.log(r);}
			});
		}
	);
};


