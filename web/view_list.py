# -*- coding: utf-8 -*-
# Create Date 2015/12/10
__author__ = 'wubo'
import requests,json
from flask import Blueprint, render_template, redirect, request, url_for
from web import API_service, User
from flask_login import login_user, login_required, current_user, logout_user, flash
from web.forms.login_form import LoginForm
from tools.Mysql_db import DB

list_view = Blueprint("list_view", __name__)

list_html = "list.html"
login_html = "login.html"
db = None
try:
    db = DB()
    db.connect()
except Exception, e:
    print e


# @list_view.errorhandler(404)
# def page_not_found(e):
#     return render_template('404.html'), 404
#
#
# @list_view.errorhandler(500)
# def internal_server_error(e):
#     return render_template('500.html'), 500


@list_view.route("/", methods=["GET", "PUT"])
def hello():
    return render_template("index.html")


@list_view.route("/login/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # login and validate the user...
        # login_user(remember=True)
        account = form.account.data
        passwd = form.passwd.data
        form.account.data = ''
        form.passwd.data = ''
        get_hmac_p = requests.post(API_service + '/api/task/hmacpasswd/', data=json.dumps({"passwd": passwd}))
        passwd = get_hmac_p.text
        r = requests.post(API_service + '/api/task/userconfirm/', data=json.dumps({"account": account, "passwd": passwd}))
        if r.status_code == 200:
            res = json.loads(r.text)
            print res["status"]
            if res["status"] == 002:
                user = User()
                user.account = account
                login_user(user)
                if user is not None:
                    login_user(user, form.remember_me.data)
                    return redirect(url_for('list_view.get_task_detail'))  #测试，待修改
            flash('Invalid username or password.')
        else:
            error = "用户名与密码不匹配"
            account_error = form.account.errors
            password_error = form.passwd.errors
            flash(account_error)
            flash(password_error)
            return render_template("login.html", form=form, account_error=account_error, password_error=password_error,
                                   error=error)
    return render_template(login_html, form=form)


@list_view.route("/logout/")
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('login'))


# @list_view.route("/register", methods=["GET", "POST"])
# def register():
#     form = RegistrationForm()
#     if form.validate_on_submit():
#
#         flash('You can now login.')
#         return redirect(url_for('login'))
#     return render_template('register.html', form=form)


@list_view.route("/tasks/", methods=["GET", "PUT"])
@login_required
def get_task_list():
    request_data = json.loads(request.data)
    account = request_data["account"]
    passwd = request_data["passwd"]
    data = json.dumps({"account":account,"passwd":passwd})
    result = json.loads(requests.get(API_service+"/api/task/tasks/", data=data))
    task_list = []
    for item in result:
        task_list.append(item)
    return render_template(list_html, task_list=task_list)


@list_view.route("/api/task/tasks/<task_no>/", methods=["GET", "PUT"])
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

