# !/usr/bin/env python3 
# -*- coding: utf-8 -*-
# @Time    : 2022/2/11 17:17
# @Author  : Gene Jiang
# @File    : mock.py
# @Description:

from faker import Faker
from src.vehicle import VehicleProvider
from src.cn_province_city import CNAddressProvider

fake = Faker('zh-CN')
fake.add_provider(VehicleProvider)
fake.add_provider(CNAddressProvider)

province_city = fake.cn_province_city()

print(fake.vehicle_model(), fake.vehicle_series())
print(province_city.province, province_city.city)
print(fake.vehicle_model_series()[0], fake.vehicle_model_series()[1])

