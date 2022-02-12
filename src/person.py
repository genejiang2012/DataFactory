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

    def gender(self):
        person_obj = self.person_objects()
        gender = person_obj.get('genders')[
            randint(0, len(person_obj.get('genders')) - 1)]
        return gender

    def birth_month(self):
        person_obj = self.person_objects()
        birth_month = person_obj.get('birth_month')[
            randint(0, len(person_obj.get('birth_month')) - 1)
        ]
        return birth_month

    def age(self):
        person_obj = self.person_objects()
        age = person_obj.get('age')[
            randint(0, len(person_obj.get('age')) - 1)
        ]
        return age

    def income(self):
        person_obj = self.person_objects()
        income = person_obj.get('income')[
            randint(0, len(person_obj.get('income')) - 1)
        ]
        return income

    def education(self):
        person_obj = self.person_objects()
        education = person_obj.get('education')[
            randint(0, len(person_obj.get('education')) - 1)
        ]
        return education

    def interests(self):
        person_obj = self.person_objects()
        interests = person_obj.get('interests')[
            randint(0, len(person_obj.get('interests')) - 1)
        ]
        return interests



