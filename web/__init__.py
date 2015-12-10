#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import ConfigParser
import json
from platform import system
from flask import Flask

# read config
config = ConfigParser.ConfigParser()
config.read("../config.conf")

env = config.get("Env", "env")
web_listen_ip = config.get(env, "web_listen_ip")
web_port = config.get(env, "web_port")
API_service = "http://%s:%s" % (config.get(env, "api_host"), config.get(env, "api_port"))


def create_app():
    app = Flask("__name__")
    from view_list import list_view as list_view_blueprint
    app.register_blueprint(list_view_blueprint)

    return app

