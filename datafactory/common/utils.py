# !/usr/bin/env python3 
# -*- coding: utf-8 -*-
# @Time    : 2023/5/9 19:54
# @Author  : Gene Jiang
# @File    : utils.py
# @Description:

import time

def tim_cost(func):
    """
    装饰器， 统计函数的耗时 @time_cost
    :param func: 函数
    :return:
    """
    def _wrapper(*args, **kwargs):
        start = time.time()
        closure = func(*args, **kwargs)
        return time.time() - start, closure

    return _wrapper
