FROM python:3.6
COPY sources.list /etc/apt/sources.list
RUN apt-get update && apt-get install -y nginx && nginx
# ADD nginx-1.15.2.tar.gz /usr/src
# RUN cd /usr/src/nginx-1.15.2 \
#     && mkdir /usr/local/nginx \
#     && ./configure --prefix=/usr/local/nginx && make && make install \
#     && ln -s /usr/local/nginx/sbin/nginx /usr/local/sbin/ \
#     && nginx \
#     && rm -rf /usr/src/nginx-1.15.2
RUN mkdir /backend
COPY ./backend/requirements.txt /backend/requirements.txt
WORKDIR /backend
RUN ls && pip install uwsgi -i https://pypi.tuna.tsinghua.edu.cn/simple/ \
    && pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/ 
CMD  . /start.sh
EXPOSE 80


