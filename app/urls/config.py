#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: lynn
# Date: 2020-05-10
# File: basic.py


from django.conf.urls import url

from app.views import config

app_name = "Config"

urlpatterns = [
    url(r"^save_config$", config.save_config, name="save_config"),
]
