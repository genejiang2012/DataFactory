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
        self.faker = faker
        self.meta_data = get_yaml(meta)
        self.db = None
        self.all_packages = {}
        self.log = log
        self.env_data = {'faker': faker, 'env': {}}
        self.field_data = {}
        self.extraction_data = {}
        self.log = log
        self.sql = []
        self.error_data = {}

    def start(self):
        self._env()
        # self._tables_handle()
        # self.extraction()
        # self._error_handle()
        # self.data2sql()

    def _env(self):
        """

        :return: 环境变量预处理
        """
        self.env_data.update(self.all_packages)
        env = self.meta_data.get('env')
        if not env:
            return
        self._field_handle(env_key='env', **env)

    def _field_handle(self, env_key=None, max_number=1, **kwargs):
        result = []
        i = 0
        while i < max_number:
            data = {}
            for key, value in copy.deepcopy(kwargs).items():
                try:
                    _value = self.dict_resolve(value)

    def dict_resolve(self, data: dict):
        """
        递归将字典的value使用模板格式化
        :param data:
        :return:
        """
        if not isinstance(data, dict) and isinstance(data, str):
            return self._template_render(data)
        elif isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, dict):
                    self.dict_resolve(value)
                elif isinstance(value, str):
                    value = self._template_render(value)
                data[key] = value
        return data


    def _template_render(self, s, env=None):
        """
        jinja2模板渲染
        :param s:
        :param env:
        :return:
        """
        source_type = type(s)

        if isinstance(s, (list, dict)):
            s = json.dumps(s).replace('\\\"', "'") # dict to string
        tp = jinja2.Template(s)

        if isinstance(env, dict):
            self.all_packages.update(env)
        tp.globals.update(self.all_packages)

        r = tp.render(**self.env_data)

        if source_type in [list, dict]:
            r = json.loads(r)   # json to dict
        return r

    def _gen_data(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        engine = kwargs.get('engine')
        rule = kwargs.get('rule')

        if isinstance(rule, str):
            rule = json.loads(self._template_render(rule))

        if not engine:
            return
        if "(" in engine and ")" in engine:
            r = eval(engine, self.env_data)
        else:
            if isinstance(rule, list):
                r = eval("{engine}(*{rule})".format(engine=engine, rule=rule),
                         self.env_data)
            elif isinstance(rule, dict):
                r = eval("{engine}(**{rule})".format(engine=engine, rule=rule),
                         self.env_data)
            elif rule is None:
                r = eval(f"{engine}()".format(engine=engine),
                         self.env_data)
            else:
                raise Exception('rule type must be dictionary or list!')
        return r




if __name__ == '__main__':
    from faker import Faker
    faker = Faker('zh-CN')

    meta = './meta.yml'

    dg = DataGenerator(faker, meta)
    # print(dg.meta)
    print(dg.env())


