#!/usr/local/bin python
#-*-coding: utf-8-*-

from openpyxl import load_workbook
import xlx
import myx
from public import get_para_dic

class MetaInfo(object):
    url = ""
    cate_1 = ""
    cate_2 = ""
    cate_3 = ""
    cate_4 = ""
    cate_5 = ""
    desc = ""
    area = ""
    unit = ""
    sect = ""
    updateWay = ""
    updatePeriod = ""
    getWay = ""
    share = ""
    year = ""

    def __init__(self, dic):
        if "url" in dic:
            self.url = dic["url"]
        
        if "cate_1" in dic:
            self.cate_1 = dic["cate_1"]

        if "cate_2" in dic:
            self.cate_2 = dic["cate_2"]

        if "cate_3" in dic:
            self.cate_3 = dic["cate_3"]

        if "cate_4" in dic:
            self.cate_4 = dic["cate_4"]

        if "cate_5" in dic:
            self.cate_5 = dic["cate_5"]

        if "desc" in dic:
            self.desc = dic["desc"]

        if "area" in dic:
            self.area = dic["area"]

        if "unit" in dic:
            self.unit = dic["unit"]

        if "sect" in dic:
            self.sect = dic["sect"]

        if "updateWay" in dic:
            self.updateWay = dic["updateWay"]

        if "updatePeriod" in dic:
            self.updatePeriod = dic["updatePeriod"]

        if "getWay" in dic:
            self.getWay = dic["getWay"]

        if "share" in dic:
            self.share = dic["share"]

        if "year" in dic:
            self.year = dic["year"]

    def show(self):
        print("%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s" % (
            self.url, self.cate_1, self.cate_2, self.cate_3, self.cate_4, self.cate_5, 
            self.desc, self.area, self.unit, self.sect, self.updateWay, self.updatePeriod, 
            self.getWay, self.share, self.year
        ))

def metadata_update(conf):
    configs = conf.items("Metadata_Update")
    paraDic = get_para_dic(configs)
    #print(paraDic)

    print("【更新元数据】\n")

    print("功能参数如下：\n")
    for config in configs:
        print("\t%s: %s" % (config[0], config[1]))
    print("\n")

    opt = input("$ 是否执行？（y/n） ")

    if opt != "y" and opt != "Y":
        return 0

    try:
        wb = load_workbook(conf["Metadata_Update"]["metadata_xlsx"])
        #print("open file success")
    except Exception as e:
        print(e)
        return 0

    #print(conf["Metadata_Update"]["metadata_worksheet"])

    try:
        sheet = wb[conf["Metadata_Update"]["metadata_worksheet"]]
        #print("open sheet success")
    except Exception as e:
        print(e)
        return 0

    #print("success")
    try:
        rowStart = int(paraDic["metadata_row_start"])
        rowEnd = int(paraDic["metadata_row_end"])
    except Exception as e:
        print(e)
        return 0

    metaInfos = list()

    for row in sheet.rows:
        for cell in row:
            cell.value = xlx.getRealCellValue(sheet, cell)

    for r in range(rowStart, rowEnd + 1):
        dic = dict()

        dic["url"] = str(sheet["%s%s" % (paraDic["col_url"], r)].value).strip()
        dic["cate_1"] = str(sheet["%s%s" % (paraDic["col_category_1"], r)].value).strip()
        dic["cate_2"] = str(sheet["%s%s" % (paraDic["col_category_2"], r)].value).strip()
        dic["cate_3"] = str(sheet["%s%s" % (paraDic["col_category_3"], r)].value).strip()
        dic["cate_4"] = str(sheet["%s%s" % (paraDic["col_category_4"], r)].value).strip()
        dic["cate_5"] = str(sheet["%s%s" % (paraDic["col_category_5"], r)].value).strip()
        dic["desc"] = str(sheet["%s%s" % (paraDic["col_description"], r)].value).strip()
        dic["area"] = str(sheet["%s%s" % (paraDic["col_area"], r)].value).strip()
        dic["unit"] = str(sheet["%s%s" % (paraDic["col_unit"], r)].value).strip()
        dic["sect"] = str(sheet["%s%s" % (paraDic["col_section"], r)].value).strip()
        dic["updateWay"] = str(sheet["%s%s" % (paraDic["col_update_way"], r)].value).strip()
        dic["updatePeriod"] = str(sheet["%s%s" % (paraDic["col_update_period"], r)].value).strip()
        dic["getWay"] = str(sheet["%s%s" % (paraDic["col_get_way"], r)].value).strip()
        dic["share"] = str(sheet["%s%s" % (paraDic["col_share"], r)].value).strip()
        dic["year"] = str(sheet["%s%s" % (paraDic["col_year"], r)].value).strip()

        metaInfo = MetaInfo(dic)
        #metaInfo.show()

        if metaInfo.url != "" and metaInfo.url != "None":
            metaInfos.append(metaInfo)

    num = len(metaInfos)

    print("共提取到%s条带服务地址URL的元数据信息\n" % num)

    print("连接数据库 %s@%s:%s/%s ...\n" % (
        paraDic["db_user"], paraDic["db_host"], paraDic["db_port"], paraDic["db_database"]
    ))

    try:
        db = myx.MyConnect(paraDic["db_database"], paraDic["db_user"], paraDic["db_password"], paraDic["db_host"], paraDic["db_port"])
    except Exception as e:
        print(e)
        return 0

    print("数据库连接成功\n")

    ct = 0

    for metaInfo in metaInfos:
        ct += 1
        print("正在处理第%s条元数据信息...\n" % ct)

        print("\turl: %s" % metaInfo.url)

        sql = """
select resource_id from gt_res_capable 
where url = '%s'
        """ % metaInfo.url

        try:
            db.execute(sql)
        except Exception as e:
            print(e)
            return 0
        
        row = db.getOne()

        resc_id = ""

        if row != None:
            resc_id = row[0]

        print("\tresc_id = %s" % resc_id)

        sqlTmp = """
select id from gt_catalog
where type = 'RESC'
and title = '<para>'
        """

        onFlag = True

        cate_id = paraDic["default_cate_id"]

        if (len(metaInfo.cate_5) >= 2) and (onFlag == True):
            sql = sqlTmp.replace('<para>', metaInfo.cate_5)
            try:
                db.execute(sql)
            except Exception as e:
                print(e)
                return 0

            
            row = db.getOne()

            flag = True

            if row == None:
                flag = False
            
            if flag == True:
                cate_id = row[0]
                onFlag = False

        if (len(metaInfo.cate_4) >= 2) and (onFlag == True):
            sql = sqlTmp.replace('<para>', metaInfo.cate_4)
            try:
                db.execute(sql)
            except Exception as e:
                print(e)
                return 0

            
            row = db.getOne()

            flag = True

            if row == None:
                flag = False
            
            if flag == True:
                cate_id = row[0]
                onFlag = False

        if (len(metaInfo.cate_3) >= 2) and (onFlag == True):
            sql = sqlTmp.replace('<para>', metaInfo.cate_3)
            try:
                db.execute(sql)
            except Exception as e:
                print(e)
                return 0

            
            row = db.getOne()

            flag = True

            if row == None:
                flag = False
            
            if flag == True:
                cate_id = row[0]
                onFlag = False

        if (len(metaInfo.cate_2) >= 2) and (onFlag == True):
            sql = sqlTmp.replace('<para>', metaInfo.cate_2)
            try:
                db.execute(sql)
            except Exception as e:
                print(e)
                return 0

            
            row = db.getOne()

            flag = True

            if row == None:
                flag = False
            
            if flag == True:
                cate_id = row[0]
                onFlag = False

        if (len(metaInfo.cate_1) >= 2) and (onFlag == True):
            sql = sqlTmp.replace('<para>', metaInfo.cate_1)
            try:
                db.execute(sql)
            except Exception as e:
                print(e)
                return 0

            
            row = db.getOne()

            flag = True

            if row == None:
                flag = False
            
            if flag == True:
                cate_id = row[0]
                onFlag = False

        sqlTmp = """
select id from gt_catalog
where type = 'XZJG'
and title = '<para>'
        """

        onFlag = True

        sect_id = paraDic["default_sect_id"]

        if (len(metaInfo.sect) >= 2) and (onFlag == True):
            sql = sqlTmp.replace('<para>', metaInfo.sect)
            try:
                db.execute(sql)
            except Exception as e:
                print(e)
                return 0

            
            row = db.getOne()

            flag = True

            if row == None:
                flag = False
            
            if flag == True:
                sect_id = row[0]
                onFlag = False

        print("\tcate_id = %s, sect_id = %s\n" % (
            cate_id, sect_id
        ))

        print("\t重建gt_cat_res_ref关系...")

        sql = "delete from gt_cat_res_ref where resource_id = '%s'" % resc_id

        try:
            db.execute(sql)
            db.commit()
        except Exception as e:
            print(e)
            return 0
        
        sql = "insert into gt_cat_res_ref values ('%s', '%s')" % (cate_id, resc_id)

        try:
            db.execute(sql)
            db.commit()
        except Exception as e:
            print(e)
            return 0

        sql = "insert into gt_cat_res_ref values ('%s', '%s')" % (sect_id, resc_id)

        try:
            db.execute(sql)
            db.commit()
        except Exception as e:
            print(e)
            return 0

        print("\tgt_cat_res_ref关系重建完成\n")

        print("\t更新发布机构名称...")

        sql = "select title from gt_catalog where id = '%s'" % sect_id

        try:
            db.execute(sql)
            #db.commit()
        except Exception as e:
            print(e)
            return 0

        row = db.getOne()

        sql = "select responsible_id from gt_resource where id = '%s'" % resc_id

        try:
            db.execute(sql)
            #db.commit()
        except Exception as e:
            print(e)
            return 0

        row1 = db.getOne()

        if row != None and row1 != None:
            sect_name = row[0]
            resp_id = row1[0]

            sql = """
update gt_responsible
set orgnization_name = '%s'
where id = '%s'            
            """ % (sect_name, resp_id)

            try:
                db.execute(sql)
                db.commit()
            except Exception as e:
                print(e)
                return 0

        print("\t发布机构名称更新完成\n")