# -*- coding: utf-8 -*-
# Copyright (c) 2021, Mohammad Hussain Nagaria and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

@frappe.whitelist()
def import_coa(filename):
    # Get the doc having the given filename
    file_doc = frappe.get_doc("File", {"file_url": filename})
    
    # Extract name and extension
    name, extension = file_doc.get_extension()
    
    # If not a json file
    if extension != ".json":
        frappe.throw("Please upload a JSON file.")

class COAImporter(Document):
	pass
