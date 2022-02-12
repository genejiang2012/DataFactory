# !/usr/bin/env python3 
# -*- coding: utf-8 -*-
# @Time    : 2022/2/9 19:56
# @Author  : Gene Jiang
# @File    : vehicle.py.py
# @Description:

from collections import namedtuple
from random import choice

from faker.providers import BaseProvider

from .dict_changan_vehicle import vehicles




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

    def vehicle_model_series(self):
        tuple_model_series = namedtuple('model_series', ['model', 'series'])
        veh = self.vehicle_object()
        model = veh.get('Model')
        series = veh.get('Series')
        model_series_instance = tuple_model_series(model, series)
        return model_series_instance


