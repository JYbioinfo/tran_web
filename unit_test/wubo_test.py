# -*- coding: utf-8 -*-
# Create Date 2015/12/14
__author__ = 'wubo'
import ConfigParser
import sys
from tools.Mysql_db import DB
db = DB()
def testConfig():
    config = ConfigParser.ConfigParser()
    config.read("../config.conf")
    env = config.get("Env", "env")
    h = config.get(env, "api_host")
    p = config.get(env, "api_port")
    print type(h)
    print h
    print type(p)
    print p
    API_service = "http://%s:%s" % (config.get(env, "api_host"), config.get(env, "api_port"))
    print type(API_service)


def test():
    sel_sql = "SELECT text FROM disease_detail limit 10;"
    db.execute(sel_sql)
    l = map(lambda s : s[0], db.fetchall())

if __name__ == '__main__':
    test()

    

