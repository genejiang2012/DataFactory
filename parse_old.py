# !/usr/bin/env python3 
# -*- coding: utf-8 -*-
# @Time    : 2022/10/25 15:58
# @Author  : Gene Jiang
# @File    : parse_old.py.py
# @Description:

import sys
import os
import codecs
import re
import csv
import json


def parse_file(src_file, key_word, file_code='utf-8'):
    """
    parse the file
    """
    regex = re.compile(key_word)

    # the path for the output file
    dir_name = os.path.dirname(src_file)
    print(src_file, dir_name)

    new_file_name = os.path.splitext(os.path.basename(src_file))[0] \
                    + '_{}.csv'.format(key_word)
    # new_file = dir_name + os.sep + new_file_name
    # print(new_file)

    # read the source file and write to the detest file

    with codecs.open(src_file, 'r', encoding='utf-8') as fr, \
            codecs.open(new_file_name, 'w', encoding='utf-8') as fw:
        flag = 1
        while True:
            line = fr.readline()
            if not line:
                break
            line = line.strip()
            # print(line)
            # print(line.count(key_word))

            if line.count(key_word) == 1:
                if flag == 1:
                    title = "{} `(".format(key_word)

                    header_line = line.split(key_word)[-1].split("` (`")[-1].split("`)")[0] + "\n"
                    print(header_line)

                    fw.write(header_line.replace('`', ''))
                    # fw.write(header_line)
                    flag = 0
                new_line = line.split('VALUES (')[-1].split(");")[0] + "\n"

                fw.write(new_line.replace("\'", "").replace('(', '').replace(')', ''))
                # fw.write(new_line)

    print('Done')

def gen_pg_sql(src_file, key_word, index_first, index_second,file_code='utf-8'):
    """
    parse the file
    """
    regex = re.compile(key_word)

    # the path for the output file
    dir_name = os.path.dirname(src_file)
    print(src_file, dir_name)

    new_file_name = os.path.splitext(os.path.basename(src_file))[0] \
                    + '_{}_pg.csv'.format(key_word)
    # new_file = dir_name + os.sep + new_file_name
    # print(new_file)

    # read the source file and write to the detest file

    with codecs.open(src_file, 'r', encoding='utf-8') as fr, \
            codecs.open(new_file_name, 'w', encoding='utf-8') as fw:
        flag = 1
        while True:
            line = fr.readline()
            if not line:
                break
            line = line.strip()
            # print(line)
            # print(line.count(key_word))

            if line.count(key_word) == 1:
                # if flag == 1:
                #     title = "{} `(".format(key_word)
                #
                #     header_line = line.split(key_word)[-1].split("` (`")[-1].split("`)")[0] + "\n"
                #     print(header_line)
                #
                #     fw.write(header_line.replace('`', ''))
                #     # fw.write(header_line)
                #     flag = 0
                first_part = line.split('VALUES (')[0]
                new_line = line.split('VALUES (')[-1].split(");")[0] + "\n"

                replace_line = new_line.replace("\'", "").replace('(', '').replace(')', '')

                latest_line =  'INSERT INTO ' + key_word + ' VALUES (' + deal_with_col(replace_line, ',', index_first, index_second).replace("\'array", 'array').replace(']\'', ']') + ');' + '\n'

                fw.write(latest_line)
                # fw.write(new_line)

    print('Done')

def deal_with_col(line: str, separator=',', index_first=2, index_second=7):
    col_array = line.split(separator)
    for index, elem in enumerate(col_array):
        # if elem.find('|') > 0:
        if index == index_first or index == index_second:
            if elem.find('|') > 0:
                elem_sub_array = elem.strip('\n').split('|')
            # print(elem_sub_array)
                new_elem = 'array{}'.format(elem_sub_array)
            else:
                new_elem = 'array[\'{}\']'.format(elem)
            # print(new_elem)
            col_array[index] = new_elem
    return ', '.join(["\'{}\'".format(i) for i in col_array]).strip('\n')


def csv2json(src_file, dst_file):
    with codecs.open(src_file, 'r', encoding='utf-8') as fr, \
            codecs.open(dst_file, 'w', encoding='utf-8') as fw:
        tmp = csv.DictReader(fr)
        for element in tmp:
            dict = {}

            for k, v in element.items():
                dict[k] = v
                json_format = json.dumps(dict, ensure_ascii=False) + "|\n"
                print(json_format)

            fw.write(json_format)


if __name__ == '__main__':
    # for item in ['C_Member', 'leads', 'C_wechat', 'C_Dept', 'C_adviser',
    #              'event_leads_distribution', 'event_followup',
    #              'event_invitation', 'event_prd_test', 'event_sale_order',
    #              'C_order']:
    #     parse_file('adviser_cep.csv', item)

    # for item in ['wechatfans']:
    #     gen_pg_sql('mock_huaxi.csv', item, 4, 5)

    for item in ['crm_member', 'wechatfans']:
        parse_file('mock_huaxi.csv', item)
    # parse_file('crm_std.csv', 'crm_action')
    # parse_file('C_new_order.csv', 'C_order')
    # parse_file('media.csv', 'C_order')
    # csv2json("adviser_cep_400_event_sale_order.csv",
    #          "adviser_cep_400_event_sale_order_json.csv")







