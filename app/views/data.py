#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: lynn
# Date: 2020-05-10
# File: data.py

import base64

# from app.models import Config
from bson import Code
from bson.objectid import ObjectId
from django.views.decorators.csrf import csrf_exempt

from app.cel import parser_expr
from app.views import STATUS
from app.views import json_data_filter_list
from app.views import json_response
from config.data import connection
from logger import log_error


def collection_keys(collect):
    """ collection keys """
    try:
        if len(connection) < 1:
            return []
        mgo = connection["client"]
        map_reduce = Code("function() { for (var key in this) { emit(key, null); } }")
        reduce = Code("function(key, stuff) { return null; }")
        result = mgo.get_collection(collect).map_reduce(map_reduce, reduce, "my_results")
        return result.distinct('_id')
    except Exception as ex:
        log_error(ex)
        return []


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
        size = 15
        data = list()
        query = request.GET.get("query", "")
        page = int(request.GET.get("page", 0))
        page = page - 1 if page > 0 else 0
        collect = request.GET.get("collection", "")
        try:
            de_str = base64.b64decode(query).decode("utf-8") if query else None
            query = parser_expr(de_str) if de_str else {}
        except Exception as ex:
            log_error(ex)
            return json_response(status=STATUS.Ok, msg="success",
                                 data={"list": [],
                                       "count": 0,
                                       "current_size": size,
                                       "current_page": page + 1,
                                       "current_collection": collect})
        pos = page * size
        if len(connection) < 1:
            return json_response(status=STATUS.Err,
                                 msg="database config not found", data={})
        mgo = connection["client"]
        total = mgo.get_collection(collect).find(query if len(query) > 0 else {}).count()
        rows = mgo.get_collection(collect).find(query if len(query) > 0 else {}).skip(pos).limit(size)
        for item in rows:
            data.append(item)
        connection["current_collection"] = collect
        connection["collection_keys"] = collection_keys(collect)
        data = json_data_filter_list(json_data=data)
        return json_response(status=STATUS.Ok, msg="success",
                             data={"list": data,
                                   "count": total,
                                   "current_size": size,
                                   "current_page": page + 1,
                                   "current_collection": collect,
                                   "collection_keys": connection["collection_keys"]})
    except Exception as ex:
        log_error(ex)
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
