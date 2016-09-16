# freeswitch对接其它SIP设备

这几天用到freeswitch对接其它设备方面的知识，这里整理下，也方便我以后查阅。

- 操作系统：debian8.5_x64
- freeswitch 版本 ： 1.6.8

## 一、freeswitch作为被叫设备
freeswitch作为被叫设备和其它设备对接的情况比较简单，可以直接通过5080端口呼入。    
freeswitch默认配置默认开启5080端口的对接（conf/dialplan/public.xml中关于public）:    

    <extension name="public_extensions">
        <condition field="destination_number" expression="^(10[01][0-9])$">
            <action application="transfer" data="$1 XML default"/>
        </condition>
    </extension>

## 二、freeswitch作为主叫设备    

这里主要描述下freeswitch作为主叫设备怎么对接其它sip设备（使用sipp模拟）。   

HostA ： 192.168.1.100     
HostB ： 192.168.1.101    

其中HostA上安装freeswitch，HostB使用sipp模拟其它设备。   

### 使用sip uri格式对接

- 1、编辑A机中 conf/dialplan/public.xml 文件 ，添加如下extension ：


    <extension name="hostB">
        <condition field="destination_number" expression="^0(.*)$">
                <action application="bridge" data="sofia/external/sip:$1@192.168.168.101:5080" />
        </condition>
    </extension>


- 2、B机上使用sipp模拟uas设备，命令如下：


    sipp -sn uas -p 5080

A机重新加载xml文件（ F6 或 reloadxml ），在A的1000话机上拨打号码 01234 即可看到对接效果。


### 使用网关对接

- 1、在A机上创建 conf/sip_profiles/external/gw_a.xml 文件，添加如下内容：


    <include>
      <gateway name="gw_A">
        <param name="username" value="anonymous"/>
        <param name="from-user" value=""/>
        <param name="password" value=""/>
        <param name="outbound-proxy" value="192.168.1.101:5080"/>
        <param name="register-proxy" value="192.168.1.101:5080"/>
        <param name="expire-seconds" value="120"/>
        <param name="register" value="false"/>
        <param name="register-transport" value="UDP"/>
        <param name="caller-id-in-from" value="true"/>
        <param name="extension-in-contact" value="true"/>
        <variables>
          <variable name="gateway_name" value="gw_A"/>          
        </variables>
      </gateway>
    </include>    

- 2、打开A机中 conf/dialplan/public.xml 文件 ，添加如下extension ：


    <extension name="gw_A">
            <condition field="destination_number" expression="^9(.*)$">
                <action application="bridge" data="sofia/gateway/gw_A/$1"/>
            </condition>
    </extension>

- 3、B机上使用sipp模拟uas设备，命令如下：

    sipp -sn uas -p 5080
    
- 4、加载网关配置，需在A机器执行如下命令：

    sofia profile external rescan


A机重新加载xml文件（ F6 或 reloadxml ），在A的1000话机上拨打号码 91234 即可看到对接效果。

