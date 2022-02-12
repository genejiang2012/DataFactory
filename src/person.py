# !/usr/bin/env python3 
# -*- coding: utf-8 -*-
# @Time    : 2022/2/12 12:54
# @Author  : Gene Jiang
# @File    : person.py
# @Description:

from random import choice, randint

from faker.providers import BaseProvider

from .dict_person import person


class Person(BaseProvider):

    def person_objects(self):
        person_obj = choice(person)
        if person_obj:
            return person_obj

    def get_random_element(self, element_list_name: str):
        person_obj = self.person_objects()

        element = person_obj.get(element_list_name)[
            randint(0, len(person_obj.get(element_list_name)) - 1)]
        return element

    def gender(self):
        return self.get_random_element('genders')

    def birth_month(self):
        return self.get_random_element('birth_month')

    def age(self):
        return self.get_random_element('age')

    def income(self):
        return self.get_random_element('income')

    def education(self):
        return self.get_random_element('education')

    def interests(self):
        return self.get_random_element('interests')



