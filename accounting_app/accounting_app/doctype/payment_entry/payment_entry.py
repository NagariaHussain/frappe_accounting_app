# -*- coding: utf-8 -*-
# Copyright (c) 2021, Mohammad Hussain Nagaria and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import nowdate

class PaymentEntry(Document):
	pass

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
