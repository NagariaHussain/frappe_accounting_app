# -*- coding: utf-8 -*-
# Copyright (c) 2021, Mohammad Hussain Nagaria and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import nowdate, flt

class PaymentEntry(Document):
	def on_submit(self):
		if self.voucher_type == "Purchase Invoice":
			self.make_pi_gl_entries()
		else:
			pass
		
		voucher = frappe.get_doc(self.voucher_type, self.voucher_link)
		voucher.paid = True
		voucher.save()

	def make_pi_gl_entries(self):
		# Debit the "Creditors" account
		debit_gl_entry = frappe.new_doc("Ledger Entry")
		debit_gl_entry.account = "Creditors"
		debit_gl_entry.credit = flt(0, self.precision("amount"))
		debit_gl_entry.debit = self.amount
		debit_gl_entry.submit()

		# Credit the "Expenses" account
		credit_gl_entry = frappe.new_doc("Ledger Entry")
		credit_gl_entry.account = self.credit_account
		credit_gl_entry.credit = self.amount
		credit_gl_entry.debit = flt(0, self.precision("amount"))
		credit_gl_entry.submit()

@frappe.whitelist()
def get_payment_entry(dt, dn):
	# Fetch the associated doc
	doc = frappe.get_doc(dt, dn)

	# Create new payment entry
	pe = frappe.new_doc("Payment Entry")
	pe.amount = doc.grand_total
	pe.voucher_type = doc.doctype
	pe.voucher_link = doc.name
	pe.posting_date = nowdate()

	# return pe doc
	return pe
