InfluxDB meta文件解析
=====================================================

influxdb默认配置：
::
    
    /etc/influxdb/influxdb.conf
    
meta默认配置：

::

    [meta]
      dir = "/var/lib/influxdb/meta"
      retention-autocreate = true
      logging-enabled = true

* dir
 
meta数据存放目录，默认值：/var/lib/influxdb/meta

meta数据文件默认路径：/var/lib/influxdb/meta/meta.db

* retention-autocreate

用于控制默认存储策略，数据库创建时，会自动生成autogen的存储策略，默认值：true

* logging-enabled

是否开启meta日志，默认值：true      
    

meta文件的dump和load
----------------------------------------------    

源码路径： github.com/influxdata/influxdb/services/meta/client.go 

meta文件dump
::

    // snapshot will save the current meta data to disk
    func snapshot(path string, data *Data) error {
        file := filepath.Join(path, metaFile)
        tmpFile := file + "tmp"

        f, err := os.Create(tmpFile)
        if err != nil {
            return err
        }
        defer f.Close()

        var d []byte
        if b, err := data.MarshalBinary(); err != nil {
            return err
        } else {
            d = b
        }

        if _, err := f.Write(d); err != nil {
            return err
        }

        if err = f.Sync(); err != nil {
            return err
        }

        //close file handle before renaming to support Windows
        if err = f.Close(); err != nil {
            return err
        }

        return renameFile(tmpFile, file)
    }

snapshot可以通过以下两种方式触发：

1、当执行 Client.Open 函数时会进行snapshot操作；

2、执行meta文件更新时通过commit函数进行snapshot操作；
 
在InfluxDB中程序中，通过 NewServer 函数创建MetaClient变量（meta.NewClient），然后执行MetaClient.Open()进行初始化；

后续会通过Server.Open函数（run/server.go）启动各项服务，如果有meta文件的更新操作，通过commit函数进行snapshot操作； 
    
meta文件load    
::

    // Load will save the current meta data from disk
    func (c *Client) Load() error {
        file := filepath.Join(c.path, metaFile)

        f, err := os.Open(file)
        if err != nil {
            if os.IsNotExist(err) {
                return nil
            }
            return err
        }
        defer f.Close()

        data, err := ioutil.ReadAll(f)
        if err != nil {
            return err
        }

        if err := c.cacheData.UnmarshalBinary(data); err != nil {
            return err
        }
        return nil
    }

Client.Open()中会执行Load操作，NewServer时会自动加载。
    
meta文件内容编解码
---------------------------------------------------------------------   

源码路径： github.com/influxdata/influxdb/services/meta/data.go  

meta数据encode：
::

    // MarshalBinary encodes the metadata to a binary format.
    func (data *Data) MarshalBinary() ([]byte, error) {
        return proto.Marshal(data.marshal())
    }

meta数据decode：
::

    // UnmarshalBinary decodes the object from a binary format.
    func (data *Data) UnmarshalBinary(buf []byte) error {
        var pb internal.Data
        if err := proto.Unmarshal(buf, &pb); err != nil {
            return err
        }
        data.unmarshal(&pb)
        return nil
    }


proto路径 ：github.com/gogo/protobuf/proto    
    
meta文件结构定义
----------------------------------------------------------------------

源码路径： github.com/influxdata/influxdb/services/meta/data.go 

meta文件存储的就是 meta.Data 的数据，结构定义如下：

::

    // Data represents the top level collection of all metadata.
    type Data struct {
        Term      uint64 // associated raft term
        Index     uint64 // associated raft index
        ClusterID uint64
        Databases []DatabaseInfo
        Users     []UserInfo

        MaxShardGroupID uint64
        MaxShardID      uint64
    }
    
Term ：暂时不知道干什么用的。 
    
Index ：从源码看这个应该是类似版本号的东西，初始化为1，执行commit操作是会增加。如果为1，会立即执行持久化操作（在Open函数中操作）。    

ClusterID ： 是InfluxDB集群相关内容；

Databases ：用于存储数据库信息；

Users ：用于存储数据库用户信息；
  
    
DatabaseInfo 定义 ：
::

    // DatabaseInfo represents information about a database in the system.
    type DatabaseInfo struct {
        Name                   string
        DefaultRetentionPolicy string
        RetentionPolicies      []RetentionPolicyInfo
        ContinuousQueries      []ContinuousQueryInfo
    }
    
RetentionPolicyInfo 定义：
::

    // RetentionPolicyInfo represents metadata about a retention policy.
    type RetentionPolicyInfo struct {
        Name               string
        ReplicaN           int
        Duration           time.Duration
        ShardGroupDuration time.Duration
        ShardGroups        []ShardGroupInfo
        Subscriptions      []SubscriptionInfo
    }

ShardGroupInfo 定义：
::

    // ShardGroupInfo represents metadata about a shard group. The DeletedAt field is important
    // because it makes it clear that a ShardGroup has been marked as deleted, and allow the system
    // to be sure that a ShardGroup is not simply missing. If the DeletedAt is set, the system can
    // safely delete any associated shards.
    type ShardGroupInfo struct {
        ID          uint64
        StartTime   time.Time
        EndTime     time.Time
        DeletedAt   time.Time
        Shards      []ShardInfo
        TruncatedAt time.Time
    }

ShardInfo 定义：
::

    // ShardInfo represents metadata about a shard.
    type ShardInfo struct {
        ID     uint64
        Owners []ShardOwner
    }

ShardOwner 定义：
::

    // ShardOwner represents a node that owns a shard.
    type ShardOwner struct {
        NodeID uint64
    }
    
ShardOwner主要用于集群，其中NodeId用于标识集群的节点ID，在InfluxDB 1.1社区版本中集群已经不支持了，该字段无效。    

SubscriptionInfo 定义：
::

    // SubscriptionInfo hold the subscription information
    type SubscriptionInfo struct {
        Name         string
        Mode         string
        Destinations []string
    }

ContinuousQueryInfo 定义：
::

    // ContinuousQueryInfo represents metadata about a continuous query.
    type ContinuousQueryInfo struct {
        Name  string
        Query string
    }
    

UserInfo 定义：
::

    // UserInfo represents metadata about a user in the system.
    type UserInfo struct {
        Name       string
        Hash       string
        Admin      bool
        Privileges map[string]influxql.Privilege
    }

    
其它
--------------------------------------------

meta文件解析示例代码：

::

    package main

    import (   
        "os"
        "fmt"
        "io/ioutil"
        "github.com/influxdata/influxdb/services/meta"
    )

    func Load(metaFile string) error {
        cacheData:= &meta.Data{
                Index: 1,
            }
        //file := filepath.Join(c.path, metaFile)

        f, err := os.Open(metaFile)
        if err != nil {
            if os.IsNotExist(err) {
                return nil
            }
            return err
        }
        defer f.Close()

        data, err := ioutil.ReadAll(f)
        if err != nil {
            return err
        }

        if err := cacheData.UnmarshalBinary(data); err != nil {
            return err
        }
        //fmt.Println(data)
        //fmt.Println("=======================")
        
        fmt.Println("Term       :",cacheData.Term)
        fmt.Println("Index      :",cacheData.Index)
        fmt.Println("Databases :")
        //fmt.Println(cacheData.Databases)

        for k,dbInfo := range cacheData.Databases {
            //fmt.Println(k,dbInfo)
            fmt.Println("k =",k)
            fmt.Println(dbInfo.Name,dbInfo.DefaultRetentionPolicy)
            for _,rPolicy := range dbInfo.RetentionPolicies {
                //fmt.Println(rPolicy)            
                fmt.Println(rPolicy.Name,rPolicy.ReplicaN,rPolicy.Duration,rPolicy.ShardGroupDuration)
                fmt.Println("-------------ShardGroups---------------")
                //fmt.Println(rPolicy.ShardGroups)
                for shardIdx,shardGroup := range rPolicy.ShardGroups {
                    //fmt.Println(shardGroup)
                    fmt.Println("shardIdx =",shardIdx)
                    fmt.Println("ID          :",shardGroup.ID)
                    fmt.Println("StartTime   :",shardGroup.StartTime)
                    fmt.Println("EndTime     :",shardGroup.EndTime)
                    fmt.Println("DeletedAt   :",shardGroup.DeletedAt)
                    //fmt.Println("Shards      :",shardGroup.Shards)
                    fmt.Printf("Shards      :")
                    for _,shard := range shardGroup.Shards {
                        fmt.Println(shard.ID,shard.Owners)
                    }
                    
                    fmt.Println("TruncatedAt :",shardGroup.TruncatedAt)
                    //fmt.Println(shardGroup.ID,shardGroup.StartTime,shardGroup.EndTime)
                    // DeletedAt,Shards  ,	TruncatedAt 
                }
                //fmt.Println(rPolicy.Subscriptions)
                fmt.Println("--------------Subscriptions----------------")
                for subsIdx,subInfo := range rPolicy.Subscriptions {
                    //fmt.Println(subInfo)
                    fmt.Println("subsIdx =",subsIdx)
                    fmt.Println("Name :",subInfo.Name)
                    fmt.Println("Mode :",subInfo.Mode)
                    fmt.Println("Destinations :",subInfo.Destinations)
                }
                            
            }
            fmt.Println("=======================")
        }
        
        fmt.Println("Users :")
        fmt.Println(cacheData.Users)
        fmt.Println(cacheData.MaxShardGroupID)
        fmt.Println(cacheData.MaxShardID)
        return nil
    }

    func main() {
        argsWithProg := os.Args
        if(len(argsWithProg) < 2) {
            fmt.Println("usage : ",argsWithProg[0]," configFile")
            return 
        }
        metaFile := os.Args[1]

        fmt.Println(argsWithProg)
        fmt.Println(metaFile)

        Load(metaFile)
    }

    


    
    
    
    
    