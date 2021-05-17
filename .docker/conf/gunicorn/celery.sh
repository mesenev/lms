#!/bin/bash

DJANGODIR=/application
cd ${DJANGODIR}
export PYTHONPATH=${DJANGODIR}:${PYTHONPATH}
if [ -n "$NORELOAD" ]; then
	    PARAMS="--noreload"
fi



celery -A celery_app beat &
flower -A celery_app --port=7999 &
celery -A celery_app worker -c 2 -O fair
