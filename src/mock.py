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

print(fake.vehicle_model(), fake.vehicle_series())
print(fake.address_province(), fake.address_city())
