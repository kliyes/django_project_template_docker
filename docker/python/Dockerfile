FROM python:2.7

COPY sources.list /etc/apt
COPY . /opt/docker
WORKDIR /opt/docker

RUN apt-get update;\
    pip install -i https://pypi.doubanio.com/simple -r requirements.txt --trusted-host pypi.doubanio.com;\
    adduser --disabled-password --gecos '' docker