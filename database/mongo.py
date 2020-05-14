#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: lynn
# Date: 2020-05-10
# File: mongo.py


from pymongo import MongoClient


class AuthErr(Exception):
    pass


class MongoService():
    def __init__(self, host, port, db, username, password, max_pool, min_pool):
        self.__conn = MongoClient(host, port,
                                  maxPoolSize=max_pool,
                                  minPoolSize=min_pool,
                                  connect=False)
        self.is_login = self.__connect(db, username, password)

    def __connect(self, db, username, password):
        self.__db = self.__conn[db]
        if username and len(username) > 0 \
                and password and len(password) > 0:
            is_login = self.__db.authenticate(username, password)
            return is_login
        return False

    def get_collection(self, collection):
        if not self.is_login:
            raise AuthErr
        return self.__db[collection]

    def get_collections(self):
        if not self.is_login:
            raise AuthErr
        return dict((db, [collection for collection in
                          self.__conn[db].list_collection_names()])
                    for db in self.__conn.list_database_names())
