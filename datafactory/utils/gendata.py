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

    def env(self):
        """

        :return: 环境变量预处理
        """
        self.env_data.update(self.all_packages)
        log.info(self.env_data)

        env = self.meta_data.get('env')
        log.info(env)
        if not env:
            return
        self._field_handle(env_key='env', **env)

    def import_packages(self):
        self._import_packages()

    def _import_packages(self):
        """
        动态导包
        :return:
        """
        if isinstance(__builtins__, dict):
            self.all_packages.update(__builtins__)
        else:
            self.all_packages.update(__builtins__.__dict__)
        packages = self.meta_data.get('package')

        for i in packages:
            try:
                self.all_packages[i] = __import__(i)
            except ModuleNotFoundError:
                self.log.e('imported package {} failed'.format(i))
        for class_name in dir(self.faker):
            provider = getattr(self.faker, class_name)
            if callable(provider) and not class_name.startswith('_'):
                self.all_packages[class_name] = provider

        self.all_packages['faker'] = self.faker

    def _field_handle(self, env_key=None, max_number=1, **kwargs):
        result = []
        i = 0
        while i < max_number:
            data = {}
            for key, value in copy.deepcopy(kwargs).items():
                try:
                    log.info("the value is {}".format(value))
                    _value = self.dict_resolve(value)
                    log.info("the _value is {}".format(_value))
                    log.debug(_value)
                    if not isinstance(value, dict):
                        _data = {
                            key: self._gen_data(**{"engine": "eq", "rule": {"value": _value}})
                        }
                    elif 'engine' not in _value:
                        _data = {key: self._field_handle(**_value)}
                    else:
                        _data = {key: self._gen_data(**_value)}
                    data.update(_data)
                except jinja2.exceptions.UndefinedError:
                    if env_key not in self.error_data:
                        self.error_data[env_key] = {}
                    self.error_data[env_key].update({key:value})
                    continue
                if env_key:
                    if env_key not in self.env_data or callable(self.env_data[env_key]):
                        self.env_data[env_key] = {}
                    self.env_data[env_key].update(data)
            result.append(data)
            i += 1

        return result


    def dict_resolve(self, data: dict):
        """.
        递归将字典的value使用模板格式化
        :param data:
        :return:
        """
        if not isinstance(data, dict) and isinstance(data, str):
            log.info(self._template_render(data))
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
        log.info('The kwargs is {}'.format(kwargs))
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
                log.info("{engine}(**{rule})".format(engine=engine, rule=rule))
                log.info(self.env_data)
                r = eval("{engine}(**{rule})".format(engine=engine, rule=rule),
                         # self.env_data
                         )
            elif rule is None:
                r = eval("{engine}()".format(engine=engine),
                         self.env_data)
            else:
                raise Exception('rule type must be dictionary or list!')
        return r




if __name__ == '__main__':
    from faker import Faker
    faker = Faker('zh-CN')

    meta = './test.yml'

    dg = DataGenerator(faker, meta)
    # print(dg.meta)
    print(dg.env())


