# -*- coding: utf-8 -*-
# Create Date 2015/12/10
__author__ = 'wubo'
import requests,json
from flask import Blueprint, render_template, redirect, request, url_for
from web import API_service
from flask_login import login_user,login_required, current_user
from web.forms.login_form import LoginForm
list_view = Blueprint("list_view", __name__)
list_html = "list.html"
login_html= "sign.html"


@list_view.route("/", methods=["GET", "PUT"])
def hello():
    return redirect("/login")


@list_view.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # login and validate the user...
        login_user(user)
        flash("Logged in successfully.")
        return redirect(request.args.get("next") or url_for("tasks"))
    return render_template(login_html, form=form)


@list_view.route("/tasks", methods=["GET", "PUT"])
@login_required
def get_task_list():
    request_data = json.loads(request.data)
    account = request_data["account"]
    passwd = request_data["passwd"]
    data = json.dumps({"account":account,"passwd":passwd})
    result = json.loads(requests.get(API_service+"/tasks/", data=data))
    task_list = []
    for item in result:
        task_list.append(item)
    return render_template(list_html, task_list=task_list)


@list_view.route("/tasks/<task_no>", methods=["GET", "PUT"])
@login_required
def get_task_detail():
    request_data = json.loads(request.data)
    account = request_data["account"]
    passwd = request_data["passwd"]
    data = json.dumps({"account": account, "passwd": passwd})
    result = json.loads(requests.get(API_service+"/tasks/", data=data))
    task_list = []
    for item in result:
        task_list.append(item)
    return render_template(list_html, task_list=task_list)

