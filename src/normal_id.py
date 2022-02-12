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

    def get_id(self, specified_id: str) -> str:
        id_obj = self.id_object()
        local_id = id_obj.get(specified_id)
        return local_id

    def userid(self):
        return self.get_id('userid')

    def openid(self):
        return self.get_id('openid')

    def idfa(self):
        return self.get_id('idfa')

    def imei(self):
        return self.get_id('imei')

    def event_id(self):
        return self.get_id('event_id')

