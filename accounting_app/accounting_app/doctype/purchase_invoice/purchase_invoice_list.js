frappe.listview_settings['Purchase Invoice'] = {
    get_indicator: function(doc) {
        if (doc.paid) {
            return [__("Paid"), "green"];
        } else {
            return [__("Unpaid"), "darkgrey"];
        }
    }
};