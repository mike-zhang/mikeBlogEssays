InfluxDB源码阅读之httpd服务
======================================================

操作系统 ： CentOS7.3.1611_x64

go语言版本：1.8.3 linux/amd64

InfluxDB版本：1.1.0

服务模块介绍
---------------------------------------------------

源码路径： github.com/influxdata/influxdb/services/httpd

config.go  ： httpd服务配置相关内容

config_test.go  ： 配置测试

service.go  ：httpd服务主程序

listen.go ：对监听器进行包装，限制活动连接的数量 

listen_test.go ：对监听器包装的测试

handler.go ： 客户端请求转发及具体的处理逻辑相关代码

handler_test.go ： 处理逻辑测试代码

response_writer.go ： http响应内容（支持csv、json格式）

response_logger.go ：日志相关内容
   
   
该模块提供https服务、http服务、unixSocket服务   
   
服务主要提供如下功能：

* 查询服务器的状态

* 统计服务器监控信息

* 提供数据查询功能

* 提供数据写入功能

* 用户认证
 

Service结构
`````````````````````````````````````````````````

该结构所在文件 ： service.go 

主服务结构如下：
::

    type Service struct {
        ln    net.Listener
        addr  string
        https bool
        cert  string
        key   string
        limit int
        err   chan error

        unixSocket         bool
        bindSocket         string
        unixSocketListener net.Listener

        Handler *Handler

        Logger *log.Logger
    }




解释如下：
    
* ln

tcp连接，用于提供http服务或https服务。

* addr 

tcp服务器绑定的服务地址及端口信息。
对应配置文件中的 bind-address 选项。

* https 

是否提供https服务，如果该标识为false，则提供http服务。
对应配置文件中的 https-enabled 选项。

* cert

https证书路径，使用https时有效。
对应配置文件中的 https-certificate 选项。

* key 

https私钥，使用https时有效。
对应配置文件中的 https-private-key 选项。

* limit 

用于限制服务器最大连接数，该值为0时不限制。
对应配置文件中的 max-connection-limit 选项。

* err 

error通道，暂时不知道怎么用。

* unixSocket

是否使用unix-socket，如果该标识为false，则不提供unix-socket服务（windows环境不适用）。
对应配置文件中的 unix-socket-enabled 选项。

* bindSocket

unix-socket文件路径，unix-socket开启时适用。
对应配置文件中的 bind-socket 选项。

* unixSocketListener 

unix_socket连接，用于提供unix_socket服务。

* Handler 

httpd->Handler 对象


Handler结构
``````````````````````````````````````````````````
该结构所在文件 ： handler.go  

snapshotter客户端请求的数据结构如下：
::

    // Handler represents an HTTP handler for the InfluxDB server.
    type Handler struct {
        mux     *pat.PatternServeMux
        Version string

        MetaClient interface {
            Database(name string) *meta.DatabaseInfo
            Authenticate(username, password string) (ui *meta.UserInfo, err error)
            Users() []meta.UserInfo
            User(username string) (*meta.UserInfo, error)
        }

        QueryAuthorizer interface {
            AuthorizeQuery(u *meta.UserInfo, query *influxql.Query, database string) error
        }

        WriteAuthorizer interface {
            AuthorizeWrite(username, database string) error
        }

        QueryExecutor *influxql.QueryExecutor

        Monitor interface {
            Statistics(tags map[string]string) ([]*monitor.Statistic, error)
        }
        PointsWriter interface {
            WritePoints(database, retentionPolicy string, consistencyLevel models.ConsistencyLevel, points []models.Point) error
        }

        Config    *Config
        Logger    *log.Logger
        CLFLogger *log.Logger
        stats     *Statistics
    }

解释如下：
    
* mux

go语言的 net/http 库的模式复用器。

* Version

InfluxDB版本信息。

* MetaClient

meta服务客户端接口，指向 meta.Client 结构（源码路径： influxdb/services/meta/client.go），
用于操作meta数据。

Database 函数 ： 通过名字查找数据库，可用于判断数据库是否存在。            

Authenticate 函数 ： 认证用户信息。

Users 函数 ：获取系统中所有用户的信息。

User 函数 ： 获取系统中单个用户的信息。

* QueryAuthorizer 

数据查询认证接口，指向 meta.QueryAuthorizer 结构（源码路径： influxdb/services/meta/query_authorizer.go）。

AuthorizeQuery 函数 ： 认证用户信息并执行数据查询操作。 

* WriteAuthorizer

数据写入认证接口，指向 meta.WriteAuthorizer 结构（源码路径： influxdb/services/meta/write_authorizer.go）。

AuthorizeWrite 函数 ： 认证用户信息并执行数据写入操作。

* QueryExecutor

查询执行器。

* Monitor 

httpd服务状态监控接口，指向 monitor.Monitor 结构（源码路径： influxdb/monitor/service.go）。

Statistics 函数 ： 统计服务器监控信息。

* PointsWriter

数据写入接口，执向 coordinator.PointsWriter 结构（源码路径： influxdb/coordinator/points_writer.go）。

WritePoints 函数 ： 数据写入功能。

* Config

httpd服务配置。

* Logger

日志相关。

* CLFLogger

日志相关。

* stats

用于存储httpd服务统计信息。


limitListener结构
``````````````````````````````````````````````````
该结构所在文件 ： listen.go 

limitListener是一个监听器，它在任何给定时间都会限制活动连接的数量，当配置文件中的max-connection-limit大于0的时有效。
   
数据结构如下：
::

    type limitListener struct {
        net.Listener
        sem chan struct{}
    }
  

该服务在InfluxDB中的应用
--------------------------------------------------------------

该服务在InfluxDB主服务器程序（influxd）中使用，具体如下：
::

    [root@localhost influxdb]# grep "github.com/influxdata/influxdb/services/httpd" * -rn
    cmd/influxd/run/config.go:24:   "github.com/influxdata/influxdb/services/httpd"
    cmd/influxd/run/server.go:23:   "github.com/influxdata/influxdb/services/httpd"
    cmd/influxd/run/server_helpers_test.go:20:      "github.com/influxdata/influxdb/services/httpd"
    services/httpd/config_test.go:7:        "github.com/influxdata/influxdb/services/httpd"
    services/httpd/handler_test.go:20:      "github.com/influxdata/influxdb/services/httpd"
    services/httpd/listen_test.go:10:       "github.com/influxdata/influxdb/services/httpd"
    services/httpd/service.go:1:package httpd // import "github.com/influxdata/influxdb/services/httpd"
    [root@localhost influxdb]#

在config中加载配置，在server中启动httpd服务。

