#!/bin/bash

DJANGODIR=/application
cd ${DJANGODIR}
export PYTHONPATH=${DJANGODIR}:${PYTHONPATH}
if [ -n "$NORELOAD" ]; then
    PARAMS="--noreload"
fi
python manage.py runserver 0.0.0.0:8000 ${PARAMS}
