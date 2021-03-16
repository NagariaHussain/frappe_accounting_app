frappe.listview_settings['Purchase Invoice'] = {
    get_indicator: function(doc) {
        if (doc.status == "Paid") {
            console.log(doc, "is paid");
            return [__("Paid"), "green"];
        } 
        else if (doc.status == "Unpaid") 
        {
            console.log("not paid");
            return [__("Unpaid"), "darkgrey"];
        }
    }
};