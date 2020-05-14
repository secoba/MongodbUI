#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: lynn
# Date: 2020-05-10

import os
import logging
import multiprocessing
import logging.handlers
from logging.handlers import WatchedFileHandler
from config.app_conf import WEB_HOST, WEB_PORT

bind = "%s:%s" % (WEB_HOST, WEB_PORT)   # 绑定的ip与端口
backlog = 512                           # 监听队列数量，64-2048
worker_class = "sync"                   # 使用gevent模式，还可以使用sync 模式，默认的是sync模式
workers = 4                             # multiprocessing.cpu_count()    #进程数
threads = 16                            # multiprocessing.cpu_count()*4 #指定每个进程开启的线程数
loglevel = "info"                       # 日志级别，这个日志级别指的是错误日志的级别，而访问日志的级别无法设置
access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" "%(a)s"'

accesslog = "./logs/gunicorn_access.log"    # 访问日志文件
errorlog = "./logs/gunicorn_error.log"      # 错误日志文件
# accesslog = "-"  # 访问日志文件，"-" 表示标准输出
# errorlog = "-"   # 错误日志文件，"-" 表示标准输出

proc_name = 'gunicorn_web'  # 进程名
