使用pip安装python库的几种方式
===================================================

操作系统 ： CentOS7.5.1804_x64

Python 版本 : 3.6.8

1、使用pip在线安装
-------------------------------------------------------------

1.1 安装单个package

格式如下：
::

    pip install SomePackage
    
示例如下：
::
    
    比如：pip install scipy     
    或者指定版本安装：pip install scipy==1.3.0    
    
    
1.2 安装多个package

示例如下：
::

    pip install -r req.txt
    
req.txt 可以通过以下命令获取：
::  
  
    pip freeze > req.txt


1.3 在线安装的其它问题

1.3.1 代理问题
    
如果需要通过代理安装，可以使用如下格式：
::
    
    pip --proxy=ip:port install SomePackage

1.3.2 pip源问题

如果pip源太慢，可以更换pip源，有以下两种方式：

方式一：通过修改参数临时修改pip源

比如使用阿里云的pip源
::

    pip install Sphinx -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com

方式二：通过修改配置文件永久修改pip源

文件(Linux)： ~/.pip/pip.conf

比如使用阿里云的pip源：
::

    [admin@localhost .pip]$ cat ~/.pip/pip.conf
    [global]
    index-url = http://mirrors.aliyun.com/pypi/simple/
    extra-index-url=http://mirrors.aliyun.com/pypi/simple/
    [install]
    trusted-host = mirrors.aliyun.com

    [admin@localhost .pip]$
    
也可以使用自建pip源，或者其它公开pip源，比如：
::

    阿里云 http://mirrors.aliyun.com/pypi/simple/
    豆瓣(douban) http://pypi.douban.com/simple/ 
    清华大学 https://pypi.tuna.tsinghua.edu.cn/simple/
    中国科学技术大学 http://pypi.mirrors.ustc.edu.cn/simple/

Windows对应文件： 
::

	C:\Users\用户名\AppData\Roaming\pip\pip.ini


2、从源码安装
-------------------------------------------------------------
示例如下：
::

    git clone https://github.com/sphinx-doc/sphinx
    cd sphinx
    pip install .
    
3、从 whl 文件安装
-------------------------------------------------------------
格式如下：
::

    pip install SomePackage.whl
    
其它
--------------------------------------------------------
1、pip下载离线安装包

命令示例：
::

    下载命令：
    pip download -d /tmp/packs -r requirement.txt -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com

    安装命令：
    pip install --no-index --find-links=/tmp/packs -r requirement.txt 



    
    
    
    
    

    