#!/usr/local/bin python
#-*-coding: utf-8-*-

import sshx
from public import get_para_dic

def client(host, cmd):
    print("正在连接服务器%s ...\n" % (host["host"]))
    s = sshx.SSHConnection(host)
    try:
        s.connect()
        print("服务器连接成功")
    except Exception as e:
        print("服务器连接失败：%s\n" % e)
        return 0

    try:
        s.execute(cmd)
        print("功能执行成功\n")
    except Exception as e:
        print("功能执行失败：%s\n" % e)

    s.close()

    return 0


def nfs_manage(conf):
    configs = conf.items("NFS_Management")
    paraDic = get_para_dic(configs)
    host = dict()
    host["host"] = paraDic["host"]
    host["port"] = int(paraDic["port"])
    host["username"] = paraDic["username"]
    host["password"] = paraDic["password"]

    print("【管理NFS服务器】\n")
    for config in configs:
        print("\t%s: %s" % (config[0], config[1]))
    print("\n")

    print("\t【1】启动\n\t【2】停止\n\t【3】重启\n")

    opt = input("$ 请输入需要执行的功能 ")

    if opt.strip() == "1":
        cmd = "service nfs start"
        client(host, cmd)
        return 0
    elif opt.strip() == "2":
        cmd = "service nfs stop"
        client(host, cmd)
        return 0
    elif opt.strip() == "3":
        cmd = "service nfs restart"
        client(host, cmd)
        return 0
    else:
        cmd = "pwd"
        client(host, cmd)
        return 0

    