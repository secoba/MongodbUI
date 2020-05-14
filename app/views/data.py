#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: lynn
# Date: 2020-05-10
# File: data.py


from django.views.decorators.csrf import csrf_exempt

# from app.models import Config
from app.views import STATUS
from app.views import json_data_filter_list
from app.views import json_response
from config.data import connection
from database.mongo import MongoService


@csrf_exempt
def data_list(request):
    """ data list with pagination """
    try:
        data = []
        page = int(request.GET.get("page", 0))
        page = page - 1 if page > 0 else 0
        size = int(request.GET.get("size", 20))
        size = 100 if size > 100 else size
        query_filter = []
        pos = page * size
        cid = request.GET.get("cid", "")
        collect = request.GET.get("collection", "")
        if len(connection) < 1:
            return json_response(status=STATUS.Err,
                                 msg="database config not found", data={})
        mgo = MongoService(host=connection.host, port=int(connection.port),
                           db=connection.database, username=connection.username,
                           password=connection.password, max_pool=5, min_pool=2)
        total = mgo.get_collection(collect).find(
            {"$and": query_filter} if len(query_filter) > 0 else {}).count()
        rows = mgo.get_collection(collect).find(
            {"$and": query_filter} if len(query_filter) > 0 else {}).skip(pos).limit(size)
        for item in rows:
            data.append(item)
        data = json_data_filter_list(json_data=data, exclude=["_id"])
        return json_response(status=STATUS.Ok, msg="success",
                             data={"data": data, "count": total,
                                   "cid": cid, "collection": collect})
    except Exception as ex:
        return json_response(status=STATUS.Err, msg="query data list err: %s" % ex, data={})


def data_info(request):
    """ data item info """
    pass
