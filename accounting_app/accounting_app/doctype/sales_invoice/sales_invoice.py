# -*- coding: utf-8 -*-
# Copyright (c) 2021, Mohammad Hussain Nagaria and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from frappe.model.document import Document
from six.moves.urllib.parse import parse_qsl
from frappe.utils import flt
from frappe.utils.pdf import get_pdf


class SalesInvoice(Document):
	def validate(self):
		self.set_status()
		self.set_grand_total()

	def set_status(self):
		if self.is_new():
			if self.get('amended_form'):
				self.status = "Draft"
			return
		
		if self.docstatus == 2:
			self.status = "Cancelled"
		elif self.docstatus == 1:
			if self.paid:
				self.status = "Paid"
			else:
				self.status = "Unpaid"

	def set_grand_total(self):
		total = flt(
			0, 
			self.precision("grand_total")
		)

		for item in self.get("items"):
			total += flt(item.amount)
		
		self.grand_total = total

	def on_submit(self):
		self.make_gl_entries()
	
	def make_gl_entries(self):
		# Credit
		credit_gle = frappe.new_doc("Ledger Entry")
		credit_gle.account = "Stock In Hand"
		credit_gle.credit = self.grand_total
		credit_gle.debit = flt(0, self.precision("grand_total"))
		credit_gle.submit()

		# Debit
		debit_gle = frappe.new_doc("Ledger Entry")
		debit_gle.account = "Debtors"
		debit_gle.debit = self.grand_total
		debit_gle.credit = flt(0, self.precision("grand_total"))
		debit_gle.submit()

	def on_cancel(self):
		# Update status
		self.set_status()
		# Make reverse entries
		self.make_reverse_gl_entries()

	def make_reverse_gl_entries(self):
		# Credit
		credit_gle = frappe.new_doc("Ledger Entry")
		credit_gle.account = "Debtors"
		credit_gle.credit = self.grand_total
		credit_gle.debit = flt(0, self.precision("grand_total"))
		credit_gle.submit()

		# Debit
		debit_gle = frappe.new_doc("Ledger Entry")
		debit_gle.account = "Stock In Hand"
		debit_gle.debit = self.grand_total
		debit_gle.credit = flt(0, self.precision("grand_total"))
		debit_gle.submit()

@frappe.whitelist(allow_guest=True)
def generate_invoice():
	query_string = frappe.local.request.query_string
	query = dict(parse_qsl(query_string))
	query = {key.decode(): val.decode() for key, val in query.items()}
	
	name = "customer invoice"
	html = '''
<h1>Invoice for Gada Electronics e-Store!</h1>
	'''

	# Add items to PDF HTML
	html += "<ol>"
	for item, qty in query.items():
		html += f"<li>{item} - {qty}</li>"
	html += "</ol>"
	
	frappe.local.response.filename = "{name}.pdf".format(name=name.replace(" ", "-").replace("/", "-"))
	frappe.local.response.filecontent = get_pdf(html)
	frappe.local.response.type = "pdf"
