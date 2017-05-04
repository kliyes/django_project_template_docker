# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import os

from fabric.api import local, abort
from fabric.context_managers import lcd, cd, settings
from fabric.contrib.console import confirm
from fabric.contrib.files import exists
from fabric.operations import put, run, sudo
from fabric.state import env


PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # project dir on local
PROJECT_NAME = os.path.basename(PROJECT_DIR)
REMOTE_DIR = "/var/project/{}/".format(PROJECT_NAME)  # project dir on server
SETTINGS_DIR = os.path.join(REMOTE_DIR, "src/settings")
DOCKER_DIR = os.path.join(REMOTE_DIR, "docker")


def prod():
    """
    生产环境
    """
    env.user = ""
    env.hosts = []
    env.key_filename = None


def archive():
    """
    使用git archive命令打包代码
    检查是否有未提交的修改
    """
    with lcd(PROJECT_DIR):
        if local("git status -s", capture=True)\
                and not confirm("Contains no committed changes, archive anyway?"):
            abort("Aborting at user request.")
        local("git archive -o deploy/{}.tar.gz master".format(PROJECT_NAME))


def upload():
    """
    上传代码包至服务器
    检查服务器上是否存在代码目录
    """
    with settings(warn_only=True):
        if not exists(REMOTE_DIR):
            sudo("mkdir -p -m 777 {}".format(REMOTE_DIR))
    with cd(REMOTE_DIR):
        put("{}.tar.gz".format(PROJECT_NAME), ".")


def extract():
    """
    解压代码
    """
    with cd(REMOTE_DIR):
        run("tar xf {}.tar.gz".format(PROJECT_NAME))


def check_settings():
    """
    检查必要的settings文件
    """
    with cd(SETTINGS_DIR):
        init_settings = "__init__.py"
        if not exists(init_settings):
            run("echo 'from prod import *' >> {}".format(init_settings))


def start_service():
    """
    docker compose命令启动服务
    """
    with cd(DOCKER_DIR):
        docker_file_args = "-f docker-compose.yml -f docker-compose.prod.yml"
        run("docker-compose {} stop".format(docker_file_args))
        up_cmd = """docker-compose {} up -d --remove-orphans""".format(docker_file_args)
        if confirm("Rebuild all docker images?"):
            up_cmd += " --build"
        run(up_cmd)


def deploy():
    """
    整个部署过程
    """
    archive()
    upload()
    extract()
    check_settings()
    start_service()
