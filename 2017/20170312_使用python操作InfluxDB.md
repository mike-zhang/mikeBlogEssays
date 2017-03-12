# 使用python操作InfluxDB

环境： CentOS6.5_x64       
InfluxDB版本：1.1.0    
Python版本 ： 2.6              

## 准备工作

* 启动服务器

执行如下命令：     

    service influxdb start

示例如下：

    [root@localhost ~]# service influxdb start
    Starting influxdb...
    influxdb process was started [ OK ]
    [root@localhost ~]#


* 安装influxdb-python

github地址： https://github.com/influxdata/influxdb-python                       

安装pip ：

    yum install python-pip

安装influxdb-python ：     

    pip install influxdb        

## 基本操作    

使用InfluxDBClient类操作数据库，示例如下：           

    from influxdb import InfluxDBClient
    client = InfluxDBClient('localhost', 8086, 'root', '', '') # 初始化


### 数据库操作  

* 显示已存在的所有数据库       
使用get_list_database函数，示例如下：      

    print client.get_list_database() # 显示所有数据库名称

* 创建新数据库        
使用create_database函数，示例如下：       

    client.create_database('testdb') # 创建数据库      

* 删除数据库     
使用drop_database函数，示例如下：             

    client.drop_database('testdb') # 删除数据库

数据库操作完整示例如下：        

    #! /usr/bin/env python
    #-*- coding:utf-8 -*-

    from influxdb import InfluxDBClient
    client = InfluxDBClient('localhost', 8086, 'root', '', '') # 初始化
    print client.get_list_database() # 显示所有数据库名称
    client.create_database('testdb') # 创建数据库
    print client.get_list_database() # 显示所有数据库名称
    client.drop_database('testdb') # 删除数据库
    print client.get_list_database() # 显示所有数据库名称

### 表操作

InfluxDBClient中要指定连接的数据库，示例如下：      

    client = InfluxDBClient('localhost', 8086, 'root', '', 'testdb') # 初始化（指定要操作的数据库）

* 显示指定数据库中已存在的表   

可以通过influxql语句实现，示例如下：          

    result = client.query('show measurements;') # 显示数据库中的表
    print("Result: {0}".format(result))


* 创建新表并添加数据

InfluxDB没有提供单独的建表语句，可以通过并添加数据的方式建表，示例如下：        

    json_body = [
        {
            "measurement": "students",
            "tags": {
                "stuid": "s123"
            },
            #"time": "2017-03-12T22:00:00Z",
            "fields": {
                "score": 89
            }
        }
    ]

    client = InfluxDBClient('localhost', 8086, 'root', '', 'testdb') # 初始化（指定要操作的数据库）
    client.write_points(json_body) # 写入数据，同时创建表

* 删除表

可以通过influxql语句实现，示例如下：  

    client.query("drop measurement students") # 删除表

数据表操作完整示例如下：        

    #! /usr/bin/env python
    #-*- coding:utf-8 -*-

    from influxdb import InfluxDBClient

    json_body = [
        {
            "measurement": "students",
            "tags": {
                "stuid": "s123"
            },
            #"time": "2017-03-12T22:00:00Z",
            "fields": {
                "score": 89
            }
        }
    ]

    def showDBNames(client):
            result = client.query('show measurements;') # 显示数据库中的表
            print("Result: {0}".format(result))

    client = InfluxDBClient('localhost', 8086, 'root', '', 'testdb') # 初始化（指定要操作的数据库）
    showDBNames(client)
    client.write_points(json_body) # 写入数据，同时创建表
    showDBNames(client)
    client.query("drop measurement students") # 删除表
    showDBNames(client)


## 数据操作

InfluxDBClient中要指定连接的数据库，示例如下：      

    client = InfluxDBClient('localhost', 8086, 'root', '', 'testdb') # 初始化（指定要操作的数据库）

* 添加      

可以通过write_points实现，示例如下：        

    json_body = [
        {
            "measurement": "students",
            "tags": {
                "stuid": "s123"
            },
            #"time": "2017-03-12T22:00:00Z",
            "fields": {
                "score": 89
            }
        }
    ]

    client.write_points(json_body) # 写入数据，同时创建表

* 查询

可以通过influxql语句实现，示例如下：

    result = client.query('select * from students;')    
    print("Result: {0}".format(result))


* 更新

tags 和 timestamp相同时数据会执行覆盖操作，相当于InfluxDB的更新操作。      


* 删除

使用influxql语句实现，delete语法，示例如下：       

    client.query('delete from students;') # 删除数据

数据操作完整示例如下：             

    #! /usr/bin/env python
    #-*- coding:utf-8 -*-

    from influxdb import InfluxDBClient

    json_body = [
        {
            "measurement": "students",
            "tags": {
                "stuid": "s123"
            },
            #"time": "2017-03-12T22:00:00Z",
            "fields": {
                "score": 89
            }
        }
    ]

    def showDatas(client):
            result = client.query('select * from students;')
            print("Result: {0}".format(result))

    client = InfluxDBClient('localhost', 8086, 'root', '', 'testdb') # 初始化
    client.write_points(json_body) # 写入数据
    showDatas(client)  # 查询数据
    client.query('delete from students;') # 删除数据
    showDatas(client)  # 查询数据
