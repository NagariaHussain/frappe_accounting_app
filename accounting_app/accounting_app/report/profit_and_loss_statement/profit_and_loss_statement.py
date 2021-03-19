# Copyright (c) 2013, Mohammad Hussain Nagaria and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from accounting_app.accounting_app.report.financial_statements import get_data, get_columns
from frappe.utils import flt

def execute(filters=None):
	columns, data = [], []

	income = get_data("Income", "Credit", filters.from_date, filters.to_date)
	expense = get_data("Expense", "Debit", filters.from_date, filters.to_date)

	net_profit_loss = get_net_profit_loss(income, expense)

	data.extend(income or [])
	data.extend(expense or [])

	if net_profit_loss:
		data.append(net_profit_loss)
	
	columns = get_columns()

	return columns, data


def get_net_profit_loss(income, expense):
	net_profit_loss = {
		"account_name": "'" + frappe._("Profit for the year") + "'",
		"account": "'" + frappe._("Profit for the year") + "'",
		"warn_if_negative": True
	}

	total_income = flt(income[-2]['opening_balance'], 3)
	total_expense = flt(expense[-2]['opening_balance'], 3)

	net_profit_loss['opening_balance'] = total_income - total_expense

	return net_profit_loss