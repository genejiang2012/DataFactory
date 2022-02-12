# !/usr/bin/env python3 
# -*- coding: utf-8 -*-
# @Time    : 2022/2/11 18:16
# @Author  : Gene Jiang
# @File    : cn_province_city.py
# @Description:
import logging
from collections import namedtuple
from random import choice, randint

from faker.providers import BaseProvider

from .dict_province_city import province_city


class CNAddressProvider(BaseProvider):
    """
    update the province and city property based on the owned province-city dict

    """

    def address_object(self):
        """
        get the province and city
        :return: one random item from the dict-province-city
        {
            'province': '澳门',
            'city_or_distinct': ['澳门']
        }
        """
        address = choice(province_city)
        if address:
            return address
        else:
            print('one empty dict')

    def cn_province(self):
        address = self.address_object()
        province = address.get('province')
        return province

    def cn_city(self):
        address = self.address_object()
        city = address.get('city')
        return city

    def cn_province_city(self):
        """
        :return: return one namedtuple with province and city
        """
        province_city_tuple = namedtuple('province_city', ['province', 'city'])
        address = self.address_object()
        province = address.get('province')
        city_list = address.get('city_or_distinct')
        city = city_list[
            randint(0, len(city_list) - 1)]
        # one instance from the named tuple
        province_city_instance = province_city_tuple(province, city)
        print(province_city_instance.province, province_city_instance.city)
        return province_city_instance
