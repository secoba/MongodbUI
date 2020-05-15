# Create your views here.

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


def index(request):
    """ index """
    return render(request, "index.html", {
        "collects": collections(),
        "host": connection.get("host") if connection.get("host") else "",
        "port": connection.get("port") if connection.get("port") else "",
        "database": connection.get("database") if connection.get("database") else "",
        "username": connection.get("username") if connection.get("username") else "",
        "password": connection.get("password") if connection.get("password") else "",
        "collection_keys": connection.get("collection_keys") if connection.get("collection_keys") else [],
        "current_collection": connection.get("current_collection") if connection.get("current_collection") else "",
    })
