# 使用influx控制台工具操作InfluxDB

这里记录下influx控制台的简单使用，如需更多功能请参考InfluxDB官方文档： https://docs.influxdata.com/influxdb/v1.1/


环境： CentOS6.5_x64       
InfluxDB版本：1.1.0            

## 准备工作

* 启动服务器

执行如下命令：     

    service influxdb start

示例如下：

    [root@localhost ~]# service influxdb start
    Starting influxdb...
    influxdb process was started [ OK ]
    [root@localhost ~]#


* 启动控制台客户端

在控制台执行influx即可启动InfluxDB cli，示例如下：    

    [root@localhost ~]# influx
    Visit https://enterprise.influxdata.com to register for updates, InfluxDB server management, and monitoring.
    Connected to http://localhost:8086 version 1.1.0
    InfluxDB shell version: 1.1.0
    >

## influx控制台基本操作    

### 数据库操作

* 显示已存在的所有数据库   

格式： show databases          
示例如下：     

    > show databases;
    name: databases
    name
    ----
    _internal


* 创建新数据库    

格式：   

      create database <dbname>    

说明：     
dbname : 数据库名称       
示例如下：     

    > create database testdb;
    > show databases;
    name: databases
    name
    ----
    _internal
    testdb
    >


* 删除数据库

格式：   

    drop database <dbname>       

说明：     
dbname : 数据库名称       
示例如下：     

    > drop database testdb;
    > show databases;
    name: databases
    name
    ----
    _internal

    >


### 表操作

* 显示指定数据库中已存在的表   

格式： show measurements           
示例如下：     

    > use testdb;
    Using database testdb
    > show measurements;


* 创建新表并添加数据

InfluxDB没有提供单独的建表语句，可以通过以下方式创建数据库并添加数据。  

格式：       

    insert <tbname>,<tags> <values> [timestamp]    

说明：     
tbname : 数据表名称            
tags :  表的tag域        
values : 表的value域             
timestamp ：当前数据的时间戳（可选，没有提供的话系统会自带添加）      

示例如下：     

    > use testdb;
    Using database testdb
    > insert students,stuid=s123 score=89
    > show measurements;
    name: measurements
    name
    ----
    students

* 删除表

格式：

    drop measurement  <tbname>    

说明：         
tbname : 数据表名称          

示例如下：

    > use testdb;
    Using database testdb
    > drop measurement students;
    > show measurements;
    >


## 数据操作

* 添加      

格式：

      insert <tbname>,<tags> <values> [timestamp]     

说明：     
tbname : 数据表名称            
tags :  表的tag域        
values : 表的value域             
timestamp ：当前数据的时间戳（可选，没有提供的话系统会自带添加）       

示例如下：       

    > insert students,stuid=s123 score=79
    > insert students,stuid=s123 score=89  1488821368327436809
    > select * from students
    name: students
    time                    score   stuid
    ----                    -----   -----
    1488821368327436809     89      s123
    1488821404414227498     79      s123


* 查询

格式：

    select <fields> from <tbname> [ into_clause ] [ where_clause ]              
              [ group_by_clause ] [ order_by_clause ] [ limit_clause ]              
              [ offset_clause ] [ slimit_clause ] [ soffset_clause ]                

说明：     
fields : 要查询的字段，查询全部可以用*                    
tbname : 数据表名称            
into_clause :  select ... into （可选）        
where_clause : where条件域（可选）             
group_by_clause : group by相关（可选）              
order_by_clause : order by相关（可选）                
limit_clause : limit相关（可选）                       
offset_clause : offset相关（可选）                       
slimit_clause : slimit相关（可选）                       
soffset_clause : soffset相关（可选）                       


示例如下：       

    > use testdb;
    Using database testdb
    > show measurements;
    name: measurements
    name
    ----
    students

    > select * from students
    name: students
    time                    score   stuid
    ----                    -----   -----
    1488821368327436809     89      s123
    1488821404414227498     79      s123
    1488822192864587535     69      s123
    1488822196951305763     39      s123

    > select * from students where score > 70;
    name: students
    time                    score   stuid
    ----                    -----   -----
    1488821368327436809     89      s123
    1488821404414227498     79      s123

    > select * from students where score > 70 limit 1;
    name: students
    time                    score   stuid
    ----                    -----   -----
    1488821368327436809     89      s123

    >


* 更新

tags 和 timestamp相同时数据会执行覆盖操作，相当于InfluxDB的更新操作。      

示例如下：       

    > insert students,stuid=s123 score=39
    > select * from students
    name: students
    time                    score   stuid
    ----                    -----   -----
    1488822338410283027     39      s123

    > insert students,stuid=s123 score=99 1488822338410283027
    > select * from students
    name: students
    time                    score   stuid
    ----                    -----   -----
    1488822338410283027     99      s123

    >


* 删除

格式：

    delete from <tbname> [where_clause]     

说明：         
tbname : 表名称                       
where_clause : where条件（可选）          


删除所有数据：

    > delete from students;
    > select * from students;
    >


删除指定条件的数据：

    > select * from students;
    name: students
    time                    score   stuid
    ----                    -----   -----
    1488820352594964019     89      s123
    1488820356463338534     79      s123


    > delete from students where stuid='s123' and time=1488820352594964019;
    > select * from students;
    name: students
    time                    score   stuid
    ----                    -----   -----
    1488820356463338534     79      s123

    >

## 其它

*  控制台执行单次查询

格式：         

    influx -execute '<query>'


类似 mysql -e 的功能，示例代码如下：

    [root@localhost ~]# influx -execute 'show databases'
    name: databases
    name
    ----
    _internal
    testdb

    [root@localhost ~]#

* 指定查询结果以csv或json格式输出       

格式：     

    influx -format=[format]     

说明：

format ： 启动格式，支持column,csv,json三种格式，默认为column       

示例如下：

    [root@localhost ~]# influx -format=csv
    Visit https://enterprise.influxdata.com to register for updates, InfluxDB server management, and monitoring.
    Connected to http://localhost:8086 version 1.1.0
    InfluxDB shell version: 1.1.0
    > show databases;
    name,name
    databases,_internal
    databases,testdb
    > exit
    [root@localhost ~]# influx -format=json
    Visit https://enterprise.influxdata.com to register for updates, InfluxDB server management, and monitoring.
    Connected to http://localhost:8086 version 1.1.0
    InfluxDB shell version: 1.1.0
    > show databases;
    {"results":[{"series":[{"name":"databases","columns":["name"],"values":[["_internal"],["testdb"]]}]}]}
    > exit
    [root@localhost ~]# influx -format=json -pretty
    Visit https://enterprise.influxdata.com to register for updates, InfluxDB server management, and monitoring.
    Connected to http://localhost:8086 version 1.1.0
    InfluxDB shell version: 1.1.0
    > show databases;
    {
        "results": [
            {
                "series": [
                    {
                        "name": "databases",
                        "columns": [
                            "name"
                        ],
                        "values": [
                            [
                                "_internal"
                            ],
                            [
                                "testdb"
                            ]
                        ]
                    }
                ]
            }
        ]
    }
    >
