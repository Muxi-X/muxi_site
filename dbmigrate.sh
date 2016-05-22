#!/bin/sh

python manage.py db migrate
python manage.py db upgrade
