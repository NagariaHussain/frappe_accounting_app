frappe.provide("frappe.treeview_settings")

frappe.treeview_settings["Account"] = {
    breadcrumb: "Accounts",
    title: __("Chart of Accounts"),
    onload: function(treeview) {
        treeview.page.add_inner_button(__("Import using JSON"), function() {
            frappe.set_route("coa-importer", "COA Importer");
        });
    }
};