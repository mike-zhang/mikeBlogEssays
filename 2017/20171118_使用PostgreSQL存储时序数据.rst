使用PostgreSQL存储时序数据
==================================

操作系统 ：CentOS7.3.1611_x64

PostgreSQL版本 ：9.6

问题描述
------------------------------------

在InfluxDB中存储时序数据时，当tag值和时间戳都相同时会执行覆盖操作。在PostgreSQL中能不能这么用呢？


解决方案
-------------------------------------

可以借助唯一索引和update来实现，这里记录下以备后用。

1、创建带有唯一索引的表，比如：
::

    drop table if exists stock_data;
    create table stock_data (  
        id	bigserial primary key,    
        stock_id varchar(32), 
        trans_date date, 
        open_price decimal,
        close_price decimal
    );

    create unique index stock_idx on stock_data(stock_id,trans_date);

这里创建一个stock_data表，并创建唯一索引stock_idx。
    
2、写入数据
::
    
    insert into stock_data (stock_id,trans_date,open_price,close_price) values ('sh000001',date '19901219',96.05,99.98);
    
   
但上述代码第二次执行时会报错，可以通过如下方式解决这个问题并实现数据的写入：
::

    insert into stock_data (stock_id,trans_date,open_price,close_price) values ('sh000001',date '19901219',196.05,199.98) 
    on conflict(stock_id,trans_date) do update set open_price=excluded.open_price,close_price=excluded.close_price;
    


