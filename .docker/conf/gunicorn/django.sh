#!/bin/bash
# Dockerized version of gunicorn starter script
NAME="lms"                  # Name of the application
DJANGODIR=/application                # Django project directory

if [[ -n DJANGO_NUM_WORKERS ]]; then
    DJANGO_NUM_WORKERS=1      # how many worker processes should Gunicorn spawn
fi
DJANGO_WSGI_MODULE=imcslms.wsgi  # WSGI module name

# Activate the virtual environment
cd ${DJANGODIR}
export PYTHONPATH=${DJANGODIR}:${PYTHONPATH}

# Start your Django Gunicorn
# Programs meant to be run under supervisor should not daemonize
# themselves (do not use --daemon)
gunicorn ${DJANGO_WSGI_MODULE} \
  --preload \
  --pythonpath ${PYTHONPATH} \
  --name ${NAME} \
  --workers ${DJANGO_NUM_WORKERS} \
  --max-requests 3000 \
  --max-requests-jitter 1500 \
  --bind 0.0.0.0:8080 \
  --log-level info \
  --log-file -
