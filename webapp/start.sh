nginx
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
pip install -r requirements.txt
uwsgi --ini uwsgi.ini
