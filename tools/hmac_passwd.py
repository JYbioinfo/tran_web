#! /usr/bin/env python
# coding: utf-8
from tools.Mysql_db import DB
from hashlib import sha256
from hmac import HMAC
import binascii, sys

class HmacPasswd:

    def __init__(self, passwd):
        salt = "secmsg" #用于hash的密钥，可改为其他固定值
        if isinstance(passwd, unicode):
            passwd = passwd.encode('UTF-8')
        for i in xrange(11):
            self.HmacPassword = HMAC(passwd, salt, sha256).digest()

    def get_hmacpassed(self):
        return binascii.b2a_hex(self.HmacPassword)


def insert_user(account,password,user_right):
    db = DB()
    passwd = HmacPasswd(password).get_hmacpassed()
    select_sql = "SELECT max(user_no) FROM account_for_disease;"
    re = db.execute(select_sql)
    user_no = db.fetchone()[0] + 1
    insert_sql = "INSERT INTO account_for_disease (user_no,account,password,user_right) " \
                 "VALUES ('%s','%s','%s','%s');" % (user_no,account,passwd,user_right)
    db.execute(insert_sql)
    print "Insert Success"

if __name__ == '__main__':
    insert_user("wubo","admin",0)