#!/usr/local/bin python
#-*-coding: utf-8-*-

import nfs_man
import configparser as cp
from public import get_para_dic
import datetime
import threading

def func():
    now = datetime.datetime.now()
    now_str = str(now)
    res = now_str[:19]
    print("\n【%s】" % res)

    conf = cp.ConfigParser()
    conf.read("config.ini", encoding="utf-8")

    configs = conf.items("NFS_Management")
    paraDic = get_para_dic(configs)
    host = dict()
    host["host"] = paraDic["host"]
    host["port"] = int(paraDic["port"])
    host["username"] = paraDic["username"]
    host["password"] = paraDic["password"]
    interval = paraDic["restart_interval"]

    cmd = "service nfs restart"
    nfs_man.client(host, cmd)

    timer = threading.Timer(1800, func)
    timer.start()

print("****************NFS服务自动重启工具****************")
print("\t\tv1.1 by Chenfei Jovany Rong")
