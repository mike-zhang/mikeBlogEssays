python访问Apollo获取配置
===================================================

操作系统 ： CentOS7.3.1611_x64
Python 版本 : 3.6.8


Apollo源码地址：
https://github.com/ctripcorp/apollo

访问Apollo使用这个库：

https://github.com/filamoon/pyapollo


不要使用pypi提供的apollo库（是一个编辑器的库）


其实真正需要的也就一个文件（pyapollo.py，我修改后的）：

https://github.com/mike-zhang/pyExamples/blob/master/pyapolloRelate/pyapollo.py


使用示例：
::
    
    import pyapollo

    a = pyapollo.ApolloClient("test1","default","http://192.168.1.100:8080")
    a.start()

    for key in ["ip","port"]:
        v = a.get_value(key)
        print("%s : " % key)
        print(v)
