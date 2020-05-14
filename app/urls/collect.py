#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: lynn
# Date: 2020-05-10
# File: collect.py


from django.conf.urls import url

from app.views import collect

app_name = "Collect"

urlpatterns = [
    url(r"^collections$", collect.collections, name="collections"),
    url(r"^collection_keys$", collect.collection_keys, name="collection_keys"),
]
