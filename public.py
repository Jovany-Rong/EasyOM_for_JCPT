#!/usr/local/bin python
#-*-coding: utf-8-*-

def get_para_dic(configs):
    dic = dict()

    for config in configs:
        dic[config[0]] = config[1]

    return dic