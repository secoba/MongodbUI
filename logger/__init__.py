#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: lynn
# Date: 2020-05-10
# File: __init__.py

import logging
import os

LOG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")

if not os.path.exists(LOG_PATH): os.makedirs(LOG_PATH)

logging.basicConfig(
    format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
    level=logging.INFO, filename=os.path.join(LOG_PATH, "web.log"))


def log_info(msg, *args, **kwargs):
    logging.info(msg, *args, **kwargs)


def log_error(msg, *args, **kwargs):
    logging.error(msg, *args, **kwargs)


def log_debug(msg, *args, **kwargs):
    logging.debug(msg, *args, **kwargs)


def log_warning(msg, *args, **kwargs):
    logging.warning(msg, *args, **kwargs)
