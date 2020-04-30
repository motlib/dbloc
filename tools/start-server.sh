#!/usr/bin/env bash

service nginx start

python3 manage.py migrate
python3 manage.py initadmin

#exec python3 manage.py runserver 0.0.0.0:8000
exec gunicorn dbloc.wsgi
