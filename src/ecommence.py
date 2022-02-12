# !/usr/bin/env python3 
# -*- coding: utf-8 -*-
# @Time    : 2022/2/12 14:59
# @Author  : Gene Jiang
# @File    : ecommence.py
# @Description:

from random import choice, randint

from faker.providers import BaseProvider

from .dict_ecommence import ecommence


class Ecommence(BaseProvider):

    def ecommence_object(self):
        ecommence_obj = choice(ecommence)
        if ecommence_obj:
            return ecommence_obj

    def get_random_element(self, element_list_name: str):
        ecommence_obj = self.ecommence_object()

        element = ecommence_obj.get(element_list_name)[
            randint(0, len(ecommence_obj.get(element_list_name)) - 1)]
        return element

    def order_status(self):
        return self.get_random_element('order_status')

    def sales_channel(self):
        return self.get_random_element('sales_channel')

    def pay_level(self):
        return self.get_random_element('pay_level')

    def pay_method(self):
        return self.get_random_element('pay_method')

    def appraise_level(self):
        return self.get_random_element('appraise_level')

    def deliver_method(self):
        return self.get_random_element('deliver_method')



