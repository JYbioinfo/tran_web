#! /usr/bin/python
# encoding: utf-8
__author__ = 'yangrui'

from hashlib import sha256
from hmac import HMAC
import binascii
from Mysql_db import DB
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

db = None
try:
    db = DB()
    db.connect()
except Exception, e:
    print e


def HmacPasswd(passwd):
    salt = "secmsg"
    if isinstance(passwd, unicode):
        passwd = passwd.encode('UTF-8')
    for i in xrange(11):
        HmacPassword = HMAC(passwd, salt, sha256).digest()
    return binascii.b2a_hex(HmacPassword)


def inser_into_passwd():
    account = "yangrui"
    passwd = "yangrui"
    hmacPasswd = HmacPasswd(passwd)
    print hmacPasswd
    sql_new = "INSERT INTO account_for_disease (account,password) VALUES ('%s', '%s');"% (account, hmacPasswd)
    #args = (account, hmacPasswd)
    db.execute(sql_new)

def test():
    passwd = "yangrui"
    account = "yangrui"
    sql = "SELECT password from account_for_disease where account='%s';" % account
    db.execute(sql)
    data = db.fetchall()
    print data
    hmacPasswd = HmacPasswd(passwd)
    print hmacPasswd
    if hmacPasswd == data[0][0]:
        print 'ok'


