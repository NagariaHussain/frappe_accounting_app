# -*- coding: utf-8 -*-
# Copyright (c) 2021, Mohammad Hussain Nagaria and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
# import frappe

from frappe.utils.nestedset import NestedSet
from frappe.utils import cstr

class Account(NestedSet):
	def autoname(self):
		self.name = self.get_autoname_with_number(
			self.account_number,
			self.account_name
		)
	
	def get_autoname_with_number(self, number_value, doc_title):
		name = doc_title
		if number_value:
			name += (' - ' + number_value)
		return name 
