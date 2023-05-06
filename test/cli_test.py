# !/usr/bin/env python3 
# -*- coding: utf-8 -*-
# @Time    : 2023/5/6 19:32
# @Author  : Gene Jiang
# @File    : cli_test.py.py
# @Description:

from datafactory.cli import parse_args, execute


def test_parse_args():
    args = parse_args()
    assert args.meta_file == 'cli_test.py::test_parse_args'
    assert args.numbers == 1
    assert args.output is None
    assert args._print == False

def test_execute():
    run = execute()
    assert run.cur == ''