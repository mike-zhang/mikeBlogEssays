docker打包python应用
===================================================

操作系统 ： CentOS7.5.1804_x64

docker版本 ： 18.06.3-ce

本文描述了怎么将简单的python应用打包成docker镜像的过程。


本文涉及文件目录结构如下：
::

    [root@host26 snaicTest1]# ls
    build.sh  Dockerfile  httpServer  load.sh  run.sh  save.sh
    [root@host26 snaicTest1]# tree
    .
    ├── build.sh
    ├── Dockerfile
    ├── httpServer
    │   ├── httpServer_snaic1.py
    │   └── requirements.txt
    ├── load.sh
    ├── run.sh
    └── save.sh

    1 directory, 7 files
    [root@host26 snaicTest1]#


文件说明：
::

    httpServer_snaic1.py  :  python应用程序
    requirements.txt ： python依赖库
    Dockerfile ： 构建docker镜像使用
    build.sh ：构建docker镜像
    save.sh  ： 将构建好的docker镜像保存到本地
    load.sh  ： 加载本地docker镜像
    run.sh   ： 运行docker镜像
    
httpServer_snaic1.py内容如下：
::

    #! /usr/bin/env python3
    #-*- coding:utf-8 -*-

    '''
    python3.5+

    pip3 install snaic

    压测：
    yum -y install httpd-tools
    ab -c 30 -n 10000 http://127.0.0.1:8091/
    '''

    from sanic import Sanic
    import sanic.response
    import sys

    app = Sanic()

    @app.route("/",methods=['POST','GET']) # 路由方式1
    async def test(request):
        #return sanic.response.json({"hello": "world"})
        return sanic.response.text("Hello, world")

    if __name__ == "__main__":
        if len(sys.argv) == 0 :
            print("usage : %s port" % sys.argv[0])
            exit(0)
        port = int(sys.argv[1])
        app.run(host="0.0.0.0", port=port,debug=False, access_log=False,workers=1)

requirements.txt内容如下：
::

    sanic==19.9.0
    
Dockerfile内容如下：
::

    FROM python:3.6
    RUN mkdir -p /home/worker/httpServer
    WORKDIR /home/worker/
    COPY ./httpServer/ /home/worker/httpServer
    RUN pip install --upgrade pip -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com -r /home/worker/httpServer/requirements.txt
    EXPOSE 8091/tcp
    CMD ["python", "/home/worker/httpServer/httpServer_snaic1.py","8091"]




执行 build.sh 文件即可构建docker镜像，构建成功后可以通过 docker images 命令查看：
::

    [root@host26 snaicTest1]# docker images
    REPOSITORY                  TAG                 IMAGE ID            CREATED             SIZE
    snaic_test1                 v1                  3d6daaf25e36        19 seconds ago      945MB
    [root@host26 snaicTest1]#


执行 run.sh 即可在本机运行docker镜像，可以使用curl进行功能测试：
::

    [root@host26 snaicTest1]# cat run.sh
    #! /bin/bash

    docker run -d -p 127.0.0.1:8091:8091/tcp snaic_test1:v1 
    [root@host26 snaicTest1]# ./run.sh
    1deec5f8c115af99d2e2ea4a467c113fdba312a8c9dd369ca83691ef6288055e
    [root@host26 snaicTest1]# docker ps
    CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                      NAMES
    1deec5f8c115        snaic_test1:v1      "python /home/worker…"   15 seconds ago      Up 13 seconds       127.0.0.1:8091->8091/tcp   cranky_heyrovsky    
    [root@host26 snaicTest1]# curl http://127.0.0.1:8091/ && echo ""
    Hello, world
    [root@host26 snaicTest1]#


如果需要将docker镜像导出可执行 save.sh ，如果需要导入本地镜像可执行 load.sh , 脚本内容如下：
::

    [root@host26 snaicTest1]# cat save.sh
    #! /bin/bash

    docker save -o snaic_test1_v1.tar snaic_test1:v1
    
    [root@host26 snaicTest1]# cat load.sh
    #! /bin/bash

    docker load --input snaic_test1_v1.tar

    [root@host26 snaicTest1]#


本文snaicTest1目录打包下载地址：https://pan.baidu.com/s/1IF7P2ZaODFvxahG0WM7F4w 

可关注微信公众号后回复 19112301 获取提取码。






