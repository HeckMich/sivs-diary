#!/bin/sh
SERVICE_NAME=sivs-diary_service
GUNICORN_CMD="/home/ubuntu/venv/bin/gunicorn -w 4 -b 0.0.0.0:8000 --chdir /home/ubuntu/sivs-diary/sivs-diary/application/ app:app"
PID_PATH_NAME=/tmp/sivs-diary_service-pid

case $1 in
start)
    echo "Starting $SERVICE_NAME ..."
    if [ ! -f $PID_PATH_NAME ]; then
        nohup $GUNICORN_CMD 2>> /dev/null >> /dev/null &
        echo $! > $PID_PATH_NAME
        echo "$SERVICE_NAME started ..."
    else
        echo "$SERVICE_NAME is already running ..."
    fi
    ;;
stop)
    if [ -f $PID_PATH_NAME ]; then
        PID=$(cat $PID_PATH_NAME)
        echo "$SERVICE_NAME stopping ..."
        kill $PID
        echo "$SERVICE_NAME stopped ..."
        rm $PID_PATH_NAME
    else
        echo "$SERVICE_NAME is not running ..."
    fi
    ;;
restart)
    if [ -f $PID_PATH_NAME ]; then
        PID=$(cat $PID_PATH_NAME)
        echo "$SERVICE_NAME stopping ..."
        kill $PID
        echo "$SERVICE_NAME stopped ..."
        rm $PID_PATH_NAME
        echo "$SERVICE_NAME starting ..."
        nohup $GUNICORN_CMD 2>> /dev/null >> /dev/null &
        echo $! > $PID_PATH_NAME
        echo "$SERVICE_NAME started ..."
    else
        echo "$SERVICE_NAME is not running ..."
    fi
    ;;
*)
    echo "Usage: $0 {start|stop|restart}"
    exit 1
    ;;
esac
