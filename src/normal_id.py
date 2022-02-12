# !/usr/bin/env python3 
# -*- coding: utf-8 -*-
# @Time    : 2022/2/12 11:04
# @Author  : Gene Jiang
# @File    : normal_id.py
# @Description:

from random import choice

from faker.providers import BaseProvider

from .dict_different_id import different_id


class CustomizedId(BaseProvider):

    def id_object(self):
        id_obj = choice(different_id)
        if id_obj:
            return id_obj

    def userid(self):
        id_obj = self.id_object()
        customer_id = id_obj.get('userid')
        return customer_id

    def openid(self):
        id_obj = self.id_object()
        open_id = id_obj.get('open_id')
        return open_id

    def idfa(self):
        id_obj = self.id_object()
        idfa = id_obj.get('idfa')
        return idfa

    def imei(self):
        id_obj = self.id_object()
        imei = id_obj.get('imei')
        return imei

    def event_id(self):
        id_obj = self.id_object()
        event_id = id_obj.get('event_id')
        return event_id

