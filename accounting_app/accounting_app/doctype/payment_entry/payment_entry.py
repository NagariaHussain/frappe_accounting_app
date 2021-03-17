# -*- coding: utf-8 -*-
# Copyright (c) 2021, Mohammad Hussain Nagaria and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import nowdate, flt

class PaymentEntry(Document):
	def validate(self):
		if self.voucher_type == "Purchase Invoice":
			ca = frappe.get_doc("Account", self.credit_account)
			if not (ca.root_type == "Expense"):
				frappe.throw("Credit Account should be of type: Expense")
		elif self.voucher_type == "Sales Invoice":
			da = frappe.get_doc("Account", self.debit_account)
			if not (da.root_type == "Income"):
				frappe.throw("Debit Account should be of type: Income")
		else:
			frappe.throw("Payment entry can only be made against SI or PI")

	def on_submit(self):
		if self.voucher_type == "Purchase Invoice":
			self.make_gl_entries("Creditors", self.credit_account)
		elif self.voucher_type == "Sales Invoice":
			self.make_gl_entries(self.debit_account, "Debtors")

		self.update_linked_voucher()

	def on_cancel(self):
		if self.voucher_type == "Purchase Invoice":
			self.make_gl_entries("Creditors", self.credit_account, reverse=True)
		else:
			self.make_gl_entries(self.debit_account, "Debtors", reverse=True)
		
		self.update_linked_voucher()

	def update_linked_voucher(self):
		voucher = frappe.get_doc(self.voucher_type, self.voucher_link)
		voucher.paid = True
		voucher.set_status()
		voucher.save()

	def make_gl_entries(self, debit_acc, credit_acc, reverse=False):
		if reverse:
			debit_acc, credit_acc = credit_acc, debit_acc
		# Debit
		debit_gl_entry = frappe.new_doc("Ledger Entry")
		debit_gl_entry.account = debit_acc
		debit_gl_entry.credit = flt(0, self.precision("amount"))
		debit_gl_entry.debit = self.amount
		debit_gl_entry.submit()

		# Credit
		credit_gl_entry = frappe.new_doc("Ledger Entry")
		credit_gl_entry.account = credit_acc
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
