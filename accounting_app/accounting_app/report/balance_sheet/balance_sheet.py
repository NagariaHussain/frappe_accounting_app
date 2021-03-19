# Copyright (c) 2013, Mohammad Hussain Nagaria and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from accounting_app.accounting_app.report.financial_statements import get_data, get_columns

def execute(filters=None):
	columns, data = [], []

	# Get data by root account type
	asset = get_data("Asset", "Debit", filters.from_date, filters.to_date)
	liability = get_data("Liability", "Debit", filters.from_date, filters.to_date)
	equity = get_data("Equity", "Credit", filters.from_date, filters.to_date)
	
	# Add data to rows
	data.extend(asset or [])
	data.extend(liability or [])
	data.extend(equity or [])

	# Add columns
	columns = get_columns()

	return columns, data
