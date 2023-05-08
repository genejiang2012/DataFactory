# !/usr/bin/env python3 
# -*- coding: utf-8 -*-
# @Time    : 2023/5/8 19:43
# @Author  : Gene Jiang
# @File    : tools.py.py
# @Description:

import os
import sys

def get_program_directory():
    cur_dir = os.getcwd()
    if not cur_dir:
        cmd = sys.argv[0]
        cur_dir = None
        if cmd:
            cur_dir, filename = os.path.split(cmd)

    return os.path.abspath(cur_dir)

def check_path(path):
    if not os.path.isabs(path):
        path = os.path.join(get_program_directory(), path)

    return path

def get_current_path(current_path, path):
    if not os.path.isabs(path):
        path = os.path.join(
            os.path.dirname(os.path.realpath(current_path)),
            path
        )

    return path


