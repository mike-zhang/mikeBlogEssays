InfluxDB源码阅读之snapshotter服务
==================================================
操作系统 ： CentOS7.3.1611_x64

go语言版本：1.8.3 linux/amd64

InfluxDB版本：1.1.0


服务模块介绍
---------------------------------------------------

源码路径： github.com/influxdata/influxdb/services/snapshotter

service.go  ： snapshotter服务的实现

service_test.go  :  snapshotter服务的测试代码

client.go  ： 提供snapshotter服务的客户端访问API
   
快照服务主要提供如下功能：

* TSM碎片文件备份

* Meta文件备份

拥有独特的标记（ BackupMagicHeader ，针对meta文件）： 0x59590101

* 数据库信息备份

* 数据库存储策略信息备份

Service结构
`````````````````````````````````````````````````

该结构所在文件 ：service.go

snapshotter主服务结构如下：
::

    type Service struct {
        wg  sync.WaitGroup
        err chan error

        Node *influxdb.Node

        MetaClient interface {
            encoding.BinaryMarshaler
            Database(name string) *meta.DatabaseInfo
        }

        TSDBStore *tsdb.Store

        Listener net.Listener
        Logger   *log.Logger
    }


解释如下：
    
* wg 

使用锁机制进行数据同步

服务收到连接请求后，首先计数器加1，然后在独立的goroutine中处理该连接，处理完成时计数器减1；

调用Close接口时，wg进行阻塞操作，保证服务关闭时所有任务都完成。

* err

error通道，暂时不知道怎么用。

* Node

InfluxDB节点信息，集群相关功能。

* MetaClient 

Meta服务客户端接口，获取Meta的信息，用于备份Meta文件、数据库信息、数据库存储策略。

* TSDBStore 

InfluxDB存储引擎指针，用于备份数据库的TSM碎片文件。
    
* Listener

socket对象，用于监听服务端口、接收客户端放来的请求。   
   
* Logger 

日志指针，用于记录快照服务在运行过程中产生的日志。

Request结构
``````````````````````````````````````````````````

该结构所在文件 ：service.go

snapshotter客户端请求的数据结构如下：
::

    type Request struct {
        Type            RequestType
        Database        string
        RetentionPolicy string
        ShardID         uint64
        Since           time.Time
    }

解释如下：

* Type 

用于区别数据备份的类型。

* Database

Meta文件备份、数据库信息备份、存储策略备份时使用，用于指定需要备份的数据库名称。

* RetentionPolicy

存储策略备份时使用，用于指定需要备份的数据库存储策略的名称。

* ShardID

TSM碎片文件备份时使用，用于指定碎片ID。

* Since

TSM碎片文件备份时使用，用于指定起始时间。
    
Response结构
``````````````````````````````````````````````````
结构如下：
::

    type Response struct {
        Paths []string
    }



该服务在InfluxDB中的应用
--------------------------------------------------------------

该服务在InfluxDB主服务器程序（influxd）中使用，具体如下：
::

    [root@localhost influxdb]# grep "github.com/influxdata/influxdb/services/snapshotter" * -rn 
    cmd/influxd/backup/backup.go:18:        "github.com/influxdata/influxdb/services/snapshotter"
    cmd/influxd/restore/restore.go:20:      "github.com/influxdata/influxdb/services/snapshotter"
    cmd/influxd/run/server.go:28:   "github.com/influxdata/influxdb/services/snapshotter"
    services/snapshotter/service.go:1:package snapshotter // import "github.com/influxdata/influxdb/services/snapshotter"
    [root@localhost influxdb]# 

1、服务流程
  
在 Server->Open 中通过 Server->appendSnapshotterService 加载SnapshotterService。

通过 Server->SnapshotterService 对外提供服务。

2、备份流程

备份流程如下：

通过控制台获取用户指令；

连接SnapshotterService，并发送请求；

执行备份过程；

snapshotter在该流程中充当SnapshotterService的客户端，负责转发请求及获取响应。


3、恢复流程

snapshotter在恢复流程中主要验证下 BackupMagicHeader 是否正确。




   
