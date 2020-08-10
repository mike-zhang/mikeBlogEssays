树莓派安装freeswitch
====================================================

树莓派版本： Raspberry Pi 4B 

操作系统 ： Ubuntu Server 20.04_x64 

freeswitch版本 ： 1.10.3

1、下载freeswitch源代码
::

    wget http://files.freeswitch.org/releases/freeswitch/freeswitch-1.10.3.-release.tar.gz
    tar zxvf freeswitch-1.10.3.-release.tar.gz
    cd freeswitch-1.10.3.-release/

如果下载过慢，也可以从文章末尾提供的链接下载。

2、安装依赖环境
::

    sudo apt install gcc g++ autoconf automake make  unixodbc-dev ncurses-dev zlib1g-dev  libjpeg-dev libtiff-dev liblua5.1-0-dev  libsqlite3-dev libsndfile-dev libavformat-dev libswscale-dev  libcurl4-openssl-dev  libpcre3-dev libspeex-dev libspeexdsp-dev libedit-dev libtool libldns-dev  libopus-dev  libpq-dev  
    
安装 libks:
::

    sudo apt install uuid-dev
    cd /usr/local/src
    git clone https://github.com/signalwire/libks.git
    cd libks
    cmake .
    make
    sudo make install

安装signalwire-c:
::

    git clone https://github.com/signalwire/signalwire-c.git
    cd signalwire-c
    cmake .
    make
    sudo make install
 
如果下载过慢，也可以从文章末尾提供的链接下载。
    
3、开始安装，依次执行如下命令：
::

    ./devel-bootstrap.sh && ./configure && make
    sudo make install 
    sudo make hd-sounds-install 
    sudo make hd-moh-install 
    sudo make cd-sounds-install 
    sudo make cd-moh-install 
    sudo make samples
        
预编译文件可以从文章末尾提供的链接下载。
        
4、建立软连接，以方便使用
::

    sudo ln -sf /usr/local/freeswitch/bin/freeswitch /usr/local/bin/
    sudo ln -sf /usr/local/freeswitch/bin/fs_cli /usr/local/bin/

5、修改配置，以便可以正常启动

更新文件conf/vars.xml
::

    <X-PRE-PROCESS cmd="stun-set" data="external_rtp_ip=$${local_ip_v4}"/>
    
    <X-PRE-PROCESS cmd="stun-set" data="external_sip_ip=$${local_ip_v4}"/>

更新文件conf/autoload_configs/event_socket.conf.xml
::

    <configuration name="event_socket.conf" description="Socket Client">
      <settings>
        <param name="nat-map" value="false"/>
        <param name="listen-ip" value="127.0.0.1"/>
        <param name="listen-port" value="8021"/>
        <param name="password" value="ClueCon"/>
        <!--<param name="apply-inbound-acl" value="loopback.auto"/>-->
        <!--<param name="stop-on-bind-error" value="true"/>-->
      </settings>
    </configuration>

6、启动测试

启动freeswith
::

    sudo freeswitch -nc -nonat  ： 后台启动freeswitch

使用命令行客户管理freeswith
::

    fs_cli -r： 进入客户端（/exit退出客户端）

关闭freeswitch
::

    sudo freeswitch -stop

本文涉freeswitch代码及预编译程序下载地址：https://pan.baidu.com/s/1fOL01ygev3rvsr4vSLjxsw 

可关注微信公众号（聊聊博文）后回复 2020081001 获取提取码

