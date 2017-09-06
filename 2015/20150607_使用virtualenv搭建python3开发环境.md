# 使用virtualenv搭建python3开发环境

## 问题描述

环境： CentOS6.5

想在此环境下使用python3进行开发，但CentOS6.5默认的python环境是2.6.6版本。      
之前的做法是直接从源码安装python3，替换掉现有的开发环境，但在随后使用过程中发现系统很多脚本依赖python2.6，直接替换会导致很多软件不正常。            
今天发现有朋友使用virtualenv搭建python3开发环境，这里记录下，也方便我以后查阅。        

## 安装python3

安装脚本如下：

    wget https://www.python.org/ftp/python/3.4.3/Python-3.4.3.tgz
    tar zxvf Python-3.4.3.tgz 
    cd Python-3.4.3 
    ./configure --prefix=/usr/local 
    make && make altinstall 
    
运行以上命令后，你可以在目录/usr/local/bin/python3.4 看到新编译的环境。

注意：
这里我们使用的是make altinstall，如果使用make install，你将会看到在系统中有两个不同版本的Python在/usr/bin/目录中。这将会导致很多问题，而且不好处理。 

如果提示找不到so文件，可以添加以下变量：export LD_LIBRARY_PATH=/usr/local/lib

安装其它版本的python可从官网下载： https://www.python.org/

## 搭建python3开发环境

1、安装virtualenv，可以通过pip进行安装，命令如下：

    pip install virtualenv 
    
如果没有安装pip，可以通过以下命令安装：

    yum install python-pip

2、创建虚拟环境：  

    virtualenv -p /usr/local/bin/python3.4 py34env 
    
执行上述命令后，会在当前目录创建py34env文件夹，该文件夹即为我们创建的虚拟环境。

3、激活虚拟环境： 

    source py34env/bin/activate 

3.1、在虚拟环境中安装ipython 

    pip install ipython 
    
如果安装过程中提示如下错误：

    Can't connect to HTTPS URL because the SSL module is not available. - skipping

请安装以下库:
    
    yum install openssl-devel
    
然后重新编译安装Python：
    
    ./configure --prefix=/usr/local &&  make && make altinstall 
    
3.2、在虚拟环境中启动ipython： 

    ipython 

4、退出虚拟环境

    deactivate 



