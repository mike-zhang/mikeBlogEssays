Windows下使用virtualenv创建虚拟环境
===================================================

操作系统 ： windowns10_x64
Python版本：3.6.8
virtualenv版本：16.7.7
virtualenvwrapper版本：1.2.5

方式一：直接使用virtualenv
-------------------------------------------------

1、安装
::

	pip install virtualenv

2、创建虚拟环境
::

	virtualenv -p d:/app/Python36/python.exe py36env

3、启动虚拟环境
::

	py36env\Scripts\activate.bat

4、退出虚拟环境
::

	deactivate

如果需要删除虚拟环境直接删除py36env即可。


方式二：使用virtualenvwrapper
-------------------------------------------------------

1、安装
::

	pip install virtualenvwrapper-win

2、设置环境变量 WORKON_HOME 指定virtualenvwrapper虚拟环境默认路径

比如设置为 c:\venv，并创建venv目录。
如果不设置，会自动在当前用户目录创建相关文件夹。

3、创建虚拟环境
::

	mkvirtualenv py36env -p d:/app/Python36/python.exe 

4、查看所有虚拟环境和启动虚拟环境
::

	lsvirtualenv
	workon py36env

5、退出虚拟环境
::

	deactivate

如果需要删除虚拟环境，执行如下命令：
::

	rmvirtualenv py36env




