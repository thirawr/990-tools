#!/bin/bash

NAME=tax_tools
BASEPATH=/home/didevadmin/webapps/990-tools
LOGFILE=$BASEPATH/"logs/"$NAME".log"
PIDFILE=$BASEPATH/"logs/"$NAME".pid"
NUM_WORKERS=3
APPHOST="0.0.0.0"
APPPORT=8010

export DJANGO_SETTINGS_MODULE=tax_tools.settings.prod
export DJANGO_WSGI_MODULE=tax_tools.wsgi

echo "Starting $NAME as `whoami`"
# cd ${BASEPATH}
cd /home/didevadmin/webapps/990-tools

# workon 990-tools
source /home/didevadmin/.virtualenvs/990-tools/bin/activate

exec gunicorn $NAME.wsgi:application \
    --bind $APPHOST:$APPPORT \
    --workers=$NUM_WORKERS \
    --log-file=$LOGFILE
