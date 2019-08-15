windows7使用vhd虚拟磁盘
===================================================

操作系统 ： windows7_x64


创建vhd
`````````````````````````````````````````````````
磁盘管理 -->  操作 --> 创建vhd


挂载vhd
`````````````````````````````````````````````````

脚本：
::

    rem 挂载VHD
    @echo off
    (echo select vdisk file="D:\workspace\srcRead.vhd"
     echo attach vdisk)>"%tmp%\vhd.sh"
    diskpart /s "%tmp%\vhd.sh"
    pause

Python版本：

https://github.com/mike-zhang/pyExamples/blob/master/tools/vhdFileOpt/load_vhd.py
    

卸载vhd
`````````````````````````````````````````````````

脚本：
::

    rem 卸载VHD
    (echo select vdisk file="D:\workspace\srcRead.vhd"
     echo detach vdisk)>"%tmp%\vhd.sh"
    diskpart /s "%tmp%\vhd.sh"
    pause

Python版本：

https://github.com/mike-zhang/pyExamples/blob/master/tools/vhdFileOpt/unload_vhd.py
