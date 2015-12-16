# -*- coding: utf-8 -*-
# Create Date 2015/12/9
import json
from flask import Blueprint, request
from tools.Mysql_db import DB
from tools import insertpasswd as PWD
task_api = Blueprint("task_api",__name__)
db = None
try:
    db = DB()
    db.connect()
except Exception, e:
    print e


@task_api.route('/hmacpasswd/', methods=['POST'])
def get_hmacpasswd():
    try:
        postdata = json.loads(request.data)
        hmacp = PWD.HmacPasswd(postdata["passwd"])
        print hmacp
        return hmacp
    except Exception, e:
        print e.args
        return json.dumps({"status": 702, "message": e.args})


@task_api.route('/userconfirm/', methods=['POST'])
def user_confirm():
    try:
        postdata = json.loads(request.data)
        account = postdata["account"]
        passwd = postdata["passwd"]
        sql = "SELECT password FROM account_for_disease WHERE account='%s';" % account
        result = db.execute(sql)
        if result == 0:
            return json.dumps({"status": 102, "message": "Account Not Exist!"})
        re_det_pro = db.fetchall()
        password = re_det_pro[0][0]
        print password
        if password != passwd:
            return json.dumps({"status": 102, "message": "Password Error!"})
        return json.dumps({"status": 002, "message": "User confirmed"})
    except Exception, e:
        return json.dumps({"status": 703, "message": e.args})


@task_api.route("/tasks/",methods=["GET"])
def get_task_list():
    return json.dumps({"status":"hello world!"})

def user_affirm(account, password):
    user_flag = 0
    check_sql = "SELECT * FROM account_for_disease WHERE account = '%s' AND password = '%s';" \
                % (account, password)
    re = db.execute(check_sql)
    if re > 0:
        user_flag = 1
    else:
        user_flag = 0
    return user_flag

@task_api.route("/tasks/list/",methods=["GET"])
def task_list_get():
    try:
        postdata = json.loads(request.data)
        account = postdata["account"]
        password = postdata["password"]
        if type(account) != str and type(account) != unicode and len(account) <= 0:
            return json.dumps({"status":"403, account"})
        if type(password) != str and type(password) != unicode and len(password) <= 0:
            return json.dumps({"status":"403, account"})
        user_flag = user_affirm(account,password)
        if user_flag == 0:
            return json.dumps({"status":"user not exit"})
        select_sql = "SELECT sys_no,disease_id,disease_name,disease_name_zn " \
                     "FROM disease_detail WHERE flag = 0 AND available = 0 limit 0,100;"
        re = db.execute(select_sql)
        if re > 0:
            result = db.fetchall()
        else:
            return json.dumps({"status":"failed get list"})
        task_list = []
        for item in result:
            dict1 = {}
            sys_no,disease_id,disease_name,disease_name_zn = item
            set_sql = "UPDATE disease_detail SET available = 1 WHERE sys_no = %d;" % sys_no
            re = db.execute(set_sql)
            dict1["sys_no"] = sys_no
            dict1["disease_id"] = disease_id
            dict1["disease_name"] = disease_name
            dict1["disease_name_zn"] = disease_name_zn
            task_list.append(dict1)
        return json.dumps({"status":"success!","data":task_list})
    except Exception,e:
        print str(e)
        return json.dumps({"status": 701, "message": "Internal error %s" % str(e)})


@task_api.route("/tasks/<int:sys_no>/",methods=["GET"])
def disease_info_get(sys_no):
    try:
        postdata = json.loads(request.data)
        account = postdata["account"]
        password = postdata["password"]
        if type(account) != str and type(account) != unicode and len(account) <= 0:
            return json.dumps({"status":"403, account"})
        if type(password) != str and type(password) != unicode and len(password) <= 0:
            return json.dumps({"status":"403, account"})
        user_flag = user_affirm(account,password)
        if user_flag == 0:
            return json.dumps({"status":"user not exit"})
        select_sql = "SELECT disease_id,disease_name,disease_name_zn,text,text_zn,flag " \
                     "FROM disease_detail WHERE sys_no = %d;" % sys_no
        re = db.execute(select_sql)
        if re > 0:
            result = db.fetchone()
            disease_id,disease_name,disease_name_zn,text,text_zn,flag = result
        else:
            return json.dumps({"status":"failed get disease info"})
        disease_info = {}
        disease_info["disease_id"] = disease_id
        disease_info["disease_name"] = disease_name
        disease_info["disease_name_zn"] = disease_name_zn
        disease_info["text"] = text
        disease_info["text_zn"] = text_zn
        disease_info["flag"] = flag
        disease_info["sys_no"] = sys_no
        return json.dumps({"status":"success!","data":disease_info})
    except Exception,e:
        print str(e)
        return json.dumps({"status": 701, "message": "Internal error %s" % str(e)})

@task_api.route("/tasks/<int:sys_no>/",methods=["PUT"])
def disease_info_update(sys_no):
    try:
        postdata = json.loads(request.data)
        account = postdata["account"]
        password = postdata["password"]
        if type(account) != str and type(account) != unicode and len(account) <= 0:
            return json.dumps({"status":"403, account"})
        if type(password) != str and type(password) != unicode and len(password) <= 0:
            return json.dumps({"status":"403, account"})
        user_flag = user_affirm(account,password)
        if user_flag == 0:
            return json.dumps({"status":"user not exit"})
        disease_name_zn = postdata.get("disease_name_zn")
        text_zn = postdata.get("text_zn")
        flag = postdata.get("flag")
        if disease_name_zn is None:
            disease_name_zn = "N\A"
        if text_zn is None:
            text_zn = "N\A"
        if flag is None:
            flag = 0
        update_sql = "UPDATE disease_detail SET disease_name_zn = '%s',text_zn = '%s',flag = %d " \
                     "WHERE sys_no = %d;" % (disease_name_zn,text_zn,flag,sys_no)
        re = db.execute(update_sql)
        if re > 0:
            postdata.pop("account")
            postdata.pop("password")
            postdata["sys_no"] = sys_no
            return json.dumps({"status":"success!","data":postdata})
        else:
            return json.dumps({"status":"failed to update"})
    except Exception,e:
        print str(e)
        return json.dumps({"status": 701, "message": "Internal error %s" % str(e)})


@task_api.route("/tasks/reset/",methods=["PUT"])
def reset_available():
    try:
        postdata = json.loads(request.data)
        account = postdata["account"]
        password = postdata["password"]
        if type(account) != str and type(account) != unicode and len(account) <= 0:
            return json.dumps({"status":"403, account"})
        if type(password) != str and type(password) != unicode and len(password) <= 0:
            return json.dumps({"status":"403, account"})
        user_flag = user_affirm(account,password)
        if user_flag == 0:
            return json.dumps({"status":"user not exit"})
        sys_no_list = postdata.get("sys_no_list")
        if sys_no_list is None:
            return json.dumps({"status":"403, sys_no_list not exit"})
        elif type(sys_no_list) != list:
            return json.dumps({"status":"403, sys_no_list need list"})
        failed_list = []
        for sys_no in sys_no_list:
            reset_sql = "UPDATE disease_detail SET available = 0 WHERE sys_no = %d;" % sys_no
            re = db.execute(reset_sql)
            if re == 0:
                failed_list.append(sys_no)
        return json.dumps({"status": "success!", "data": {"failed":failed_list}})
    except Exception,e:
        print str(e)
        return json.dumps({"status": 701, "message": "Internal error %s" % str(e)})





