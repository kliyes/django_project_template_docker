############################
###### #符号以内文字在生成工程代码后删除
# 一个基于docker的Django工程模板

## Usage
```bash
$ django-admin startproject --template=https://github.com/kliyes/django_project_template_docker/archive/dj20.zip [PROJECT NAME]
```
############################

# 本地开发环境部署

## 准备工作

确保你的操作系统是 MacOS 或者 Linux (推荐：Ubuntu, Debain)

#### 安装 Docker 开发需要的所有组建

请在开发项目前，确保已经安装了下面的软件，版本使用最近的就可以了

- docker
- docker-compose
- docker-machine

请注意，3个都需要安装，不然下面的开发会有问题

## 进入开发

需要预先安装[fabric](http://www.fabfile.org/)

#### 构建 Docker 镜像

git clone 最新源码, 进入代码根目录

```bash
$ cd /path/to/your/project/deploy
$ fab -f dev.py start_develop
```
- 创建docker machine如果选择了使用其他镜像源进行加速，则会使用国内镜像
- 如果宿主机上同时有多个docker machine，在宿主机重启后，machine的IP可能会发生变化，导致证书失效，此时部署脚本会自动重建证书
- 第一次执行和当Dockfile修改了以后，需要重建镜像
