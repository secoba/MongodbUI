#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: lynn
# Date: 2020-05-10
# File: __init__.py

import configparser
import os

config_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.ini")
conf = configparser.RawConfigParser()
conf.read(config_file, encoding="utf-8")


def get_web_host():
    try:
        return os.environ.get("WEB_HOST") if os.environ.get("WEB_HOST") else conf.get("web", "host")
    except Exception as e:
        print("[-] get web host err: %s, use default 127.0.0.1" % e)
    return "127.0.0.1"


def get_web_port():
    """ get port """
    try:
        return int(os.environ.get("WEB_PORT")) if os.environ.get("WEB_PORT") else conf.get("web", "port")
    except Exception as e:
        print("[-] get web port err: %s, use default 18080" % e)
    return 18080


def get_web_debug():
    """ get debug """
    try:
        return bool(os.environ.get("WEB_DEBUG")) if os.environ.get("WEB_DEBUG") else conf.getboolean("web", "debug")
    except Exception as e:
        print("[-] get web debug err: %s, use default false" % e)
    return False
