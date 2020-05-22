#!/usr/bin/env sh
#
# Start script for running inside docker container
#

# Set up database
python3 manage.py migrate

# Create admin user (password is shown during startup in the logs)
python3 manage.py initadmin

# If nothing else is set already, we run the testing config for the container
if [ -z "${DJANGO_SETTINGS_MODULE}" ]
then
    export DJANGO_SETTINGS_MODULE=dbloc_project.settings.testing
fi

# Start nginx for serving static and media files and act as a reverse proxy for
# gunicorn
nginx -c /etc/nginx/nginx.conf

exec gunicorn dbloc_project.wsgi
