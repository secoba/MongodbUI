#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: lynn
# Date: 2020-05-10
# File: collect.py


from bson import Code
from django.views.decorators.csrf import csrf_exempt

# from app.models import Config
from app.views import STATUS
from app.views import json_response
from config.data import connection
from database.mongo import MongoService


@csrf_exempt
def collections(request):
    """ get all collections """
    try:
        if len(connection) < 1:
            return json_response(status=STATUS.Err, msg="database config not found", data={})
        mgo = MongoService(host=connection.host, port=int(connection.port),
                           db=connection.database, username=connection.username,
                           password=connection.password, max_pool=5, min_pool=2)
        return json_response(status=STATUS.Ok, msg="success", data=mgo.get_collections())
    except Exception as ex:
        return json_response(status=STATUS.Err, msg="get collections err: %s" % ex, data={})


def collection_keys(request):
    """ collection keys """
    try:
        # cid = request.GET.get("cid", "")
        # config = Config.objects.get(cid=cid)
        # if config is None:
        #     return json_response(status=STATUS.Err, msg="database config not found", data={})
        collect = request.GET.get("collection", "")
        if len(connection) < 1:
            return json_response(status=STATUS.Err, msg="database config not found", data={})
        mgo = MongoService(host=connection.host, port=int(connection.port),
                           db=connection.database, username=connection.username,
                           password=connection.password, max_pool=5, min_pool=2)
        map_reduce = Code("function() { for (var key in this) { emit(key, null); } }")
        reduce = Code("function(key, stuff) { return null; }")
        result = mgo.get_collection(collect).map_reduce(map_reduce, reduce, "my_results")
        return json_response(status=STATUS.Ok, msg="success", data={"keys": result.distinct('_id')})
    except Exception as ex:
        return json_response(status=STATUS.Err, msg="get collection keys err: %s" % ex, data={})
