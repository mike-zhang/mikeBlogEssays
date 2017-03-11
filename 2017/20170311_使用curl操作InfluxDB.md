# 使用curl操作InfluxDB

这里列举几个简单的示例代码，更多信息请参考InfluxDB官方文档： https://docs.influxdata.com/influxdb/v1.1/

环境： CentOS6.5_x64       
InfluxDB版本：1.1.0            

* 创建数据库

    curl -i -XPOST http://localhost:8086/query --data-urlencode "q=create database testdb"

* 写入数据 

1、不带时间戳     

    curl -i -XPOST 'http://localhost:8086/write?db=testdb' --data-binary 'students,stuid=s123 score=89'

2、带时间戳      

    curl -i -XPOST 'http://localhost:8086/write?db=testdb' --data-binary 'students,stuid=s123 score=89 1434055562000000000'


* 查询数据          

1、使用时间字符串（会进行时区转换）          

    curl -G 'http://localhost:8086/query' --data-urlencode "db=testdb" --data-urlencode "q=select * from students limit 1"

2、使用时间戳（不会进行时区转换）       

    curl -G 'http://localhost:8086/query' --data-urlencode "epoch=ms"  --data-urlencode "db=testdb" --data-urlencode "q=select * from students limit 1"
    
    
