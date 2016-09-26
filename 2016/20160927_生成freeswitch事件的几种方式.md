# 生成freeswitch事件的几种方式

本文描述了生成freeswitch事件的几种方式，这里记录下，也方便我以后查阅。

- 操作系统：debian8.5_x64
- freeswitch 版本 ： 1.6.8

## 在freeswitch代码中加入事件

产生内置事件（以SWITCH_EVENT_MODULE_LOAD为例）：

	switch_event_t *event;
    if (switch_event_create(&event, SWITCH_EVENT_MODULE_LOAD) == SWITCH_STATUS_SUCCESS)
    {
        switch_event_add_header_string(event, SWITCH_STACK_BOTTOM, "type", "endpoint");
        switch_event_add_header_string(event, SWITCH_STACK_BOTTOM, "name", ptr->interface_name);
        switch_event_add_header_string(event, SWITCH_STACK_BOTTOM, "key", new_module->key);
        switch_event_add_header_string(event, SWITCH_STACK_BOTTOM, "filename", new_module->filename);
        switch_event_fire(&event);
    }

产生自定义事件：

    if (switch_event_create_subclass(&event,SWITCH_EVENT_CUSTOM,"calltest1::calltest1_sub") == SWITCH_STATUS_SUCCESS)
    {
        switch_event_add_header_string(event, SWITCH_STACK_BOTTOM, "callee_uuid", "86896a7a-3dc3-4175-aaa1-cdcbfd9bd566");
        switch_event_add_header_string(event, SWITCH_STACK_BOTTOM, "caller_num", "1000");
        switch_event_add_header_string(event, SWITCH_STACK_BOTTOM, "callee_num", "1001");
        switch_event_add_header_string(event, SWITCH_STACK_BOTTOM, "failed_reason", "exten not avaliable");
        switch_event_fire(&event);
    }

## 使用嵌入式脚本生成freeswitch事件

### 使用lua生成freeswitch事件

/tmp/1.lua内容如下：

    function fire_failed_event(callee_uuid,caller_num,callee_num,failed_reason)
        local event = freeswitch.Event("CUSTOM","calltest1::calltest1_sub")
        event:addHeader("callee_uuid",callee_uuid)
        event:addHeader("caller_num",caller_num)
        event:addHeader("callee_num",callee_num)
        event:addHeader("failed_reason",failed_reason)
        event:fire()
    end

    fire_failed_event("86896a7a-3dc3-4175-aaa1-cdcbfd9bd566","1000","1001","exten not avaliable")
    
fscli中运行：

    /event json  CUSTOM calltest1::calltest1_sub
    luarun /tmp/1.lua

事件内容如下：

    {
            "Event-Subclass":       "calltest1::calltest1_sub",
            "Event-Name":   "CUSTOM",
            "Core-UUID":    "ae0f2919-f45f-450c-8d8f-4c9c555032b6",
            "FreeSWITCH-Hostname":  "localhost",
            "FreeSWITCH-Switchname":        "localhost",
            "FreeSWITCH-IPv4":      "192.168.1.101",
            "FreeSWITCH-IPv6":      "::1",
            "Event-Date-Local":     "2016-09-23 16:54:41",
            "Event-Date-GMT":       "Fri, 23 Sep 2016 08:54:41 GMT",
            "Event-Date-Timestamp": "1474620881330278",
            "Event-Calling-File":   "switch_cpp.cpp",
            "Event-Calling-Function":       "Event",
            "Event-Calling-Line-Number":    "262",
            "Event-Sequence":       "347438",
            "callee_uuid":  "86896a7a-3dc3-4175-aaa1-cdcbfd9bd566",
            "caller_num":   "1000",
            "callee_num":   "1001",
            "failed_reason":        "exten not avaliable"
    }

### 使用python生成freeswitch事件

脚本/usr/local/freeswitch/scripts/test11.py 内容如下：

    import freeswitch
    import uuid

    def fsapi(session,stream,env,args):
        event = freeswitch.Event("CUSTOM","calltest1::calltest1_sub")
        event.addHeader("callee_uuid",str(uuid.uuid4()))
        event.addHeader("caller_num","1000")
        event.addHeader("callee_num","1001")
        event.addHeader("failed_reason","pytest reason")
        event.fire()
        freeswitch.consoleLog("info","fire ")

运行效果参考lua实现的demo

## 通过ESL发送事件

也可以通过freeswitch的ESL接口的sendEvent函数进行发送事件

### ESL库方式

freeswitch提供的有ESL开发库，这里以python为例展示下通过ESL实现事件的发送：

    import ESL

    pbxHost,pbxPort = '192.168.1.101','8021'
    pbxAuth = 'Cluecon'

    con = ESL.ESLconnection(pbxHost,pbxPort,pbxAuth)    
    e = ESL.ESLevent("CUSTOM","calltest1::calltest1_sub")
    e.addHeader("callee_uuid","42e36a32-d6c9-4fac-841d-95bbab9ce2f5")
    e.addHeader("caller_num","1000")
    e.addHeader("callee_num","1001")
    e.addHeader("failed_reason","pytest reason")

    con.sendEvent(e)

运行效果参考lua实现的demo

### 使用socket方式

如果在某些场合不适合使用ESL（比如windows下想使用ESL），
或者发现ESL有bug（之前发现python版的ESL有内存泄漏），
可以直接使用socket直接发送，示例如下：

    import socket  

    pbxHost,pbxPort = '192.168.1.101',8021
    pbxAuth = 'ClueCon'

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    sock.connect((pbxHost,pbxPort))
    sock.send('auth %s\r\n\r\n' % pbxAuth)

    tmsg = "sendevent CUSTOM\r\n"
    tmsg += "Event-Name: CUSTOM\r\n"
    tmsg += "Event-Subclass: calltest1::calltest1_sub\r\n"
    tmsg += "callee_uuid: 42e36a32-d6c9-4fac-841d-95bbab9ce2f5\r\n"
    tmsg += "caller_num: 1000\r\n"
    tmsg += "callee_num: 1001\r\n"
    tmsg += "failed_reason: pytest reason\r\n"

    sock.send('%s\r\n' % tmsg)

运行效果参考lua实现的demo


