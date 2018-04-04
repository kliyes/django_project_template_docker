FROM python:2.7

COPY sources.list /etc/apt
COPY . /opt/docker

RUN apt-get update;\
    apt-get install -y postgresql-client;\
    pip install -i https://pypi.doubanio.com/simple -r /opt/docker/requirements.txt --trusted-host pypi.doubanio.com;\
    mkdir -m 777 /opt/logging /opt/running;\
    adduser --disabled-password --gecos '' docker