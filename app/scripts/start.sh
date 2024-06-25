#! /usr/bin/env sh
set -e

if [ -f "/app/app/main.py" ]; then
    DEFAULT_MODULE_NAME=app.main
else
    echo "Can't find main.py in /app/app/entrypoints/telegram/main.py"
    exit 1
fi
MODULE_NAME=${MODULE_NAME:-$DEFAULT_MODULE_NAME}
VARIABLE_NAME=${VARIABLE_NAME:-app}
export APP_MODULE=${APP_MODULE:-"$MODULE_NAME:$VARIABLE_NAME"}

HOST=${BACKEND__HOST:-0.0.0.0}
PORT=${BACKEND__PORT:-80}
LOG_LEVEL=${LOG_LEVEL:-info}

RUN_PRE_START=${RUN_PRE_START:-false}
if [ "$RUN_PRE_START" = "true" ]; then
    PRE_START_PATH=${PRE_START_PATH:-/app/app/scripts/prestart.sh}
    echo "Checking for script in $PRE_START_PATH"
    if [ -f $PRE_START_PATH ] ; then
        echo "Running script $PRE_START_PATH"
        . "$PRE_START_PATH"
    else
        echo "There is no script $PRE_START_PATH"
    fi
fi

exec uvicorn --reload --host $HOST --port $PORT --log-level $LOG_LEVEL "$APP_MODULE"
