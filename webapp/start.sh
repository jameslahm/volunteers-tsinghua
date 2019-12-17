nginx
export FLASK_CONFIG=production
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple 
python manage.py db init
python manage.py db stamp heads
python manage.py db migrate
python manage.py db upgrade
uwsgi --ini uwsgi.ini
