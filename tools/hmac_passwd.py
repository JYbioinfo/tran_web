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


def insert_user(account):
    db = DB()
    passwd = HmacPasswd(account).get_hmacpassed()
    insert_sql = "INSERT INTO account_for_disease(account,password) VALUES('%s','%s');" % (account,passwd)
    db.execute(insert_sql)
    print "Insert Success"

if __name__ == '__main__':
    insert_user(sys.argv[1])