#!/bin/bash

DJANGODIR=/application
cd ${DJANGODIR}
export PYTHONPATH=${DJANGODIR}:${PYTHONPATH}
if [ -n "$NORELOAD" ]; then
	    PARAMS="--noreload"
fi
celery -A celery_app beat --detach
flower -A celery_app --port=7999

