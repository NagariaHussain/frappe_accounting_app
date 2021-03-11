# -*- coding: utf-8 -*-
# Copyright (c) 2021, Mohammad Hussain Nagaria and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import flt

class JournalEntry(Document):
	def validate(self):
		self.validate_total_debit_credit()
	
	def validate_total_debit_credit(self):
		'''throw if total credit not equal to total debit'''
		total_debit, total_credit = 0, 0
		difference = 0

		for acc in self.get("accounts"):
			total_debit = flt(total_debit) + flt(acc.debit, acc.precision("debit"))
			total_credit = flt(total_credit) + flt(acc.credit, acc.precision("credit"))
		
		difference = total_debit - total_credit

		if difference:
			frappe.throw(frappe._("Total Debit must be equal to Total Credit. The difference is {0}"
							.format(difference)
			))

	def on_submit(self):
		self.make_gl_entries()

	def make_gl_entries(self, is_cancel=0):
		'''create and save General Ledger Entries'''
		for acc in self.get("accounts"):
			# Create new LE doc
			le = frappe.new_doc("Ledger Entry")

			# Set fields
			if is_cancel:
				le.debit = acc.credit
				le.credit = acc.debit
			else:
				le.debit = acc.debit
				le.credit = acc.credit

			le.account = acc.account
			le.posting_date = self.posting_date

			# Save LE doc
			le.submit()

	def on_cancel(self):
		# Create reverse GL entries 
		# for this Journal Entry
		self.make_gl_entries(1)

