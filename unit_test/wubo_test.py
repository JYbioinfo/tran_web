# -*- coding: utf-8 -*-
# Create Date 2015/12/14
__author__ = 'wubo'
import ConfigParser

if __name__ == "__main__":
    config = ConfigParser.ConfigParser()
    config.read("../config.conf")
    env = config.get("Env", "env")
    h = config.get(env, "api_host")
    p = config.get(env, "api_port")
    print type(h)
    print h
    print type(p)
    print p
    API_service = "http://%s:%s" % (config.get(env, "api_host"), config.get(env, "api_port"))
    print type(API_service)

    

