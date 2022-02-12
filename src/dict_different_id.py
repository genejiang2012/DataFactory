# !/usr/bin/env python3 
# -*- coding: utf-8 -*-
# @Time    : 2022/2/12 10:59
# @Author  : Gene Jiang
# @File    : dict_different_id.py
# @Description:

import random
import string

different_id = [
    {
        'userid':
            "{}".format("".join(random.sample(string.ascii_letters
                                              + string.digits, 10))),
        'open_id':
            "".join(random.sample(string.ascii_letters + string.digits, 28)),
        'imei':
            "".join(random.sample(string.ascii_letters + string.digits, 15)),
        'idfa':
            "".join(random.sample(string.ascii_letters + string.digits, 16)),
        'event_id':
            "event_{}".format("".join(random.sample(string.ascii_letters +
                                                    string.digits, 12)))
    }
]
