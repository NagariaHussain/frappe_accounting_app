# -*- coding: utf-8 -*-
# Copyright (c) 2021, Mohammad Hussain Nagaria and Contributors
# See license.txt
from __future__ import unicode_literals

import frappe
import unittest

from accounting_app.accounting_app.doctype.payment_entry.payment_entry import get_payment_entry

class TestPaymentEntry(unittest.TestCase):
	def test_get_payment_entry_for_pi(self):
		pi = get_sample_voucher_of_type('Purchase Invoice')

		pe = get_payment_entry('Purchase Invoice', pi.name)

		self.assertEqual(pe.amount, pi.grand_total, "PE's amount and PI's grand_total does not match")
		self.assertEqual(pe.voucher_type, 'Purchase Invoice', "Voucher type should be PI")
		self.assertEqual(pe.voucher_link, pi.name, "PI name does not match with PE's linked name")

	def test_get_payment_entry_for_si(self):
		si = get_sample_voucher_of_type('Sales Invoice')

		pe = get_payment_entry('Sales Invoice', si.name)

		self.assertEqual(pe.amount, si.grand_total, "PE's amount and si's grand_total does not match")
		self.assertEqual(pe.voucher_type, 'Sales Invoice', "Voucher type should be si")
		self.assertEqual(pe.voucher_link, si.name, "si name does not match with PE's linked name")

def get_sample_voucher_of_type(v_type):
	voucher = frappe.new_doc(v_type)
	voucher.title = f"Test {v_type}"

	# Add sample items to child table
	voucher.append("items", {
			"item": "Envy 13",
			"qty": 10,
			"rate": 100,
			"amount": 1000
		})

	voucher.append("items", {
			"item": "iPhone 12",
			"qty": 5,
			"rate": 10,
			"amount": 50
		})

	voucher.insert()

	return voucher