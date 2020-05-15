# Create your views here.

from bson import Code
from django.shortcuts import render

from config.data import connection
from database.mongo import MongoService
from logger import log_error


def collections():
    """ get all collections """
    try:
        if len(connection) < 1:
            return []
        mgo = MongoService(host=connection.host, port=int(connection.port),
                           db=connection.database, username=connection.username,
                           password=connection.password, max_pool=5, min_pool=2)
        return mgo.get_collections()[connection["database"]]
    except Exception as ex:
        log_error(ex)
        return []


def collection_keys(collect):
    """ collection keys """
    try:
        if len(connection) < 1:
            return []
        mgo = MongoService(host=connection.host, port=int(connection.port),
                           db=connection.database, username=connection.username,
                           password=connection.password, max_pool=5, min_pool=2)
        map_reduce = Code("function() { for (var key in this) { emit(key, null); } }")
        reduce = Code("function(key, stuff) { return null; }")
        result = mgo.get_collection(collect).map_reduce(map_reduce, reduce, "my_results")
        return result.distinct('_id')
    except Exception as ex:
        log_error(ex)
        return []


def index(request):
    """ index """
    return render(request, "index.html", {
        "collects": collections(),
        "host": connection.get("host") if connection.get("host") else "",
        "port": connection.get("port") if connection.get("port") else "",
        "database": connection.get("database") if connection.get("database") else "",
        "username": connection.get("username") if connection.get("username") else "",
        "password": connection.get("password") if connection.get("password") else "",
        "current_collection": connection.get("current_collection") if connection.get("current_collection") else "",
    })
