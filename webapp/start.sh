nginx
export FLASK_CONFIG=production
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple 
uwsgi --ini uwsgi.ini
