#!/bin/bash
# Dockerized version of gunicorn starter script
NAME="lms"                  # Name of the application
DJANGODIR=/application                # Django project directory

DJANGO_NUM_WORKERS=2      # how many worker processes should Gunicorn spawn
DJANGO_ASGI_MODULE=imcslms.asgi  # WSGI module name
WORKER_CLASS=uvicorn.workers.UvicornWorker
# Activate the virtual environment
cd ${DJANGODIR}
export PYTHONPATH=${DJANGODIR}:${PYTHONPATH}

# Start your Django Gunicorn
# Programs meant to be run under supervisor should not daemonize
# themselves (do not use --daemon)
gunicorn ${DJANGO_ASGI_MODULE} \
  --preload \
  --pythonpath ${PYTHONPATH} \
  --name ${NAME} \
  --workers ${DJANGO_NUM_WORKERS} \
  --worker-class ${WORKER_CLASS} \
  --max-requests 3000 \
  --max-requests-jitter 1500 \
  --bind 0.0.0.0:8080 \
  --log-level info \
  --log-file - \
  --pid gunicorn.pid

