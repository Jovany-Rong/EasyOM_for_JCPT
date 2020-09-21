#!/usr/local/bin python
#coding: utf-8

import pgx

pg = pgx.PgConnect('njcgkcoregis', 'njcgkcoregis', 'njcgkcoregis', '192.168.192.66', 30533)
#tables = pg.tables('njcgkcoregis')

sql = """select 'UPDATE ' || f_table_name || ' SET ' || f_geometry_column || ' = st_force2d(' || f_table_name || '.' || f_geometry_column || ');'
from geometry_columns"""

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