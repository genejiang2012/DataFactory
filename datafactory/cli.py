# !/usr/bin/env python3 
# -*- coding: utf-8 -*-
# @Time    : 2022/10/25 15:53
# @Author  : Gene Jiang
# @File    : cli.py.py
# @Description:

import sys
import argparse
import os
import importlib

from datafactory.utils.constant import __version__


def parse_args():
    if '--version' in sys.argv:
        print(__version__)
        exit(0)

    parser = argparse.ArgumentParser(
        description='通过yml格式来生成数据'
    )
    parser.add_argument('meta_file', nargs='?', action='store',
                        help='yml文件所在路径')
    parser.add_argument('-n', '--numbers', nargs='?', action='store',
                        default=1, help='生成数据量', type=int)
    parser.add_argument('-o', '--output', nargs='?', action='store',
                        help='指定文件名， 输出内容')
    parser.add_argument('-p', '--_print', action='store_true',
                        help='是否打印到控制台')

    # 参数放入args
    args = parser.parse_args()
    if not args.meta_file:
        parser.print_help()
        exit(0)

    return args