#! /usr/bin/env python
# coding: utf-8
__author__ = 'wubo'
# 2016/2/18 0018
import smtplib,thread,time
from datetime import datetime
from Mysql_db import DB
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
EMAIL_SERVER = "ym.163.com"
USER = "admin@gene.ac"
PASSWD = "Bdcbdc123456"
# USER = "wubo@gene.ac"
# PASSWD = "1993wb1116"
encoding = 'utf-8'
TO_ADDR_LIST = ["wubo@gene.ac", "budechao@gene.ac", "lixiyuan@gene.ac"]
# TO_ADDR_LIST = ["wubo@gene.ac"]
db = DB()


def db_status():
    flag_dic = { 0: "未分配", 1: "已分配未翻译", 2: "正在翻译", 3: "已提交未审核", 4: "已审核", 99: "检查重复中"}
    result_dic = {}
    get_sql = "select flag,count(sys_no) from disease_detail group by flag;"
    db.execute(get_sql)
    l = db.fetchall()
    for item in l:
        result_dic[flag_dic[item[0]]] = [item[1]]
    return result_dic


def company_status():
    company_list = ["shangcai", "baihang", "caijing", "chensiyao"]
    result_dic = {}
    for company in company_list:
        get_sql = "select sum(case when flag>0 then 1 else 0 end) as total, " \
                  "sum(case when flag>2 then 1 else 0 end) as subs, " \
                  "sum(case when flag=4 then 1 else 0 end) as mark, " \
                  "avg(case when flag=4 then cast(score as unsigned) end) as av " \
                  "from disease_detail where account like '%s%%'  and flag <5;" % company
        db.execute(get_sql)
        result_dic[company] = []
        result_dic[company].extend(db.fetchone())
    return result_dic


def users_stats():
    result_dic = {}
    user_sql = "select account,sum(case when flag > 0 then 1 else 0 end) as total, " \
               "sum(case when flag > 2 then 1 else 0 end) as subs, " \
               "sum(case when flag =4 then 1 else 0 end) as mark, " \
               "avg(case when flag=4 then cast(score as unsigned) end) as av " \
               "from disease_detail where flag < 5 group by account;"
    db.execute(user_sql)
    l0 = db.fetchall()
    for item in l0:
        result_dic[item[0]] = [item[1], item[2], item[3], item[4]]
    return result_dic


def words_stats(account):
    pass


def dic2html(dic, heading=None,title_list=None):
    table = '<table border="1px" cellspacing="0px" style="border-collapse:collapse">'
    if heading:
        table += '<th>{head}</th>'.format(head=encoded(heading, encoding))
    if title_list:
        table += '<tr>'
        for title in title_list:
            table += '<td>{value}</td>'.format(value=encoded(title, encoding))
        table += '</tr>'
    for k,v in dic.items():
        table += '<tr>'
        table += '<td>{value}</td>'.format(value=encoded(k, encoding))
        for item in v:
            if item is int:
                table += '<td>%s</td>' % item
            else:
                table += '<td>{value}</td>'.format(value=encoded(item,encoding))
        table += '</tr>'
    return table


def encoded(s,encoding):
    return s.encode(encoding) if isinstance(s, unicode) else s


def send_email(subject,content,to):
    try:
        smtp = smtplib.SMTP("smtp.%s" % EMAIL_SERVER, 25)
        smtp.starttls()
        smtp.login(USER, PASSWD)
        user = '{nick_name} <{user}>'.format(nick_name=encoded("翻译系统",encoding), user=USER)
        msg = MIMEMultipart('alternative')
        msg['From'] = user
        msg['To'] = encoded(to, encoding)
        msg['Subject'] = Header(encoded(subject, encoding), encoding)
        msg.attach(MIMEText(encoded(content, encoding), "html", encoding))
        smtp.sendmail(user, to, msg.as_string())
        smtp.quit()
        print "send success"
        return True
    except Exception, e:
        error_message = "MyEmailManager send_mail error %s" % str(e.args)
        print(error_message)
        return False


def thread_to_send(subject, content, to):
    return thread.start_new_thread(send_email, (subject, content, to))

if __name__ == '__main__':
    subject = "翻译系统状态"
    nowtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    content = "<html><body>统计时间: "+nowtime+"<br>系统邮件，请不要回复<br>"
    content += dic2html(db_status(), "数据库概况")
    content += "<br><br>"
    content += dic2html(company_status(), "已提交翻译情况",["翻译方", "共分配","已提交","已审核","平均得分"])
    content += "<br><br>"
    content += dic2html(users_stats(), "各账户翻译情况",["账户", "分配数","提交数","已审核数", "平均得分"])
    content += "<br><br></body></html>"
    for to in TO_ADDR_LIST:
        thread_to_send(subject, content, to)
    time.sleep(3)