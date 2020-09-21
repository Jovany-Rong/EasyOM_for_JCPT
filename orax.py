#!/usr/local/bin python
#coding: utf-8

#import psycopg2 as pg
import cx_Oracle as ora

class OraConnect(object):
    def __init__(self, database, user, password, host, port):
        self.sid = "%s@%s:%s/%s" % (user, host, port, database)
        self._sid = "%s/%s@%s:%s/%s" % (user, password, host, port, database)
        try:
            self._conn = ora.connect(self._sid)
            self._cur = self._conn.cursor()
            self.user = user
        except Exception as e:
            print(e)
            self.close()

    def close(self):
        try:
            self._cur.close()
            self._conn.close()
        except:
            pass

    def __del__(self):
        self.close()

    def execute(self, sql):
        self._cur.execute(sql)

    def commit(self):
        self._conn.commit()

    def getOne(self):
        return self._cur.fetchone()

    def result(self):
        return self._cur.fetchall()

    #def fields(self):
        #return self._cur.description

    def tables(self, owner=''):
        if owner == '':
            owner = self.user.upper()
        sql = """
select table_name from all_tab_comments where owner = '%s'  and table_type = 'TABLE'
        """ % (owner)

        self.execute(sql)
        rows = self.result()
        l = list()
        for row in rows:
            l.append(row[0])

        return l

    def table_structure(self, table, owner=''):
        if owner == '':
            owner = self.user.upper()
        sql = """
select a.column_name name, a.data_type || '(' || a.data_length || ')' type, 
case when a.nullable = 'N' then 'yes' else 'no' end is_not_null, b.comments comments
   from all_tab_cols a 
   left join all_col_comments b on b.owner = a.owner and b.TABLE_NAME = a.table_name and b.column_name = a.column_name
   where a.owner = '%s' and a.table_name = '%s'
        """ % (owner, table)

        self.execute(sql)
        rows = self.result()
        return rows

if __name__ == "__main__":
    conn = OraConnect('orcl', 'om', 'gtis', '192.168.0.25', '1521')
    l = conn.table_structure('OM_TOMCATINFO')
    print(l)
    del conn