# Copyright (c) 2013, Mohammad Hussain Nagaria and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns, data = [], []
	return columns, data

def get_accounts(root_type):
	return frappe.db.sql("""
	select name, account_number, parent_account, lft, rgt, root_type, report_type, account_name, account_type, is_group, lft, rgt
	from tabAccount
	where root_type=%s order by lft""", (root_type), as_dict=True)
