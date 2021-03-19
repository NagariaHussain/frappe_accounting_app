from __future__ import unicode_literals

import functools
import re

import frappe
from frappe.utils import flt, getdate
from past.builtins import cmp
from six import itervalues


def get_data(root_type, balance_must_be, from_date, to_date, total = True):
	accounts = get_accounts(root_type)

	if not accounts:
		return None

	accounts, accounts_by_name = filter_accounts(accounts)

	gl_entries_by_account = {}
	for root in frappe.db.sql("""select lft, rgt from tabAccount
			where root_type=%s and ifnull(parent_account, '') = ''""", root_type, as_dict=1):

		set_gl_entries_by_account(
			gl_entries_by_account,
			from_date,
			to_date,
			root.lft, root.rgt)
	
	calculate_values(
		accounts_by_name, gl_entries_by_account, to_date)
	
	accumulate_values_into_parents(accounts, accounts_by_name)

	out = prepare_data(accounts, balance_must_be, from_date, to_date)

	if out and total:
		add_total_row(out, root_type, balance_must_be)

	return out

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

	return filtered_accounts, accounts_by_name

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

def set_gl_entries_by_account(gl_entries_by_account, from_date, to_date, root_lft, root_rgt):
	"""Returns a dict like { "account": [gl entries], ... }"""
	accounts = frappe.db.sql_list("""select name from `tabAccount`
		where lft >= %s and rgt <= %s""", (root_lft, root_rgt))
	
	additional_conditions = ""

	if accounts:
		additional_conditions += "account in ({})"\
			.format(", ".join([frappe.db.escape(d) for d in accounts]))

	sql_statement = """select posting_date, account, debit, credit from `tabLedger Entry`
						where {additional_conditions}
						and posting_date between '{from_date}' and '{to_date}'
						order by account, posting_date""".format(
			additional_conditions=additional_conditions, to_date=to_date, from_date=from_date
		)

	gl_entries = frappe.db.sql(sql_statement, as_dict=True) 
	
	for entry in gl_entries:
			gl_entries_by_account.setdefault(entry.account, []).append(entry)

	return gl_entries_by_account

def calculate_values(accounts_by_name, gl_entries_by_account, to_date):
	for entries in itervalues(gl_entries_by_account):
		for entry in entries:
			d = accounts_by_name.get(entry.account)
			if not d:
				frappe.msgprint(
					frappe._("Could not retrieve information for {0}.").format(entry.account), title="Error",
					raise_exception=1
				)

			if entry.posting_date < getdate(to_date):
				d["opening_balance"] = d.get("opening_balance", 0.0) + flt(entry.debit) - flt(entry.credit)

def accumulate_values_into_parents(accounts, accounts_by_name):
	"""accumulate children's values in parent accounts"""
	for d in reversed(accounts):
		if d.parent_account:
			accounts_by_name[d.parent_account]["opening_balance"] = \
				accounts_by_name[d.parent_account].get("opening_balance", 0.0) + d.get("opening_balance", 0.0)

def prepare_data(accounts, balance_must_be, from_date, to_date):
	data = []
	year_start_date = from_date
	year_end_date = to_date

	for d in accounts:
		# add to output
		has_value = False
		total = 0
		row = frappe._dict({
			"account": frappe._(d.name),
			"parent_account": frappe._(d.parent_account) if d.parent_account else '',
			"indent": flt(d.indent),
			"year_start_date": year_start_date,
			"year_end_date": year_end_date,
			"account_type": d.account_type,
			"is_group": d.is_group,
			"opening_balance": d.get("opening_balance", 0.0) * (1 if balance_must_be=="Debit" else -1),
			"account_name": ('%s - %s' %(frappe._(d.account_number), frappe._(d.account_name))
				if d.account_number else frappe._(d.account_name))
		})

		row["to_date"] = flt(d.get("to_date", 0.0), 3)

		if abs(row["to_date"]) >= 0.005:
			# ignore zero values
			has_value = True
			total += flt(row["to_date"])

		row["has_value"] = has_value
		row["total"] = total
		data.append(row)

	return data

def add_total_row(out, root_type, balance_must_be):
	total_row = {
		"account_name": frappe._("Total {0} ({1})").format(frappe._(root_type), frappe._(balance_must_be)),
		"account": frappe._("Total {0} ({1})").format(frappe._(root_type), frappe._(balance_must_be))
	}

	for row in out:
		if not row.get("parent_account"):
			total_row.setdefault('opening_balance', 0.0)
			total_row['opening_balance'] += row.get('opening_balance', 0.0)
			row['opening_balance'] = row.get('opening_balance', 0.0)
			total_row.setdefault("total", 0.0)
			total_row["total"] += flt(row["total"])
			row["total"] = ""

	if "total" in total_row:
		out.append(total_row)

		# blank row after Total
		out.append({})

def get_columns():
	columns = [{
		"fieldname": "account",
		"label": frappe._("Account"),
		"fieldtype": "Link",
		"options": "Account",
		"width": 300
	}, 
	{
		"fieldname": "opening_balance",
		"label": "Amount",
		"fieldtype": "Currency",
		"options": "currency",
		"width": 150
	}]

	return columns
