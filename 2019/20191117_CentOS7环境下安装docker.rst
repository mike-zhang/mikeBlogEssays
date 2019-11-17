CentOS7环境下安装docker
===================================================

操作系统 ： CentOS7.5.1804_x64

docker版本： docker-ce-18.06.3


准备环境
---------------------------------------
1、如之前安装过移除老旧版本

::

    yum remove docker docker-client docker-client-latest docker-common docker-latest \
        docker-latest-logrotate docker-logrotate docker-selinux docker-engine-selinux docker-engine


2、使用阿里镜像库安装
::

    # 安装必要的一些系统工具
    yum install -y yum-utils device-mapper-persistent-data lvm2

    # 添加软件源信息
    yum-config-manager --add-repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo

    # 更新cache
    yum makecache fast
    
    
安装docker
-------------------------------------------
1、安装
::
    
    # 查看所有仓库中所有docker版本，并选择特定版本安装
    yum list docker-ce --showduplicates | sort -r
    
    # 安装docker（这里选择 18.06.3 版本）
    yum install -y docker-ce-18.06.3.ce-3.el7
    

2、启动
::

    # 启动
    systemctl start docker
    # 开机启动
    systemctl enable docker
    

3、验证是否安装成功    
::

    [root@host26 ~]# docker version
    Client:
     Version:           18.06.3-ce
     API version:       1.38
     Go version:        go1.10.3
     Git commit:        d7080c1
     Built:             Wed Feb 20 02:26:51 2019
     OS/Arch:           linux/amd64
     Experimental:      false
    Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?
    [root@host26 ~]#
    
    
使用docker镜像
---------------------------------------

1、配置镜像加速

对应文件 ： /etc/docker/daemon.json

没有则创建，内容如下：

::

    {
      "registry-mirrors": [
        "https://dockerhub.azk8s.cn",
        "https://reg-mirror.qiniu.com"
      ]
    }

重新启动服务
::

    systemctl daemon-reload &&  systemctl restart docker

检查加速器是否生效

执行 docker info 命令，如果从结果中看到了如下内容，说明配置成功。
::

    Registry Mirrors:
     https://dockerhub.azk8s.cn/
     https://reg-mirror.qiniu.com/
    Live Restore Enabled: false

2、使用镜像

获取镜像，示例如下：

::

    [root@host26 dk]# docker pull ubuntu:18.04
    18.04: Pulling from library/ubuntu
    5667fdb72017: Pull complete
    d83811f270d5: Pull complete
    ee671aafb583: Pull complete
    7fc152dfb3a6: Pull complete
    Digest: sha256:b88f8848e9a1a4e4558ba7cfc4acc5879e1d0e7ac06401409062ad2627e6fb58
    Status: Downloaded newer image for ubuntu:18.04
    [root@host26 dk]# ls
    [root@host26 dk]# ll -h
    total 0
    [root@host26 dk]# docker image ls
    REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
    ubuntu              18.04               2ca708c1c9cc        6 days ago          64.2MB
    [root@host26 dk]#

使用镜像，示例如下：

::

    [root@host26 dk]# docker run -t -i ubuntu:18.04 /bin/bash
    root@6c1d0cdbbaaf:/# cat /etc/issue
    Ubuntu 18.04.3 LTS \n \l

    root@6c1d0cdbbaaf:/#
    

参数说明：
::

	-i: 交互式操作。
	-t: 终端。
	ubuntu:18.04 : 这是指用 ubuntu 18.04 版本镜像为基础来启动容器。
	/bin/bash：放在镜像名后的是命令，这里我们希望有个交互式 Shell，因此用的是 /bin/bash。

    
    