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

    def start(self):
        self.result_data = {}
        self.extraction_data = {}
        self._env()

    def _env(self):
        """

        :return: 环境变量预处理
        """
        self.pre_data['env'] = {}
        env = self.meta.get('env')
        if not env:
            return
        for index, value in env.items():
            engine = value.get('engine')
            rule = value.get('rule')
            rule = json.dumps(rule)
            result = self._gen_data(engine, rule)
            self.pre_data['env'][index] = result

    def _gen_data(self, engine: str, rule):
        """

        :param engine:
        :param rule:
        :return:
        """
        if isinstance(rule, str):
            rule = json.loads(self._template_render(rule))
        faker = self.faker
        if not engine:
            return
        if '.' not in engine:
            engine = "faker.{engine}".format(engine=engine)
        if isinstance(rule, list):
            r = eval("{engine}(*{rule})".format(engine=engine, rule=rule))
        if isinstance(rule, dict):
            r = eval("{engine}(**{rule})".format(engine=engine, rule=rule))
        elif rule is None:
            r = eval(f"{engine}()".format(engine=engine))
        return 0

    def _template_render(self, s, env=None):
        """
        jinja2模板渲染
        :param s:
        :param env:
        :return:
        """
        tp = jinja2.Template(s, undefined=jinja2.StrictUndefined)
        if isinstance(env, dict):
            self.all_packages.update(env)
        tp.globals.update(self.all_packages)
        r = tp.render(**self.pre_data)
        return r

