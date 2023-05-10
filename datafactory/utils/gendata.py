# !/usr/bin/env python3 
# -*- coding: utf-8 -*-
# @Time    : 2023/5/10 19:55
# @Author  : Gene Jiang
# @File    : gendata.py.py
# @Description:

import sys
import jinja2
import json
import copy
from tqdm import tqdm
from datafactory.common.logger import log
from datafactory.common.setting import get_yaml




class DataGenerator:
    def __init__(self, faker, meta, connect=None):
        self.log = log
        self.all_packages = {}
        self.pre_data = {}
        self.result_data = {}
        self.extraction_data = {}
        self.error_fields = {}
        self.faker = faker
        self.sql = []
        # self.db = Database(connect) if connect else None
        self.meta = get_yaml(meta)


