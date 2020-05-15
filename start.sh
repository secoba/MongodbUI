#!/bin/sh

LOG=$(pwd)/logs
if [ ! -d $LOG ]; then
  mkdir -p "$LOG"
fi

gunicorn -c config/gunicorn_conf.py MongodbUI.wsgi:application >/dev/null 2>&1
