# Copyright (c) 2013, Mohammad Hussain Nagaria and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import functools
import re
from past.builtins import cmp

def execute(filters=None):
	columns, data = [], []
	return columns, data

def get_accounts(root_type):
	return frappe.db.sql("""
	select name, account_number, parent_account, lft, rgt, root_type, report_type, account_name, account_type, is_group, lft, rgt
	from tabAccount
	where root_type=%s order by lft""", (root_type), as_dict=True)

def filter_accounts(accounts, depth=20):
	parent_children_map = {}
	accounts_by_name = {}
	for d in accounts:
		accounts_by_name[d.name] = d
		parent_children_map.setdefault(d.parent_account or None, []).append(d)

	filtered_accounts = []

	def add_to_list(parent, level):
		if level < depth:
			children = parent_children_map.get(parent) or []
			sort_accounts(children, is_root=True if parent==None else False)

			for child in children:
				child.indent = level
				filtered_accounts.append(child)
				add_to_list(child.name, level + 1)

	add_to_list(None, 0)

	return filtered_accounts, accounts_by_name, parent_children_map
	
def sort_accounts(accounts, is_root=False, key="name"):
	def compare_accounts(a, b):
		if re.split('\W+', a[key])[0].isdigit():
			# if chart of accounts is numbered, then sort by number
			return cmp(a[key], b[key])
		elif is_root:
			if a.report_type != b.report_type and a.report_type == "Balance Sheet":
				return -1
			if a.root_type != b.root_type and a.root_type == "Asset":
				return -1
			if a.root_type == "Liability" and b.root_type == "Equity":
				return -1
			if a.root_type == "Income" and b.root_type == "Expense":
				return -1
		else:
			# sort by key (number) or name
			return cmp(a[key], b[key])
		return 1

	accounts.sort(key = functools.cmp_to_key(compare_accounts))