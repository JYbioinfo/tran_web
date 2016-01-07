#! /usr/bin/env python
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
listShow_html = "listShow.html"
list_html = "list.html"
login_html = "sign.html"



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
    pw = current_user.passwd_enc
    data = json.dumps({"account": account, "password": pw})
    result = json.loads(requests.get(API_service+"/api/tasks/list/", data=data).text)
    task_list = []
    for item in result["data"]:
        task_list.append(item)
    return render_template(list_html, task_list=task_list)


@list_view.route("/tasks/<int:sys_no>", methods=["GET", "PUT"])
@login_required
def get_task_detail(sys_no):
    account = current_user.account
    pw = current_user.passwd_enc
    data = json.dumps({"account": account, "password": pw})
    result = json.loads(requests.get(API_service+"/api/tasks/%d/" % sys_no, data=data).text)
    info = result["data"]
    return render_template(listShow_html, info=info)


@list_view.route("/tasks/<int:sys_no>/update", methods=["PUT", "POST"])
@login_required
def save_detail(sys_no):
    postdata = {}
    postdata["account"] = current_user.account
    postdata["password"] = current_user.passwd_enc
    postdata["disease_name_zn"] = request.form.get("disease_name_zn", "")
    postdata["text_zn"] = request.form.get("text_zn", "")
    postdata["flag"] = int(request.form.get("flag", 0))
    result = json.loads(requests.put(API_service+"/api/tasks/%d/" % sys_no, data=json.dumps(postdata)).text)
    if result["status"] == u'success!':
        if postdata["flag"] == 0:
            return redirect("/tasks/%d" % sys_no)
        else:
            return redirect("/tasks")


