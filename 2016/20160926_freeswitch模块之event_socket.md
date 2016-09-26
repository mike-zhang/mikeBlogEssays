# freeswitch模块之event_socket

这是我之前整理的关于freeswitch mod_event_socket的相关内容，这里记录下，也方便我以后查阅。

mod_event_socket以socket的形式，对外提供控制FS一种途径，
缺省的IP是127.0.0.1，TCP端口是8021，可以在外部通过sokcet执行API/APP命令。

## 连接模式

连接分两种模式： inbound/outbound       
mod_event_socket 的默认加载模式是inbound,outbound模式需要在dialplan的配置文件中设置。

InBound模式由于是可以主动连接并可长期稳定保持，且此通道有且只有一个，心跳、外呼和注册等动作必须通过此种连接完成

OutBound模式由于是在外线呼入和内线呼出的时候才会触发socket连接事件，所以是不稳定的，且由于同一时间呼入数量不唯一，所以此连接的数目也是动态变化的，但是由于其每个来电建立一个socket连接，所以在大负荷情况下不会造成命令和事件的堵塞。

### 使用inbound模式
1、修改acl配置：

配置autoload_configs/acl.conf.xml文件：

    <list name="domains" default="deny">
      <!-- domain= is special it scans the domain from the directory to build the ACL -->
      <node type="allow" domain="$${domain}"/>
      <!-- use cidr= if you wish to allow ip ranges to this domains acl. -->
      <!-- <node type="allow" cidr="192.168.0.0/24"/> -->
      <node type="allow" cidr="192.168.168.0/24"/>
      <node type="allow" cidr="127.0.0.0/24"/>
    </list>

2、修改esl配置:
    
配置autoload_configs/event_socket.conf.xml文件：

    <configuration name="event_socket.conf" description="Socket Client">
      <settings>
        <param name="nat-map" value="false"/>
        <param name="listen-ip" value="0.0.0.0"/>
        <param name="listen-port" value="8021"/>
        <param name="password" value="ClueCon"/>
        <param name="apply-inbound-acl" value="domains"/>
        <!--<param name="apply-inbound-acl" value="loopback.auto"/>-->
        <!--<param name="stop-on-bind-error" value="true"/>-->
      </settings>
    </configuration>

3、重启freeswitch      

4、通过inbound方式使用freeswitch
python示例代码如下：

    import socket
    import json
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('127.0.0.1', 8021))
    # send auth
    sock.send('auth ClueCon\r\n\r\n')
    # send command
    sock.send('event json ALL\r\n\r\n')
    #sock.send('event plain ALL\r\n\r\n')
    while True:
        print sock.recv(10240)


### 使用outbound模式

1、编辑conf/dialplan/default.xml，增加如下内容：

    <extension name="123456789 Entrance">
        <condition field="destination_number" expression="^123456789$">           
          <action application="socket" data="127.0.0.1:9000 async full" />       
          <action application="playback" data="$${hold_music}"/>
          <action application="hangup" data="" /> 
        </condition>
    </extension>

2、启动监听服务器
监听listen-ip:listen-port（如在Linux下可以通过 nc -v -l 9000)，

然后拨打配置的电话号码（本例中为123456789）
即可收到Connection from 127.0.0.1 port 9000 [tcp/*] accepted 的消息，
键入connect\n\n即可进入OutBound模式


## 通过socket控制freeswitch

可以通过任何支持socket的语言控制freeswitch，这里以python为例子描述怎么通过socket控制freeswitch。

- auth <password>

当用户第一次通过mod_event_socket连接到freeswitch时，必须进行认证，认证示例：

sock.send(“auth ClueCon\r\n\r\n”)

- api       
执行freeswitch的API命令，阻塞执行。            
语法：api <command> <args>                 
示例：     

    sock.send('api originate user/1000 &echo\r\n\r\n')
    sock.send('api originate user/1001 &echo\r\n\r\n')

socket会将上述两条指令同时发送给freeswitch，但freeswitch按顺序阻塞执行。

- bgapi     
功能和api相同，非阻塞执行。             
语法：bgapi  <command>  <args>             
示例：     

    sock.send('bgapi originate user/1000 &echo\r\n\r\n')
    sock.send('bgapi originate user/1001 &echo\r\n\r\n')

socket会将上述两条指令同时发送给freeswitch，同时执行。

- event     
启动或停止事件流。       
语法：event  <format>  <event type list |all>          
<format> : 	plain、json、xml              
Event types ： 参考freeswitch事件类型              

示例:             

    sock.send('event json ALL\r\n\r\n')

接收freeswitch所有事件，并以json格式返回。

- noevents      
关闭上一个event开启的事件         
语法 ： noevents           
示例：             
    
    sock.send('noevents\r\n\r\n')

- divert_events     
脚本注册接收事件的函数分转到event  socket上。       
语法：divert_events  <on|off>          

- filter        
设置event socket接收事件的类型。      
语法：filter  <EventHeader>  <ValueToFilter>           
示例：     

只订阅CHANNEL_EXECUTE事件        

    sock.send('filter Event-Name CHANNEL_EXECUTE\r\n\r\n')
        
只订阅uuid为34602e08-557a-494a-af47-99e9d55e26ed的事件

    sock.send('filter Unique-ID 34602e08-557a-494a-af47-99e9d55e26ed\r\n\r\n')

- filter delete     
取消订阅的事件。    
语法：filter  delete  <EventHeader>  <ValueToFilter>       
示例：     

    sock.send('filter  delete  Event-Name CHANNEL_EXECUTE\r\n\r\n')    
    sock.send('filter  delete  Unique-ID 34602e08-557a-494a-af47-99e9d55e26ed\r\n\r\n')

- nixevents     
设置event socket禁止接收的事件类型。        
语法：nixevents <event types | ALL| CUSTOM custom event sub-class>         
示例：         

不订阅HEARTBEAT事件

    sock.send('nixevent HEARTBEAT\r\n\r\n')
   

- sendevent     
发送一个事件到系统队列中。       
语法：sendevent  <event-name>          
示例（消息内容）：       

    sendevent SOME_NAME
    Event-Name: CUSTOM
    Event-Subclass: albs::Section-Alarm
    Section: 33
    Alarm-Type: PIR
    State: ACTIVE

- sendmsg       

给一个uuid发送一个消息，可以执行其他模块的应用接口，也可以挂断电话等。       
语法：sendmsg <uuid>       
示例（消息内容）：   

    sendmsg <uuid>
    call-command: execute
    execute-app-name: playback
    execute-app-arg: /tmp/test.wav

- execute           
执行一个拨号规则的应用。        
语法：         

    sendmsg <uuid>      
    call-command: execute
    execute-app-name: <one of the applications>
    execute-app-arg: <application data>
    loops: <number of times to invoke the command, default: 1>

- hangup
对活动的呼叫挂机。           
语法： 

    sendmsg <uuid>
    call-command: hangup
    hangup-cause: <one of the causes listed below>

- nomedia       

控制freeswitch是否处于实时的媒体路径，这个命令支持用户对指定的通道启用或关闭媒体处理。            

语法：

    sendmsg <uuid>
    call-command: nomedia
    nomedia-uuid: <noinfo>

- log <level>       

设置日志级别。

- nolog     

禁止日志。

- linger    

告诉freeswitch当一个通道挂机时不要关闭socket连接，直到收取相关通道的最后一个事件。

- nolinger

关闭上次开启的linger命令。

## 通过freeswitch提供的ESL库进行控制

这里以python为例描述下ESL库的基本使用及api接口。

###　安装ESL
以python为例进行安装:

    cd libs/esl/
    make pymod
    make pymod-install
    
### ESL示例

- InBound模式

Python示例代码：

    import ESL
    import time

    hostIp,port,user = "127.0.0.1","8021","ClueCon"

    con = ESL.ESLconnection(hostIp,port,user)
    con.events("json","all")
    for i in range(100):
        eventData = con.recvEvent()
        print eventData.getHeader("Event-Name")
    con.disconnect()

- OutBound模式

配置dialplan：     

    <action application="socket" data="127.0.0.1:9000 async full"/>

Python示例代码：

    import SocketServer
    import ESL

    class ESLRequestHandler(SocketServer.BaseRequestHandler ):
        def setup(self):
            print self.client_address, 'connected!'
            fd = self.request.fileno()
            con = ESL.ESLconnection(fd)
            if con.connected():
                info = con.getInfo()
                uuid = info.getHeader("unique-id")
                print uuid
                con.execute("answer","", uuid)
                con.execute("playback","/tmp/sample.wav", uuid)

    server = SocketServer.ThreadingTCPServer(('', 9000), ESLRequestHandler)
    server.serve_forever()
    
    
### ESL接口介绍

#### eslSetLogLevel函数

该函数用于设置服务器的日志级别，使用方式如下：

    eslSetLogLevel(loglevel)

其中loglevel是一个整数变量，从0到7，含义如下:          

0 是 EMERG           
1 是 ALERT           
2 是 CRIT        
3 是 ERROR       
4 是 WARNING     
5 是 NOTICE      
6 是 INFO        
7 是 DEBUG       

### ESLconnection对象

ESLconnection对象维护与freeswitch之间的连接，以发送命令并进行事件处理。
成员函数列表如下：

- socketDescriptor()
该函数返回连接的UNIX文件句柄

- connected()
判断是否已连接，连接返回1，否则返回0

- getInfo()

当freeswitch使用outbound模式连接时，它将首先发一个CHANNEL_DATA事件，getInfo会返回该事件；         
在inbound模式中返回None

- send(command)
向freeswitch发送一个command，但不会等待返回结果，需要显式调用recvEvent或recvEventTimed以接收返回的事件。        

- sendRecv(command) 
向freeswitch发送一个command，并等待返回结果（一个ESLevent对象）。

- api(command[,arguments])
向freeswitch发送api命令，阻塞执行 

- bgapi(command[, arguments][,custom_job_uuid])
向freeswitch发送bgapi命令，后台执行，非阻塞执行     

- sendEvent(event)      
向freeswitch发送一个事件
- sendMSG(event,uuid)
参考sendmsg命令 

- recvEvent()
从freeswitch接收事件，阻塞模式

- recvEventTimed(milliseconds)  
与recvEvent类似，但不会无限等待，而是在参数指定的毫秒数会返回。            
recvEventTimed(0)会立即返回。 

- filter (header,value)     
事件过滤，类似filter命令。

- events (event_type,value)     
事件订阅，类似event命令。

- execute (app[,arg][,uuid])        
执行dialplan的app，并阻塞等待返回.
返回结果为一个ESLevent对象，通过getHeader(“Reply-Text”)可以获取返回值，”+OK”表示成功，”-ERR”表示失败。

- executeAsync (app[,arg][,uuid])       
与execute()相同，但非阻塞执行。        

- setAsyncExecute(value)        
强制将socket设置为异步模式，value为1是异步，0是同步。   

- setEventLock(value)       
使用该选项后，后续所有的execute()调用都将带有”event-lock:true”头域。 

- disconnect()  
主动中断与freeswitch的连接。 

#### ESLevent对象         

当接收一个事件时，用户将获得一个ESLevent对象，这个对象包含各种帮助函数变量
来帮助解析和处理收到的事件。
    
    con = ESL.ESLconnection("127.0.0.1", "8021", "ClueCon")
    con.events("json", "all");
    eventData = con.recvEvent()

eventData即为ESLevent对象 

ESLevent对象成员函数列表如下：

- serialize([format])

将event数据转换成”name:value”型数据，format参数可以为：     

"xml"           
"json"          
"plain" (default)           

示例如下：

    eventData.serialize('json') 获取json格式数据

- setPriority([number])     
设置事件的级别         

- getHeader(headerName)     
获取header对应的value，示例如下：      

    eventData .getHeader('Event-Name') #获取事件名称
    
- getBody()

获取事件的正文

- getType()     
获取event object的事件类型         

- addBody(value)    
向事件中加入正文，可以调用多次

- addHeader(key,value)  
向事件中加入一个头域(ESL_STACK_BOTTOM)

- pushHeader(key,value)
向事件中加入一个头域(ESL_STACK_PUSH)

- unshiftHeader(key,value)
向事件中加入一个头域(ESL_STACK_UNSHIFT)

- delHeader(key)
从Event中删除头域

- firstHeader()
将指针指向Event的第一个头域，并返回它的key值。它必须在nextHeader之前调用

- nextHeader()
移动指针指向下一个header，在函数调用前必须先调用firstHeader()

