#!/usr/local/bin python
#coding: utf-8

import psycopg2 as pg

class PgConnect(object):
    def __init__(self, database, user, password, host, port):
        self.sid = "%s@%s:%s/%s" % (user, host, port, database)
        self._conn = pg.connect(database=database, user=user, password=password, host=host, port=port)
        self._cur = self._conn.cursor()
        self.user = user

    def close(self):
        self._cur.close()
        self._conn.close()

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

    def fields(self):
        return self._cur.description

    def tables(self, schema='public'):
        sql = """
select tablename from pg_tables 
where tableowner = '%s' and schemaname = '%s'
        """ % (self.user, schema)

        self.execute(sql)
        rows = self.result()
        l = list()
        for row in rows:
            l.append(row[0])

        return l

    def table_structure(self, table):
        sql = """
select
	A.attname as name,
	format_type(A.atttypid, A.atttypmod) as type,
	case when A.attnotnull = 't' then 'yes' else 'no' end is_not_null,
	col_description(A.attrelid, A.attnum) as comment
from 
	pg_class as c,
	pg_attribute as a
where
	A.attrelid = c.oid
	and A.attnum > 0
	and C.relname = '%s'
        """ % (table)

        self.execute(sql)
        rows = self.result()
        return rows