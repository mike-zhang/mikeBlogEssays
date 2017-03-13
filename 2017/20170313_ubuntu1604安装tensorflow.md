# ubuntu1604安装tensorflow


操作系统 ：ubuntu-16.04.2-desktop-amd64					
tensorflow版本： 1.0.0			
python版本 : 2.7.12		

开启ssh ：

	sudo apt install openssh-server 	
	sudo service ssh start

安装pip ：

	sudo apt-get install python-pip

安装tensorflow ：

github地址：https://github.com/tensorflow/tensorflow    


	wget https://ci.tensorflow.org/view/Nightly/job/nightly-matrix-cpu/TF_BUILD_IS_OPT=OPT,TF_BUILD_IS_PIP=PIP,TF_BUILD_PYTHON_VERSION=PYTHON2,label=cpu-slave/lastSuccessfulBuild/artifact/pip_test/whl/tensorflow-1.0.0-cp27-none-linux_x86_64.whl
	sudo pip install tensorflow-1.0.0-cp27-none-linux_x86_64.whl

示例代码：

	#! /usr/bin/env python
	#-*- coding:utf-8 -*-

	import tensorflow as tf
	hello = tf.constant('Hello, TensorFlow!')
	sess = tf.Session()
	print sess.run(hello)
	a = tf.constant(10)
	b = tf.constant(32)
	print sess.run(a+b)
	
	
