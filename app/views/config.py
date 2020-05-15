#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: lynn
# Date: 2020-05-10
# File: basic.py


from django.views.decorators.csrf import csrf_exempt

from app.views import STATUS
from app.views import json_response
from config.data import connection
from database.mongo import MongoService


@csrf_exempt
def save_config(request):
    """ add mongo config """
    if request.method == "POST":
        host = request.POST.get("host", "")
        port = request.POST.get("port", "")
        database = request.POST.get("database", "")
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        if host is None or len(host) < 1:
            return json_response(status=STATUS.Err, msg="host is none", data={})
        if port is None or len(port) < 1:
            return json_response(status=STATUS.Err, msg="port is none", data={})
        if database is None or len(database) < 1:
            return json_response(status=STATUS.Err, msg="database is none", data={})
        connection["host"] = host
        connection["port"] = port
        connection["database"] = database
        connection["username"] = username
        connection["password"] = password
        try:
            connection["client"] = MongoService(host=host, port=int(port),
                                                db=database, username=username,
                                                password=password, max_pool=5, min_pool=2)
            return json_response(status=STATUS.Ok, msg="save config success", data={})
        except Exception as ex:
            return json_response(status=STATUS.Err, msg="save config failed: %s" % ex, data={})
    return json_response(status=STATUS.Err, msg="method not support", data={})
