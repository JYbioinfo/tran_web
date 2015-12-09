# -*- coding: utf-8 -*-
# Create Date 2015/12/9
import json
from flask import Blueprint
from tools.Mysql_db import DB
task_api = Blueprint("task_api",__name__)
db = DB()


@task_api.route("/tasks/",methods=["GET"])
def get_task_list():
    return json.dumps({"status":"hello world!"})
    

