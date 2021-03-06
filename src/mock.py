# !/usr/bin/env python3 
# -*- coding: utf-8 -*-
# @Time    : 2022/2/11 17:17
# @Author  : Gene Jiang
# @File    : mock.py
# @Description:

from faker import Faker
from src.vehicle import VehicleProvider
from src.cn_province_city import CNAddressProvider
from src.normal_id import CustomizedId
from src.person import Person
from src.ecommence import Ecommence

fake = Faker('zh-CN')
fake.add_provider(VehicleProvider)
fake.add_provider(CNAddressProvider)
fake.add_provider(CustomizedId)
fake.add_provider(Person)
fake.add_provider(Ecommence)


province_city = fake.cn_province_city()

print(fake.vehicle_model(), fake.vehicle_series())
print(province_city.province, province_city.city)
print(fake.vehicle_model_series()[0], fake.vehicle_model_series()[1])
print(fake.userid(), fake.idfa(), fake.imei(), fake.openid(), fake.event_id())
print(fake.gender(), fake.birth_month(), fake.age(), fake.income(),
      fake.education(), fake.interests())
print(fake.order_status(), fake.sales_channel(),
      fake.pay_level(), fake.pay_method(),
      fake.appraise_level(), fake.deliver_method())

