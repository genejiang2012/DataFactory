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
        self.env_data = {'faker': faker, 'env': {}}
        self.result_data = {}
        self.extraction_data = {}
        self.error_fields = {}
        self.faker = faker
        self.sql = []
        # self.db = Database(connect) if connect else None
        self.meta_data = get_yaml(meta)

    def start(self):
        self.result_data = {}
        self.extraction_data = {}
        self.env()

    def _env(self):
        """

        :return: 环境变量预处理
        """
        self.env_data.update(self.all_packages)
        env = self.meta_data.get('env')
        if not env:
            return
        self._field_handle(env_key='env', **env)

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

    def _template_render(self, s, env=None):
        """
        jinja2模板渲染
        :param s:
        :param env:
        :return:
        """
        source_type = type(s)

        if isinstance(s, (list, dict)):
            s = json.dumps(s).replace('\\\"', "'")
        tp = jinja2.Template(s)
        if isinstance(env, dict):
            self.all_packages.update(env)

        tp.globals.update(self.all_packages)

        r = tp.render(**self.env_data)

        if source_type in [list, dict]:
            r = json.loads(r)
        return r


if __name__ == '__main__':
    from faker import Faker
    faker = Faker('zh-CN')

    meta = './meta.yml'

    dg = DataGenerator(faker, meta)
    # print(dg.meta)
    print(dg.env())


