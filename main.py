#!/usr/local/bin python
#-*-coding: utf-8-*-

import os
import configparser as cp
import metadata_update as mu
import nfs_man as nm
import browse
import geojsonWkt

class Main(object):
    def __init__(self):
        self.conf = cp.ConfigParser()
        self.conf.read("config.ini", encoding="utf-8")

        print("***********************************************")
        print("************EasyOM ToolBox for JCPT************")
        print("***********************************************\n")
        print("****************************作者：戎晨飞 版本：1.0\n\n")

        os.system("pause")

        self.show_funcs()

    def close_proc(self):
        os.system("pause")

    def reselect_func(self):
        opt = input("$ 是否需要返回主菜单（y/n） ")

        if opt == "y" or opt == "Y":
            self.show_funcs()
        else:
            self.close_proc()

    def show_funcs(self):
        funcs = {
            "1" : "更新元数据", 
            "2" : "管理NFS服务器",
            "3" : "常用地址导览",
            "4" : "GeoJSON转WKT格式",
            "99" : "退出"
        }

        print("当前程序提供以下功能：\n")

        for func in funcs:
            print("\t【%s】%s" % (func, funcs[func]))

        print("\n")

        self.enter_func()

    def enter_func(self):
        opt = input("$ 请输入需要使用的功能代码 ")

        if opt == "1":
            mu.metadata_update(self.conf)
        elif opt == "2":
            nm.nfs_manage(self.conf)
        elif opt == "3":
            browse.url_direct(self.conf)
        elif opt == "4":
            geojsonWkt.geojson2Wkt()
        elif opt == "99":
            pass
        else:
            print("无效的输入！\n")
            
        self.reselect_func()