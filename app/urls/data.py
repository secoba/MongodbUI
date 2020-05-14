#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: lynn
# Date: 2020-05-10
# File: data.py

from django.conf.urls import url

from app.views import data

app_name = "Data"

urlpatterns = [
    url(r"^data_list$", data.data_list, name="data_list"),
    url(r"^data_info$", data.data_info, name="data_info"),
]
