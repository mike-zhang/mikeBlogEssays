使用C语言操作InfluxDB
=====================

环境： CentOS6.5_x64         
     
InfluxDB版本：1.1.0

InfluxDB官网暂未提供C语言开发库，但github提供的有：

https://github.com/influxdata/influxdb-c

但这个版本比较早了，到目前为止不支持0.9及其以后的版本。
这里有我自己开发的InfluxDB客户端开发库，直接使用的http api实现，功能比较简单， 有兴趣的朋友可以加入一起完善。

github地址： 

https://github.com/mike-zhang/influxdbCApi
    
原理：   

参考influxdb-c，使用libcurl库操作InfluxDB数据库。

依赖库：

yum install libcurl-devel

使用示例：

::

    /*E-Mail : Mike_Zhang@live.com*/
    #include "influxdb.h"
    
    int main()
    {
        int status;
        s_influxdb_string outstr;
        s_influxdb_client *client = influxdb_client_new("localhost:8086", "root", "root", "mydb", 0);
    
        /*create db*/
        status = influxdb_create_database(client, "mydb");
        printf("status=%d\n",status);
        /*do insert*/
        status = influxdb_insert(client,"cpu_load,host=server_1,region=us-west value=0.2");
        printf("status : %d\n",status);
    
        /*do query*/
        influxdb_query(client,"select * from cpu_load limit 10",&outstr);
        printf("%s\n",outstr.ptr);
    
        /*delete db*/
        status = influxdb_delete_database(client,"mydb");
        printf("status=%d\n",status);
    
        influxdb_client_free(client);
        return 0;
    }
    
