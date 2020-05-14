#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: lynn
# Date: 2020-05-10
# File: app.conf.py


from config import \
    get_web_host, \
    get_web_port, \
    get_web_debug

WEB_HOST = get_web_host()
WEB_PORT = get_web_port()
WEB_DEBUG = get_web_debug()
