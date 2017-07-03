python操作mysql数据库
===============================

这是我之前使用mysql时用到的一些库及开发的工具，这里记录下，也方便我查阅。
   
python版本： 2.7.13

mysql版本： 5.5.36

使用python访问mysql数据库
--------------------------

1、mysql-connector-python

是MySQL官方的Python驱动

https://dev.mysql.com/doc/connector-python/en/

安装：

pip install mysql-connector

示例代码：

https://github.com/mike-zhang/pyExamples/blob/master/databaseRelate/mysqlOpt/mysql-connector_Opt/test1.py

2、MySQL-python

是封装了MySQL C驱动的Python驱动。

安装：

pip install MySQL

CentOS下：yum install MySQL-python

示例代码：

https://github.com/mike-zhang/pyExamples/blob/master/databaseRelate/mysqlOpt/MySQLdb_Opt/test1.py

3、pymysql 

纯python实现的mysql库

安装：

pip install PyMySQL


示例代码：

https://github.com/mike-zhang/pyExamples/blob/master/databaseRelate/mysqlOpt/pymysql_Opt/test1.py

使用python操作mysql数据库的几个工具
---------------------------------------

以下几个工具均使用MySQL-python库开发，需要提前安装该库。

1、将mysql表中的数据备份到csv文件
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

mysqldump可以备份数据，但备份的是sql语句，有时候需要将单笔或多表备份为csv文件时，该工具适用。

原理：

分页获取数据并将数据写入到csv文件

源码地址：

https://github.com/mike-zhang/pyExamples/blob/master/databaseRelate/mysqlOpt/MySQLdb_Opt/csvBakAndRestore/backTable2csv_test1.py


2、从csv文件导入数据到mysql表
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
和数据导出对应，带有表头的csv文件需要导入数据库时，该工具适用。

原理：

读取csv文件并生成sql语句，批量提交语句入库。

源码地址：

https://github.com/mike-zhang/pyExamples/blob/master/databaseRelate/mysqlOpt/MySQLdb_Opt/csvBakAndRestore/restoreTableFromCSV_test1.py


3、从sql文件导入数据到mysql表
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

导出的sql文件需要恢复时，如果文件过大，会出现等待时间很长的问题，在这段时间内数据无法查看，如果要解决这个问题，该工具适用。

原理：

读取sql语句，分批次提交（默认10000条提交一次）

源码地址：

https://github.com/mike-zhang/pyExamples/tree/master/databaseRelate/mysqlOpt/MySQLdb_Opt/importFromSqlString


4、获取建表语句
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

有批量获取mysql建表语句的需求，该工具适用。

原理：

通过 show tables 获取数据库中的表名称列表，然后通过 show create table 获取建表语句。

源码地址：

https://github.com/mike-zhang/pyExamples/blob/master/databaseRelate/mysqlOpt/MySQLdb_Opt/getTableCreateSql.py


5、获取表字段名称
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
有获取表字段名的需求，该工具适用。

原理：

通过 desc 命令获取表字段信息

源码地址：

https://github.com/mike-zhang/pyExamples/blob/master/databaseRelate/mysqlOpt/MySQLdb_Opt/getTableFields.py

6、分页测试
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
数据过多，需要分页获取时，该代码适用。

原理：

通过limit实现

源码地址：

https://github.com/mike-zhang/pyExamples/blob/master/databaseRelate/mysqlOpt/MySQLdb_Opt/pagingTest1.py

7、批量清理表内容
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

需要批量清理表的内容时，该代码适用。

原理：

通过脚本执行多条删除语句。

源码地址：

https://github.com/mike-zhang/pyExamples/blob/master/databaseRelate/mysqlOpt/MySQLdb_Opt/clearTables.py

