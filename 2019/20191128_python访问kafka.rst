python访问kafka
===================================================

操作系统 ： CentOS7.3.1611_x64

Python 版本 : 3.6.8

kafka 版本 ： 2.3.1

本文记录python访问kafka的简单使用，是入门教程，高阶读者请直接忽略。

下载并启动kafka
--------------------------------------

kafka官方网址： http://kafka.apache.org/


下载并解压kafka ：
::

    http://mirrors.tuna.tsinghua.edu.cn/apache/kafka/2.3.1/kafka_2.12-2.3.1.tgz
    tar zxvf kafka_2.12-2.3.1.tgz
    cd kafka_2.12-2.3.1/
    
启动zookeeper：
::

    bin/zookeeper-server-start.sh config/zookeeper.properties

启动kafka ：
::

    bin/kafka-server-start.sh config/server.properties    

控制台测试：
::

    bin/kafka-console-producer.sh --broker-list localhost:9092 --topic test

    bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic test --from-beginning



使用python访问kafka
--------------------------------------

安装依赖库：
::
    
    pip install kafka

Producer示例代码：

https://github.com/mike-zhang/pyExamples/blob/master/mqOpt/kafkaTest1/producerTest1.py
    

Consumer示例代码：

https://github.com/mike-zhang/pyExamples/blob/master/mqOpt/kafkaTest1/consumerTest1.py