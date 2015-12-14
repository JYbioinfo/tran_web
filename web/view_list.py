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
    print request.method
    if form.validate_on_submit():
        # login and validate the user...
        print current_user.passwd_enc
        pw = HmacPasswd(form.passwd.data).get_hmacpassed()
        print pw
        if current_user.passwd_enc == pw:
            if form.remember_me.data:
                login_user(current_user, remember=True)
            else:
                login_user(current_user)
            flash(u"Logged in successfully.")
            return redirect(request.args.get("next") or "/tasks")
    return render_template(login_html, form=form)


@list_view.route("/logout")
def logout():
    logout_user()
    return redirect("/login")


@list_view.route("/tasks/list/", methods=["GET", "PUT"])
# @login_required
def get_task_list():
    # request_data = json.loads(request.data)
    # account = request_data["account"]
    # passwd = request_data["passwd"]
    # data = json.dumps({"account":account,"passwd":passwd})
    post_data = json.dumps({"account":"yangrui",
                        "password":"6320f9d341d76ae9c6bfda5f7b53471f74b0ce87d536f90a2c73f1fe78657f6f"})
    result = requests.get("http://127.0.0.1:7777/api/task/tasks/list/",data = post_data)
    info = json.loads(result.text)["data"]
    print info
    # result = json.loads(requests.get("http://127.0.0.1:7777/api/task/tasks/list/",data = post_data))
    print post_data
    # result = json.loads(requests.get(API_service+"/tasks/list/", data=post_data))
    task_list = []
    # print result
    for item in info:
        task_list.append(item)
    print task_list
    return render_template(list_html, task_list=task_list)


@list_view.route("/tasks/<int:sys_no>", methods=["GET", "PUT"])
# @login_required
def get_task_detail(sys_no):
    # request_data = json.loads(request.data)
    # account = request_data["account"]
    # passwd = request_data["passwd"]
    # data = json.dumps({"account": account, "passwd": passwd})
    post_data = json.dumps({"account":"yangrui",
                        "password":"6320f9d341d76ae9c6bfda5f7b53471f74b0ce87d536f90a2c73f1fe78657f6f"})
    result = requests.get("http://127.0.0.1:7777/api/task/tasks/%d/" % sys_no,data = post_data)
    info = json.loads(result.text)["data"]
    print info
    # result = json.loads(requests.get(API_service+"/tasks/sys_no/", data=data))
    info_list = []
    # for item in result:
    #     task_list.append(item)

    #---------------------------------------
    # for item in info.keys():
    #     info_list.append(info[item])
    # print info_list
    return render_template(listShow_html, info=info)

# @list_view.route("/<int:sys_no>/update",methods=["PUT"])
# def update_sys_no_save(sys_no):
#     post_data = json.dumps({"account":"yangrui",
#                         "password":"6320f9d341d76ae9c6bfda5f7b53471f74b0ce87d536f90a2c73f1fe78657f6f"})
#     result = request.get

