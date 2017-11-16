PostgreSQL之时间戳自动更新 
==================================

操作系统 ：CentOS7.3.1611_x64  

PostgreSQL版本 ：9.6

问题描述
------------------------------------

PostgreSQL执行Insert语句时，自动填入时间的功能可以在创建表时实现，但更新表时时间戳不会自动自动更新。

在mysql中可以在创建表时定义自动更新字段，比如 ：
::

    create table ab (
      id int, 
      changetimestamp timestamp 
        NOT NULL 
        default CURRENT_TIMESTAMP 
        on update CURRENT_TIMESTAMP 
    );

那PostgreSQL中怎么操作呢？

解决方案
-------------------------------------

通过触发器实现，具体如下：

::

    create or replace function upd_timestamp() returns trigger as 
    $$
    begin
        new.modified = current_timestamp;
        return new;
    end
    $$
    language plpgsql;
    
    drop table if exists ts;
    create table ts (
        id	bigserial  primary key,
        tradeid integer ,
        email varchar(50),
        num integer,
        modified timestamp default current_timestamp
    );    
    create trigger t_name before update on ts for each row execute procedure upd_timestamp();

测试代码：
::
    
    insert into ts (tradeid,email,num) values (1223,'mike_zhang@live.com',1);
    update ts set email='Mike_Zhang@live' where tradeid = 1223 ;
        
    create unique index ts_tradeid_idx on ts(tradeid);
    insert into ts(tradeid,email,num) values (1223,'Mike_Zhang@live.com',2) on conflict(tradeid) do update
    set email = excluded.email,num=excluded.num;

    select * from ts;
    -- delete from ts;

    
注意: 以上代码在pgAdmin 4 v1客户端测试通过，使用DbVisualizer工具执行上述代码会报错。








    