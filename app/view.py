# Create your views here.

from django.shortcuts import render

from config.data import connection


def index(request):
    """ index """
    return render(request, "index.html", {
        "host": connection.get("host") if connection.get("host") else "",
        "port": connection.get("port") if connection.get("port") else "",
        "database": connection.get("database") if connection.get("database") else "",
        "username": connection.get("username") if connection.get("username") else "",
        "password": connection.get("password") if connection.get("password") else "",
    })
