#!/usr/local/bin python
#coding: utf-8

import pgx

pg = pgx.PgConnect('njcgkcoregis', 'njcgkcoregis', 'njcgkcoregis', '192.168.192.66', 30533)
#tables = pg.tables('njcgknocoregis')

sql = """select 'select UpdateGeometrySRID(''' || f_table_name || ''', ''' || f_geometry_column || ''', 45281);'
from geometry_columns
where srid != 45281"""

pg.execute(sql)

sqlList = pg.result()

#print(result)
num = len(sqlList)

i = 0

for sqlT in sqlList:
    sql = sqlT[0]
    i += 1
    try:
        pg.execute(sql)
        pg.commit()
    except Exception as e:
        print(e)
        print(sql)
        break

    print("%s / %s done. (%s)" % (i, num, sql))