# ! /bin/bash

echo "--------create test database file--------"
python manage.py db init
python manage.py db migrate -m "init"
python manage.py db upgrade

python manage.py shell
# type Role.insert_roles()
echo "--------create database file done--------"
