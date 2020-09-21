#!/usr/local/bin python
#-*-coding: utf-8-*-

from public import get_para_dic
import webbrowser

def url_direct(conf):
    configs = conf.items("URLs")
    paraDic = get_para_dic(configs)

    urlList = list()
    ct = 0

    for para in paraDic:
        ct += 1
        d = dict()
        d["num"] = str(ct)
        d["name"] = para
        d["url"] = paraDic[para]
        urlList.append(d)

    print("【常用地址导览】\n")

    for url in urlList:
        print("\t【%s】%s" % (url["num"], url["name"]))

    print("\n")
    opt = input("$ 请输入需要跳转的系统地址 ")
    flag = False

    for url in urlList:
        if opt.strip() == url["num"]:
            flag = True
            webbrowser.open(url["url"])
            break
    
    return 0