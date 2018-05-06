VirtualBox虚拟机磁盘瘦身
===================================================

操作系统 ： windows7_x64

VirtualBox 版本 : 4.3.28

原理：

使用0填充虚拟系统磁盘，然后删除填充文件，再使用VBoxManage进行压缩。


Linux系统磁盘瘦身
--------------------------------------

一、清理虚拟机操作系统磁盘
`````````````````````````````````````````````````

方法一：借助dd命令

::

    dd if=/dev/zero of=1.zero bs=1M
    
方法二：自己写程序实现（这里以Python为例）：

https://github.com/mike-zhang/pyExamples/blob/master/tools/diskFillzero.py

    
然后删除用0填充的磁盘文件（这里是 1.zero ）。

二、压缩vdi文件
`````````````````````````````````````````````````

将VirtualBox安装目录加入环境变量:
::

    C:\Program Files\Oracle\VirtualBox

    
关闭虚拟机，针对虚拟机磁盘文件执行如下命令：
::

    VBoxManage.exe modifyhd centos_7.3.vdi --compact  

如果要针对快照进行压缩，则需要针对特定的快照文件执行如下命令：
::

    VBoxManage.exe modifyhd Snapshots/{b28cd85a-2532-4e2c-90b3-e9b4fbaa062e}.vdi --compact 
        
    
windows系统磁盘瘦身
--------------------------------------


windows没有 dd 命令，可以使用上文提到的方法二，如果没有Python环境可以通过pyinstaller转换为exe文件（或者使用其它语言实现同样的功能），其它操作与上面提到的相同。



    
    