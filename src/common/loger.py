# !/usr/bin/env python3 
# -*- coding: utf-8 -*-
# @Time    : 2022/2/15 19:23
# @Author  : Gene Jiang
# @File    : loger.py
# @Description:


import os
import logging.config
from logging import ERROR, DEBUG, INFO, WARNING
import yaml


class CustomLogger:
    """
    customize the loggers to print the blank line before and after messages
    """
    logging.config.dictConfig(yaml.safe_load(open()))
