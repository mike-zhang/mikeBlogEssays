# freeswitch嵌入python脚本

- 操作系统：debian8.5_x64
- freeswitch 版本 ： 1.6.8
- python版本：2.7.9

## 开启python模块

安装python lib库

    apt-get install python-dev

编辑modules.conf，开启python模块：

    languages/mod_python

编译安装：

    ./configure && make && make install

modules.conf.xml中开启python支持；

启动freeswitch；

## 测试脚本

### API测试

添加测试脚本：

文件路径：/usr/local/freeswitch/scripts/test1.py

文件内容：

    import freeswitch

    def fsapi(session,stream,env,args):
        stream.write("hello")
        #stream.write(str(dir(freeswitch)))
        freeswitch.consoleLog("info","test")


控制台测试

    freeswitch@debian8> python test1
    hello
    2016-09-06 23:06:09.069753 [NOTICE] mod_python.c:212 Invoking py module: test1
    2016-09-06 23:06:09.069753 [DEBUG] mod_python.c:283 Call python script
    2016-09-06 23:06:09.069753 [INFO] switch_cpp.cpp:1360 test
    2016-09-06 23:06:09.069753 [DEBUG] mod_python.c:286 Finished calling python script
    freeswitch@debian8>


### APP测试

文件路径：
/usr/local/freeswitch/scripts/testCall.py

文件内容：

    import freeswitch
    def handler(session, args):
        session.answer()
        freeswitch.console_log("info","testCall")
        session.streamFile("local_stream://moh")
        freeswitch.msleep(3000)
        session.hangup()


在dialplan中加入如下配置：

    <extension name="python test script">
            <condition field="destination_number" expression="^400123456$">
                <action application="python" data="testCall"/>
            </condition>
    </extension>


注册话机，拨打400123456号码即可听到moh声音，同时看到freeswitch控制台日志。
