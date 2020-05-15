#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: lynn
# Date: 2020-05-10
# File: data.py


from bson.objectid import ObjectId
from django.views.decorators.csrf import csrf_exempt

# from app.models import Config
from app.views import STATUS
from app.views import json_data_filter_list
from app.views import json_response
from config.data import connection


def data_del(request):
    try:
        _id = request.GET.get("id", "")
        mgo = connection["client"]
        rst = mgo.get_collection(connection["current_collection"]).remove({"_id": ObjectId(_id)})
        return json_response(status=STATUS.Ok, msg="success", data=rst)
    except Exception as ex:
        return json_response(status=STATUS.Err, msg="query data list err: %s" % ex, data={})


@csrf_exempt
def data_list(request):
    """ data list with pagination """
    try:
        data = list()
        page = int(request.GET.get("page", 0))
        page = page - 1 if page > 0 else 0
        size = 14
        # size = int(request.GET.get("size", 10))
        # size = 100 if size > 100 else size
        query_filter = []
        pos = page * size
        collect = request.GET.get("collection", "")
        if len(connection) < 1:
            return json_response(status=STATUS.Err,
                                 msg="database config not found", data={})
        mgo = connection["client"]
        total = mgo.get_collection(collect).find(
            {"$and": query_filter} if len(query_filter) > 0 else {}).count()
        rows = mgo.get_collection(collect).find(
            {"$and": query_filter} if len(query_filter) > 0 else {}).skip(pos).limit(size)
        for item in rows:
            data.append(item)
        connection["current_collection"] = collect
        data = json_data_filter_list(json_data=data)
        return json_response(status=STATUS.Ok, msg="success",
                             data={"list": data,
                                   "count": total,
                                   "current_size": size,
                                   "current_page": page + 1,
                                   "current_collection": collect})
    except Exception as ex:
        return json_response(status=STATUS.Err, msg="query data list err: %s" % ex, data={})


def data_info(request):
    """ data item info """
    try:
        _id = request.GET.get("id", "")
        mgo = connection["client"]
        item = mgo.get_collection(connection["current_collection"]).find_one({"_id": ObjectId(_id)})
        data = json_data_filter_list(json_data=[item])
        return json_response(status=STATUS.Ok, msg="success", data=data[0])
    except Exception as ex:
        return json_response(status=STATUS.Err, msg="query data list err: %s" % ex, data={})
