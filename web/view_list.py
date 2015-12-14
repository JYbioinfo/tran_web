# -*- coding: utf-8 -*-
# Create Date 2015/12/10
__author__ = 'wubo'
import requests,json
from tools.hmac_passwd import HmacPasswd
from flask import Blueprint, render_template, redirect, request, url_for
from web import API_service,User
from flask_login import login_user, login_required, current_user, logout_user, flash
from web.forms.login_form import LoginForm
list_view = Blueprint("list_view", __name__)
list_html = "list.html"
login_html = "sign.html"
detail_html = "listShow.html"



@list_view.route("/", methods=["GET", "PUT"])
def hello():
    return redirect("/tasks")


@list_view.route("/login", methods=["GET", "POST"])
def login():
    # return redirect(request.args.get("next") or "/tasks")
    form = LoginForm()
    if form.validate_on_submit():
        # login and validate the user...
        account = unicode.encode(form.account.data.decode())
        pw = HmacPasswd(form.passwd.data).get_hmacpassed()
        r = requests.post(API_service+"/api/user/check/", data=json.dumps({"account": account, "password": pw}))
        if r.status_code /100 == 2:
            res = json.loads(r.text)
            if res["status"] == 1:
                user = User()
                user.account = account
                user.passwd_enc = pw
                if form.remember_me.data:
                    login_user(user, remember=True)
                else:
                    login_user(user)
                flash(u"Logged in successfully.")
                return redirect(request.args.get("next") or "/tasks")
    return render_template(login_html, form=form)


@list_view.route("/logout")
def logout():
    logout_user()
    return redirect("/login")


@list_view.route("/tasks", methods=["GET", "PUT"])
@login_required
def get_task_list():
    account = current_user.account
    passwd = current_user.passwd_enc
    data = json.dumps({"account":account,"password":passwd})
    result = json.loads(requests.get(API_service+"/api/tasks/list/", data=data).text)
    task_list = []
    for item in result:
        task_list.append(item)
    return render_template(list_html, task_list=task_list)


@list_view.route("/tasks/<task_no>", methods=["GET", "PUT"])
@login_required
def get_task_detail(task_no):
    account = current_user.account
    passwd = current_user.passwd_enc
    data = json.dumps({"account": account, "password": passwd})
    result = json.loads(requests.get(API_service+"/api/tasks/%s/" % task_no, data=data).text)
    if result["status"] != u"success!":
         return redirect("/tasks")
    if type(result["data"]) is dict:
        detail_dic = result["data"]
    # {u'text': None, u'disease_id': None, u'flag': 0, u'disease_name': None, u'disease_name_zn': u'NA', u'sys_no': 1, u'text_zn': u'NA'}
    return render_template(detail_html, detail_dic=detail_dic)

