#/usr/bin/env bash

printf "============== create database =============\n"
printf "========== create migration files ==========\n"
python manage.py db init
printf "============= create database ==============\n"
python manage.py db migrate
printf "============= upgrade database =============\n"
python manage.py db upgrade

