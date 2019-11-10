FROM python:3.7

COPY . /opt/docker
WORKDIR /opt/docker

RUN pip install -i https://pypi.doubanio.com/simple -r requirements.txt;\
    adduser --disabled-password --gecos '' docker