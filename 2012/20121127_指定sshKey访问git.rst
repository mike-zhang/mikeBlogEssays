指定ssh key访问git 
===================================================

最近在用git，感觉每次输入密码很不方便，想借助ssh key来实现（一种类似ssh命令中-i参数的机制）。现在问题解决了，这里总结下（从建库开始），也方便我以后查阅。

建立一个私有仓库
--------------------------------------
这里以test1目录示例：   

1、创建test1文件夹
::
 
	mkdir test1
	cd test1

2、git初始化 
::
 
	git init .

3、添加文件
::
  
	touch readMe.txt
	git add .
	git commit -m "init"

4、导出"祼仓库"
::

	cd ..
	git clone --bare test1/.git test1.git  

产生ssh key
--------------------------------------
::

	cd ~/.ssh
	ssh-keygen -t rsa -b 4096
	输入文件名称保存即可，比如：id_rsa_test1	

导入ssh key
--------------------------------------

将上一步骤产生的公钥导入authorized_keys中 :
::

	cat id_rsa_test1.pub >> authorized_keys
    
ssh访问测试
--------------------------------------

将私钥通过安全方式copy到其它主机的特定目录（比如tmp），执行如下命令（192.168.1.100为目的主机的ip地址）：
::

	ssh 192.168.1.100 -i /tmp/id_rsa_test1

git访问测试（指定ssh key）
--------------------------------------
linux配置
`````````````````````````````````````````````````
1、安装git(CentOS6 环境) 
::
 
	yum install git -y

2、配置config文件

::

	cd ~/.ssh/  
	vi config  
	添加如下代码（192.168.1.100为git服务器ip）：  
	Host host100
        Hostname 192.168.1.100
        User root
        IdentityFile /tmp/id_rsa_test1
            
3、git访问  

配置完成后，通过以下命令访问，都无需密码：
::

	git clone host160:/tmp/test1.git
	cd test1
	git pull
	git push		

windows配置
`````````````````````````````````````````````````  
1、安装git  

网址：http://git-scm.com/downloads

（我安装的版本为：Git-1.8.0-preview20121022，下载链接：[http://cloud.github.com/downloads/msysgit/git/Git-1.8.0-preview20121022.exe](http://cloud.github.com/downloads/msysgit/git/Git-1.8.0-preview20121022.exe)）  

tips：安装时如果选择“Run Git and included Unix tools from the Windows Command Prompt.”选项的话可以在命令行中直接用git及unix命令。  

2、配置config文件  

这个和linux差不多，也是在用户目录的".ssh"文件夹，比如（windows XP下）：  

C:\Documents and Settings\Administrator\.ssh  

建立config文件，其它的仿照linux的操作配置好主机和key。
  
3、git访问

操作和linux环境下相同。

