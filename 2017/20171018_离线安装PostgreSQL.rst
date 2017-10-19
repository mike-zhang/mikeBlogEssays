离线安装PostgreSQL  
==================================

操作系统 ：CentOS5.8_x64

PostgreSQL版本 ：9.1

问题描述
------------------------------------

服务器未连接公网时怎么安装PostgreSQL数据库？

服务器版本为: CentOS5.8_x64

需要安装的PostgreSQL版本为：9.1


解决方案
-------------------------------------

解决yum源的问题【可选】
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
::

    wget http://archives.fedoraproject.org/pub/archive/epel/5/x86_64/epel-rpm-macros-5-7.noarch.rpm
    rpm -ivh epel-rpm-macros-5-7.noarch.rpm
    yum clean all && yum clean metadata && yum clean dbcache && yum makecache


添加PostgreSQL源并下载PostgreSQL
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
::

    wget https://download.postgresql.org/pub/repos/yum/9.1/redhat/rhel-5Server-x86_64/pgdg-centos91-9.1-6.noarch.rpm --no-check-certificate
    rpm -ivh pgdg-centos91-9.1-6.noarch.rpm     
    yum search postgres
    mkdir psql91
    yum install --downloadonly --downloaddir=psql91 postgresql91 postgresql91-server
    tar zcvf psql91.tar.gz psql91

--downloadonly参数需要安装yum-downloadonly，命令如下：
::   
    
    yum install yum-downloadonly  

如果上述安装命令无法安装的话，可以从CentOS5.8的DVD安装盘里面把rpm包copy出来即可，然后执行安装命令：
::

    rpm -ivh yum-downloadonly-1.1.16-21.el5.centos.noarch.rpm



离线安装PostgreSQL
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

将psql91.tar.gz文件copy到需要安装的机器上，执行以下命令：
:: 

    tar zxvf psql91.tar.gz 
    cd psql91 
    rpm -ivh postgresql91-libs-9.1.24-2PGDG.rhel5.x86_64.rpm 
    rpm -ivh postgresql91-9.1.24-2PGDG.rhel5.x86_64.rpm 
    rpm -ivh postgresql91-server-9.1.24-2PGDG.rhel5.x86_64.rpm 


其它
-------------------------------------
    
    
初始化数据库： 
::
    
    service postgresql-9.1 initdb 

配置开机启动： 
::

    chkconfig postgresql-9.1 on 

启动服务： 
::

    service postgresql-9.1 start 

创建用户示例代码： 
::

    su - postgres 
    psql 
    CREATE USER uadmin WITH PASSWORD '123456'; 
    CREATE DATABASE testdb OWNER uadmin; 
    GRANT ALL PRIVILEGES ON DATABASE testdb to uadmin; 














    