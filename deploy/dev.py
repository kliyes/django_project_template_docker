# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import os

from fabric.api import local, settings
from fabric.colors import yellow, cyan, green
from fabric.context_managers import lcd, prefix, hide
from fabric.contrib.console import confirm
from fabric.utils import puts


PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MACHINE_NAME = os.path.basename(PROJECT_DIR).replace("_", "-")  # allowed machine name chars: 0-9a-zA-Z . -
SETTINGS_DIR = os.path.join(PROJECT_DIR, "src/settings")
DOCKER_DIR = os.path.join(PROJECT_DIR, "docker")


def start_machine():
    """
    检查machine状态并启动
    """
    with settings(warn_only=True):
        machine_status = local("docker-machine status {}".format(MACHINE_NAME),
                               capture=True)
    if "Host does not exist" in machine_status.stderr:
        creation_cmd = "docker-machine create {} -d virtualbox".format(MACHINE_NAME)
        puts(yellow("Machine does not exist, creating a new one..."))
        if confirm("Use another mirror to speed up pulling images?"):
            creation_cmd += " --engine-registry-mirror=https://avyczztf.mirror.aliyuncs.com"
        local(creation_cmd)
    elif not machine_status == "Running":
        local("docker-machine start {}".format(MACHINE_NAME))

    with settings(warn_only=True):
        configs = local("docker-machine config {}".format(MACHINE_NAME),
                        capture=True)
    if "There was an error validating certificates" in configs.stderr:
        puts(yellow("Machine IP changed so the certificates invalid, regenerating..."))
        local("docker-machine regenerate-certs {} -f".format(MACHINE_NAME))


def check_settings():
    """
    检查必要的settings文件
    """
    with lcd(SETTINGS_DIR):
        init_settings = "__init__.py"
        dev_settings = "dev.py"
        if not os.path.exists(os.path.join(SETTINGS_DIR, init_settings)):
            local("echo 'from dev import *' >> {}".format(init_settings))
        if not os.path.exists(os.path.join(SETTINGS_DIR, dev_settings)):
            local("""echo "from base import *\n\n\nDEBUG=True\nALLOWED_HOSTS = ['*']" >> {}""".format(dev_settings))


def start_service():
    """
    启动docker服务
    """
    with lcd(DOCKER_DIR):
        up_cmd = "docker-compose up -d --remove-orphans"
        if confirm("Rebuild all docker images?"):
            up_cmd += " --build"
        with prefix("eval $(docker-machine env {})".format(MACHINE_NAME)):
            local("docker-compose stop")
            local(up_cmd)


def welcome():
    """
    输出欢迎信息
    """
    with hide("running"):
        machine_ip = local("docker-machine ip {}".format(MACHINE_NAME), capture=True)

    puts(green("Already started a development server at http://{}:8000".format(machine_ip)))
    puts(green("Default superuser created: admin/admin"))
    puts(green("Please active the machine environment before run any docker-compose command:"))
    puts(cyan("    1. Change dir to '../docker'"))
    puts(cyan("    2. Execute: eval $(docker-machine env {})".format(MACHINE_NAME)))
    puts(green("Also, run django manage commands via:"))
    puts(cyan("    docker-compose run --rm web python manage.py [COMMAND]"))
    puts(green("Tail the runserver logs use:"))
    puts(cyan("    docker-compose logs -ft web"))


def start_develop():
    """
    完整的本地开发部署流程
    """
    start_machine()
    check_settings()
    start_service()
    welcome()
