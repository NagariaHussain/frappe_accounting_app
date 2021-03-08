# -*- coding: utf-8 -*-
# Copyright (c) 2021, Mohammad Hussain Nagaria and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import json
from unidecode import unidecode
from six import iteritems
from frappe.utils import cstr
from frappe.model.document import Document
from frappe.utils.nestedset import rebuild_tree

@frappe.whitelist()
def import_coa(filename):
    # Get the doc having the given filename
    file_doc = frappe.get_doc("File", {"file_url": filename})
    
    # Extract name and extension
    name, extension = file_doc.get_extension()
    
    # If not a json file
    if extension != ".json":
        frappe.throw("Please upload a JSON file.")

    # Get path to file
    file_path = file_doc.get_full_path()

    # Load and validate JSON data
    with open(file_path, 'r') as json_file:
        try:
            data = json.load(json_file)
        except json.decoder.JSONDecodeError as e:
            frappe.throw("Invalid JSON content.")

    # Create and insert COA
    create_charts(data)
    
def create_charts(custom_chart):
    accounts = []

    # Recursive charts of accounts importer
    def _import_accounts(children, parent, root_type, root_account=False):
        for account_name, child in iteritems(children):
            if root_account:
                root_type = child.get("root_type")
            
            single_account_attributes = ["account_number", "account_type",
               "root_type", "is_group", "tax_rate"]

            if account_name not in single_account_attributes:
                account_number = cstr(child.get("account_number")).strip()   
                account_name, account_name_in_db = add_suffix_if_duplicate(
                                                    account_name, 
                                                    account_number, 
                                                    accounts
                                                    )
                is_group = identify_is_group(child)
                report_type = "Balance Sheet" if root_type in ["Asset", "Liability", "Equity"] \
                    else "Profit and Loss"
                
                account = frappe.get_doc({
						"doctype": "Account",
						"account_name": account_name,
						"parent_account": parent,
						"is_group": is_group,
						"root_type": root_type,
						"report_type": report_type,
						"account_number": account_number,
						"account_type": child.get("account_type"),
					})

                account.flags.ignore_mandatory = True
                account.flags.ignore_permissions = True
                account.insert()
                accounts.append(account_name_in_db)
                _import_accounts(child, account.name, root_type)
    
    # Rebuild NestedSet tree for Account DocType
    # after all accounts have been inserted.
    frappe.local.flags.ignore_on_update = True
    _import_accounts(custom_chart, None, None, root_account=True)
    rebuild_tree("Account", "parent_account")
    frappe.local.flags.ignore_on_update = False

def add_suffix_if_duplicate(account_name, account_number, accounts):
    '''Adds a suffix (count sequence) to the account name 
       if the given name already exists'''
    if account_number:
        account_name_in_db = unidecode(" - ".join(
            (account_number,
            account_name.strip().lower())
        ))
    else:
        account_name_in_db = unidecode(account_name.strip().lower())
    
    if account_name_in_db in accounts:
        count = accounts.count(account_name_in_db)
        account_name = account_name + " " + cstr(count)
    
    return account_name, account_name_in_db

def identify_is_group(child):
    '''return 1 if child is a group account else 0'''
    if child.get("is_group"):
        is_group = child.get("is_group")
    elif len(
        set(child.keys()) - set(("account_type", "root_type", "is_group", "tax_rate", "account_number"))
        ):
        is_group = 1
    else:
        is_group = 0

    return is_group

class COAImporter(Document):
	pass
