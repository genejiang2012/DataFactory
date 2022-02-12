# !/usr/bin/env python3 
# -*- coding: utf-8 -*-
# @Time    : 2022/2/11 18:16
# @Author  : Gene Jiang
# @File    : cn_province_city.py
# @Description:


from random import choice, randint

import city as city
import faker
from faker.providers import BaseProvider

from .province_city_dict import province_city


class CNAddressProvider(BaseProvider):
    province = None
    city = None
    def address_object(self):

        address = choice(province_city)

        CNAddressProvider.province = address.get('province')
        city_list = address.get('city_or_distinct')
        CNAddressProvider.city = city_list[
             randint(0, len(city_list) - 1)]
        print("The address" + CNAddressProvider.province+CNAddressProvider.city)
        return CNAddressProvider.province, CNAddressProvider.city

    def address_province(self):
        self.address_object()
        return CNAddressProvider.province

    def address_city(self):
        self.address_object()

        return CNAddressProvider.city
