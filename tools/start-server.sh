#!/usr/bin/env bash
#
# Start script for running inside docker container
#

# Start nginx for serving static and media files and act as a reverse proxy for
# gunicorn
service nginx start

# Set up database
python3 manage.py migrate

# Create admin user (password is shown during startup in the logs)
python3 manage.py initadmin

# If nothing else is set already, we run the testing config for the container
if [ -z "${DJANGO_SETTINGS_MODULE}" ]
then
    export DJANGO_SETTINGS_MODULE=dbloc.settings.testing
fi

exec gunicorn dbloc.wsgi
