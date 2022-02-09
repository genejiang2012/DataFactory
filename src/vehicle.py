# !/usr/bin/env python3 
# -*- coding: utf-8 -*-
# @Time    : 2022/2/9 19:56
# @Author  : Gene Jiang
# @File    : vehicle.py.py
# @Description:


from random import choice, randint

import faker
from faker.providers import BaseProvider

from .changan_vehicle_dict import vehicles
from .province_city_dict import province_city


class VehicleProvider(BaseProvider):
    """
    A provider for vehicle related test data

    """

    def vehicle_object(self):
        """
        :return: return a random vehicle dict
        """
        veh = choice(vehicles)
        return veh

    def vehicle_model(self):
        veh = self.vehicle_object()
        model = veh.get('Model')
        return model

    def vehicle_series(self):
        veh = self.vehicle_object()
        series = veh.get('Series')
        return series


