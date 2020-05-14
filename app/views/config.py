#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: lynn
# Date: 2020-05-10
# File: basic.py


from django.views.decorators.csrf import csrf_exempt

from app.views import STATUS
from app.views import json_response
from config.data import connection


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
        return json_response(status=STATUS.Ok, msg="save config success", data={})
    return json_response(status=STATUS.Err, msg="method not support", data={})

# @csrf_exempt
# def add_config(request):
#     """ add mongo config """
#     if request.method == "POST":
#         host = request.POST.get("host", "")
#         port = request.POST.get("port", "")
#         database = request.POST.get("database", "")
#         username = request.POST.get("username", "")
#         password = request.POST.get("password", "")
#         if host is None or len(host) < 1 or port is None or len(port) < 1:
#             return json_response(status=STATUS.Err, msg="host or port is none", data={})
#         Config.objects.create(cid=str(uuid.uuid4()),
#                               host=host,
#                               port=port,
#                               database=database,
#                               username=username,
#                               password=password)
#         return json_response(status=STATUS.Ok, msg="add config success", data={})
#     return json_response(status=STATUS.Err, msg="method not support", data={})


# def config_list(request):
#     """ config list """
#     page = request.GET.get("page", 1)
#     size = request.GET.get("size", 10)
#     configs = Config.objects.all()
#     configs_list, page_range = paginator_tool(
#         pages=page,
#         queryset=configs,
#         display_amount=size,
#     )
#     total = configs.count()
#     configs_list = data_filter_list(configs_list, ["cid", "host", "port", "database"])
#     return json_response(status="", data={"count": total, "data": configs_list}, msg="")


# @csrf_exempt
# def update_config(request):
#     """ update config """
#     if request.method == "POST":
#         cid = request.POST.get("cid", "")
#         host = request.POST.get("host", "")
#         port = request.POST.get("port", "")
#         database = request.POST.get("database", "")
#         username = request.POST.get("username", "")
#         password = request.POST.get("password", "")
#         if host is None or len(host) < 1 or \
#                 port is None or len(port) < 1 or \
#                 cid is None or len(cid) < 1:
#             return json_response(status=STATUS.Err, msg="cid and host and port cannot be none", data={})
#         config = Config.objects.get(cid=cid)
#         if config is None:
#             return json_response(status=STATUS.Err, msg="config not found", data={})
#         config.host = host
#         config.port = port
#         config.username = username
#         config.password = password
#         config.database = database
#         config.save()
#         return json_response(status=STATUS.Ok, msg="update config success", data={})
#     return json_response(status=STATUS.Err, msg="method not support", data={})
