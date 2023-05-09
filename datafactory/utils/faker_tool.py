# !/usr/bin/env python3 
# -*- coding: utf-8 -*-
# @Time    : 2023/5/6 19:59
# @Author  : Gene Jiang
# @File    : faker_tool.py
# @Description:


from faker.providers import BaseProvider
import random
import uuid
from datafactory.common.logger import log
import os
import re
import json
from datafactory.common.setting import check_path
from datafactory.common.database import Database
import pypinyin
import string
import time
import hashlib
from datetime import *


class Provider(BaseProvider):
    def __init__(self, generator, connect=None):
        super().__init__(generator)
        self.log = log
        self.db = None
        if connect:
            self.db = Database(connect)

    def hans2pinyin(self, hans, style='A'):
        """
        汉字转拼音
        :param hans: 汉字
        :param style: 返回首字母还是全拼， A：全拼； F：首字母
        :return:
        """

        if style.upper() == 'F':
            return ''.join(pypinyin.lazy_pinyin(hans=hans,
                                                style=pypinyin.Style.FIRST_LETTER))
        else:
            return ''.join(pypinyin.lazy_pinyin(hans=hans))

    def eq(self, value=None):
        """
        原样返回
        """
        return value

    def choice(self, value):
        if isinstance(value, str):
            try:
                value = json.loads(value)
            except json.decoder.JSONDecodeError:
                pass
        return random.choice(value)

    def choice_file(self, path, file_match=None, recursion=False, number=1):
        """
        指定目录寻找匹配规则的文件
        :param path:
        :param file_match:
        :param recursion:
        :return:
        """
        file_list = list(os.walk(check_path(path), ))
        if not file_list:
            return
        if not recursion:
            file_list = file_list[0][-1]
            result = [os.path.abspath(s.string) for s in
                      [re.match(file_match, x) for x in file_list] if s]
        else:
            result = []
            for k in list(zip(*file_list))[-1]:
                result += k
            result = [os.path.abspath(s.string) for s in
                      [re.match(file_match, x) for x in result] if s]
        if len(result) > number:
            result = random.sample(result, number)
        return result

    def uuid(self, underline=True):
        """
        返回遗传32位随机字符串
        """
        uid = str(uuid.uuid4())
        if underline:
            uid = uid.replace("-", '')
        self.log.d('生成uuid： {}'.format(uid))
        return uid

    def from_db(self, sql, choice_method='random', key=None):
        """
        从数据库中查数据
        :param sql: 查询语句
        :param choice_method: 对返回多个值时的处理方式，random： 随机取一个， first：取第一个，其它：返回整个list
        :param key: 当key存在时，将从返回数据键值对中取键为“key”的值
        :param tag:
        :return:
        """
        if not self.db:
            self.log.w('未指定数据库连接引擎，无法从数据库查询数据')
            return
        result = self.db.select3(sql)
        if not result:
            return
        if key:
            result = [i[key] for i in result]
        if choice_method == 'random':
            result = random.choice(result)
        elif choice_method == 'first':
            result = result[0]
        return result

    def from_db_yield(self, sql, key=None):
        """
        从数据库中查数据
        :param sql: 查询语句
        :param choice_method: 对返回多个值时的处理方式，random：
                              随机取一个， first：取第一个，其它：返回整个list
        :param key: 当key存在时，将从返回数据键值对中取键为“key”的值
        :return:
        """
        if not self.db:
            self.log.w('未指定数据库连接引擎，无法从数据库查询数据')
            return
        result = self.db.select3(sql)
        if key:
            result = [i[key] for i in result]
        for i in result:
            yield i

    def weights_randint(self, *args):
        """
        带权重的随机数，int型
        >> weights_randint({"weight": 0.8, "value": [1,2]}, {"weight": 0.2, "value": [3,4]})
        >> 1
        """
        result = []
        for d in args:
            _weights = d.get('weight')
            value = d.get('value')
            if isinstance(value, str):
                try:
                    value = json.loads(value)
                except json.decoder.JSONDecodeError:
                    pass

            n = 10
            while _weights < 1:
                _weights = int(_weights * n)
            for i in range(_weights):
                result.append(random.randint(*value))
        result = random.choice(result)
        return result

    def weights_randfloat(self, *args, round_num=2):
        """
        权重计算随机数float类型
        :param args:
        :param round_num:
        :return:
        """
        result = []
        for d in args:
            _weights = d.get('weight')
            value = d.get('value')
            if isinstance(value, str):
                try:
                    value = json.loads(value)
                except json.decoder.JSONDecodeError:
                    pass
            if d.get("round_num"):
                round_num = d.get("round_num")
            n = 10
            while _weights < 1:
                _weights = int(_weights * n)
            for i in range(_weights):
                result.append(round(random.uniform(*value), round_num))
        result = random.choice(result)
        return result

    def weights_choice(self, *args):
        """
        权重选择
        :param args:
        :return:
        """
        values = []
        for d in args:
            weights = d.get('weight')
            value = d.get('value')
            if isinstance(value, str):
                try:
                    value = json.loads(value)
                except json.decoder.JSONDecodeError:
                    pass
            if weights < 1:
                weights = int(weights * 100 / len(value))
            for i in value:
                values += [i] * weights
        result = random.choice(values)
        return result

    def multi_choice(self, value, splits="|", rand_number=None):
        """
        从指定的列表中随机选择多个，使用拼接字符拼起来返回
        :param value:
        :param splits:
        :return:
        """
        if isinstance(value, str):
            try:
                value = json.loads(value)
            except json.decoder.JSONDecodeError:
                pass
        if not rand_number or rand_number > len(value):
            rand_number = random.randint(1, len(value))
        return splits.join([str(i) for i in random.sample(value, rand_number)])
        # return [str(i) for i in random.sample(value, rand_number)]

    def randint(self, value: list):
        """
        从给定的数值范围内随机返回一个int数值
        """
        if isinstance(value, str):
            try:
                value = json.loads(value)
            except json.decoder.JSONDecodeError:
                pass
        return random.randint(*value)

    def randfloat(self, value: list, round_num=2):
        """
        从给定的数值范围内随机返回一个float数值
        """
        if isinstance(value, str):
            try:
                value = json.loads(value)
            except json.decoder.JSONDecodeError:
                pass
        return round(random.uniform(*value), round_num)

    def randstring(self, prefix: string, number: int):
        """
        return the random string based on specified prefix and number
        :param prefix: string, specified the prefix, such as od, mock, etc
        :param number: int, specified the number for generating the string
        """
        return "{}{}".format(prefix, "".join(
            random.sample(string.ascii_letters + string.digits, number)))

    def randphonenumber(self, prefix: string) -> string:
        """
        return the random string based on specified prefix and number
        :param prefix: string, specified the prefix, such as od, mock, etc
        :param number: int, specified the number for generating the string
        """
        local_value = self.get_phone_num()
        # print("phone_number value", "{}{}".format(prefix, local_value))
        return "{}{}".format(prefix, local_value)

    def randphonenumber_md5(self, prefix: string):
        """
        return the random string based on specified prefix and number
        :param prefix: string, specified the prefix, such as od, mock, etc
        :param number: int, specified the number for generating the string
        """
        local_value = self.randphonenumber(prefix)
        # print("phone_number value2", local_value, self.gen_md5(local_value))
        return local_value, self.gen_md5(local_value)

    def rand_mac(self):
        """
        """
        return "{}-{}-{}-{}-{}-{}".format(
            "".join(
                random.sample(
                    string.ascii_uppercase + string.digits,
                    2)),
            "".join(
                random.sample(
                    string.ascii_uppercase + string.digits,
                    2)),
            "".join(
                random.sample(
                    string.ascii_uppercase + string.digits,
                    2)),
            "".join(
                random.sample(
                    string.ascii_uppercase + string.digits,
                    2)),
            "".join(
                random.sample(
                    string.ascii_uppercase + string.digits,
                    2)),
            "".join(
                random.sample(
                    string.ascii_uppercase + string.digits,
                    2))

        )

    def rand_mac_md5(self):
        local_value = self.rand_mac()
        return local_value, self.gen_md5(local_value)

    def randwechatid(self, number: int):
        """
        return the wechat id, such as unionid, openid
        :param number: int, specified the number for generating the string
        """
        return "oO8fw5{}".format("".join(
            random.sample(
                string.ascii_letters + string.digits,
                number)))

    def randmixedid(self, number: int):
        """
        return the device id, such as IDFA, IMEI, OAID
        :param number: int, specified the number for generating the string
        """
        return "{}".format("".join(
            random.sample(
                string.ascii_letters + string.digits + string.ascii_letters,
                number)))

    def randmixedid_md5(self, number: int):
        """
        return the device id, such as IDFA, IMEI, OAID
        :param number: int, specified the number for generating the string
        """
        local_value = "{}".format("".join(
            random.sample(
                string.ascii_letters + string.digits + string.ascii_letters,
                number)))
        return local_value, self.gen_md5(local_value)

    def randmixedid_sha256(self, number: int):
        """
        return the device id, such as IDFA, IMEI, OAID
        :param number: int, specified the number for generating the string
        """
        local_value = "{}".format("".join(
            random.sample(
                string.ascii_letters + string.digits,
                number)))
        return self.gen_sha256(local_value)

    def randid(self, prefix: string, number: int):
        """
        return the random string based on specified prefix and number
        :param prefix: string, specified the prefix, such as od, mock, etc
        :param number: int, specified the number for generating the string
        """
        return "{}{}".format(prefix,
                             "".join(random.sample(string.digits, number)))

    def gen_md5(self, value: str):
        """
        return the md5 string based on specified value
        """
        m = hashlib.md5()
        m.update(value.encode("utf8"))
        m_md5 = m.hexdigest()
        return m_md5

    def get_year(self, value: str):
        now_time = self.get_time(value)[0]
        return now_time.strftime("%Y")

    def get_month(self, value: str):
        now_time = self.get_time(value)[0]
        return now_time.strftime("%m")

    def get_day(self, value: str):
        now_time = self.get_time(value)[0]
        return now_time.strftime("%d")

    def get_month_day(self, value: str, separator: str):
        month = self.get_month(value)
        day = self.get_day(value)
        return '{}separator{}'.format(month, day)

    def get_week_of_month(self, value: str):
        now_time = self.get_time(value)[0]
        one_time = self.get_time(value)[1]

        return int(now_time.strftime('%W')) - int(one_time.strftime('%W')) + 1

    def get_quarter(self, value: str):
        month = int(self.get_month(value))
        quarter = (month - 1) // 3 + 1
        return 'Q{}'.format(quarter)

    def get_quarter_of_year(self, value: str):
        year = self.get_year(value)
        month = int(self.get_month(value))
        quarter = (month - 1) // 3 + 1
        return '{}Q{}'.format(year, quarter)

    def get_week_day(self, value: str):
        now_time = self.get_time(value)[0]
        return now_time.isoweekday()

    def get_week_year(self, value: str):
        now_time = self.get_time(value)[0]
        return now_time.isocalendar()[1]

    @staticmethod
    def get_time(value: str):
        if value and isinstance(value, str):
            now_time = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        else:
            now_time = datetime.now().replace(hour=0, minute=0, second=0,
                                              microsecond=0)

        one_time = now_time.replace(day=1, hour=0, minute=0, second=0,
                                    microsecond=0)
        return now_time, one_time

    @staticmethod
    def gen_sha256(value: str):
        hsobj = hashlib.sha256(value.encode("utf-8"))
        hsobj.update()
        return hsobj.hexdigest()

    @staticmethod
    def order(value, out_of_order=False):
        """
        返回一个列表生成器对象，使用next()来调用
        """
        if out_of_order and isinstance(value, list):
            value = list(set(value))
        for i in json.loads(value):
            yield i

    @staticmethod
    def get_phone_num():
        second_spot = random.choice([3, 4, 5, 7, 8])
        third_spot = {3: random.randint(0, 9),
                      4: random.choice([5, 7, 9]),
                      5: random.choice([i for i in range(10) if i != 4]),
                      7: random.choice(
                          [i for i in range(10) if i not in [4, 9]]),
                      8: random.randint(0, 9), }[second_spot]
        remain_spot = random.randint(9999999, 100000000)
        phone_num = "1{}{}{}".format(second_spot, third_spot, remain_spot)
        return phone_num

if __name__ == "__main__":
    local_provider = Provider(BaseProvider)
    local_provider.get_week_day("2022-4-13 10:00:00")
    result = local_provider.weights_randint({"weight": 0.3, "value": [1,5]})
    print(result)
