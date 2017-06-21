FROM python:2.7

RUN apt-get update;\
    apt-get install -y vim postgresql-client;\
    true

COPY . /opt/docker

# 自动重试3次，第一个使用官方的源，第二次，第三次用豆瓣的源，这样是为了避免
# 在服务器上部署过慢的问题
RUN pip install -r /opt/docker/requirements.txt --default-timeout=20 || \
    pip install -i https://pypi.doubanio.com/simple  \
    -r /opt/docker/requirements.txt --trusted-host pypi.doubanio.com || \
    pip install -i https://pypi.doubanio.com/simple  \
    -r /opt/docker/requirements.txt --trusted-host pypi.doubanio.com

RUN mkdir /opt/logging
RUN mkdir /opt/running

RUN adduser --disabled-password --gecos '' docker
