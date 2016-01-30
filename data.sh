#/usr/bin/env bash

printf "=========== create database ============\n"
printf "create migration files\n"
python manage.py db init
printf "create database\n"
python manage.py db migrate
printf "upgrade database\n"
python manage.py db upgrade
printf "create roles\n"
python manage.py shell
printf "add user\n"
python manage.py adduser neo1218@yeah.net neo1218
printf "database setup done!"

