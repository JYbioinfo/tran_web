# -*- coding: utf-8 -*-
# Create Date 2015/12/10
__author__ = 'wubo'
from flask import Blueprint,render_template
from web import API_service

list_view = Blueprint("list_view", __name__)
list_html = "list.html"


@list_view.route("/tasks/", methods=["GET", "PUT"])
def get_task_list():

    return render_template(list_html)

    

