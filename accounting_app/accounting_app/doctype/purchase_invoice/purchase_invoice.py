# -*- coding: utf-8 -*-
# Copyright (c) 2021, Mohammad Hussain Nagaria and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
# import frappe
from frappe.model.document import Document

class PurchaseInvoice(Document):
	def validate(self):
		self.set_status()
		
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




	
