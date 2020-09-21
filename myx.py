#!/usr/local/bin python
#coding: utf-8

import pymysql as my

class MyConnect(object):
    def __init__(self, database, user, password, host, port):
        self._conn = my.connect(host=host, port=int(port), user=user, password=password, database=database)
        self._cur = self._conn.cursor()

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