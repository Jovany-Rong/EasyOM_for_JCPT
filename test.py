#!/usr/local/bin python
#coding: utf-8

import pgx

pg66 = pgx.PgConnect('njdj_new', 'njdj_new', 'njdj_new', '192.168.192.66', '30998')

pg75 = pgx.PgConnect('njdj_new', 'njdj_new', 'njdj_new', '192.168.192.75', '30998')

print("connected.")

sql = "select smid from gh_m_jbntbhq order by smid asc"

pg66.execute(sql)
pg75.execute(sql)

rows66 = pg66.result()


rows75 = pg75.result()


ct = -1
while ct< 500000:
    print(ct)
    ct += 1
    if rows66[ct][0] != rows75[ct][0]:
        print(rows66[ct][0])
        break

