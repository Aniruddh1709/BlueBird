#!/bin/bash
NAME="gunicorn"
ROOTDIR=/<project_name>/

NUM_WORKERS=1

cd $ROOTDIR

exec gunicorn app:app \
  --name $NAME \
  --workers $NUM_WORKERS \
  -k gevent \
  --bind=0.0.0.0:80 \
  --log-level=info \
  --access-logfile=- \
  --timeout=10 \
  --reload
