nginx
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
uwsgi --ini uwsgi.ini
