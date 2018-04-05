# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import os

from fabric.api import local, settings
from fabric.colors import yellow, cyan, green
from fabric.context_managers import lcd, prefix, hide
from fabric.contrib.console import confirm
from fabric.operations import prompt
from fabric.utils import puts


PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_NAME = os.path.basename(PROJECT_DIR)
MACHINE_NAME = PROJECT_NAME.replace("_", "-")  # allowed machine name chars: 0-9a-zA-Z . -
SETTINGS_DIR = os.path.join(PROJECT_DIR, "src/settings")
DOCKER_DIR = os.path.join(PROJECT_DIR, "docker")
REGISTRY_MIRROR = "https://avyczztf.mirror.aliyuncs.com"
BOOT2DOCKER_REPO = "https://github.com/boot2docker/boot2docker"
CACHED_BOOT2DOCKER = "~/.docker/machine/cache/boot2docker.iso"
BOOT2DOCKER_LEGACY_VERSION = "v17.05.0-ce"


def start_machine():
    """
    检查machine状态并启动
    """
    with settings(warn_only=True):
        machine_status = local("docker-machine status {}".format(MACHINE_NAME),
                               capture=True)
    if "does not exist" in machine_status.stderr:
        creation_cmd = "docker-machine create {}".format(MACHINE_NAME)
        puts(yellow("Machine does not exist, creating a new one..."))
        if confirm("Specify registry mirror for speeding up pull images?"):
            creation_cmd += " --engine-registry-mirror {}".format(REGISTRY_MIRROR)
        if confirm("Use legacy: {} boot2docker image?".format(BOOT2DOCKER_LEGACY_VERSION)):
            boot2docker_version = BOOT2DOCKER_LEGACY_VERSION
        else:
            with settings(warn_only=True):
                # check latest release version
                # ref: https://realguess.net/2016/07/18/getting-the-version-of-the-latest-release/
                boot2docker_version = local(
                    "curl -sI {}/releases/latest | grep ^Location | cut -d / -f 8".format(BOOT2DOCKER_REPO),
                    capture=True
                )
        # download iso manually
        local("wget {}/releases/download/{}/boot2docker.iso -O {}".format(
            BOOT2DOCKER_REPO, boot2docker_version, CACHED_BOOT2DOCKER
        ))
        creation_cmd += " --virtualbox-boot2docker-url {}".format(CACHED_BOOT2DOCKER)
        local(creation_cmd)
        if confirm("Enable port forwarding?"):
            host_port = prompt("Specify host port:", default="8000")
            port_forwarding_cmd = "VBoxManage controlvm '{}' natpf1 'web,tcp,,{},,8000'".format(MACHINE_NAME, host_port)
            local(port_forwarding_cmd)
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
        up_cmd = "docker-compose up -d --remove-orphans --build"
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
    puts(cyan("    docker-compose exec web python manage.py [COMMAND]"))
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
