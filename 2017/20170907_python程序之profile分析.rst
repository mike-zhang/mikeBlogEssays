python程序之profile分析
==================================

操作系统 ： CentOS7.3.1611_x64     
  
python版本：2.7.5      

问题描述
------------------------------------

1、Python开发的程序在使用过程中很慢，想确定下是哪段代码比较慢；

2、Python开发的程序在使用过程中占用内存很大，想确定下是哪段代码引起的；

解决方案
-------------------------------------
使用profile分析分析cpu使用情况
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

profile介绍： https://docs.python.org/2/library/profile.html

可以使用profile和cProfile对python程序进行分析，这里主要记录下cProfile的使用，profile参考cProfile即可。

假设有如下代码需要进行分析（cProfileTest1.py）：
::

    #! /usr/bin/env python
    #-*- coding:utf-8 -*-

    def foo():
        sum = 0
        for i in range(100):
            sum += i
        return sum
        
    if __name__ == "__main__" :
        foo()
        

可以通过以下两种使用方式进行分析：

1、不修改程序

分析程序：
::

    python -m cProfile -o test1.out cProfileTest1.py

查看运行结果：
::
    
    python -c "import pstats; p=pstats.Stats('test1.out'); p.print_stats()"

查看排序后的运行结果：
::
    
    python -c "import pstats; p=pstats.Stats('test1.out'); p.sort_stats('time').print_stats()"
     
2、修改程序

加入如下代码：
::

    import cProfile 
    cProfile.run("foo()") 
    
完整代码如下： 
https://github.com/mike-zhang/pyExamples/blob/master/profileOpt/cpuProfile1/cProfileTest2.py

运行效果如下：
::

   Ordered by: standard name

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    0.000    0.000 <string>:1(<module>)
        1    0.000    0.000    0.000    0.000 cProfileTest2.py:4(foo)
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
        1    0.000    0.000    0.000    0.000 {range}

结果说明：
::

    ncalls ： 函数的被调用次数
    tottime ：函数总计运行时间，除去函数中调用的函数运行时间
    percall ：函数运行一次的平均时间，等于tottime/ncalls
    cumtime ：函数总计运行时间，含调用的函数运行时间
    percall ：函数运行一次的平均时间，等于cumtime/ncalls
    filename:lineno(function) 函数所在的文件名，函数的行号，函数名

使用memory_profiler分析内存使用情况
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

https://pypi.python.org/pypi/memory_profiler

需要安装memory_profiler ：
::

    pip install psutil
    pip install memory_profiler

假设有如下代码需要进行分析:
::

    def my_func():
        a = [1] * (10*6)
        b = [2] * (10*7)
        del b
        return a

使用memory_profiler是需要修改代码的，这里记录下以下两种使用方式：

1、不导入模块使用
::

    @profile
    def my_func():
        a = [1] * (10*6)
        b = [2] * (10*7)
        del b
        return a

完整代码如下： 
https://github.com/mike-zhang/pyExamples/blob/master/profileOpt/memoryProfile1/test1.py

profile分析：
::

    python -m memory_profiler test1.py
    
   
2、导入模块使用

::

    from memory_profiler import profile

    @profile
    def my_func():
        a = [1] * (10*6)
        b = [2] * (10*7)
        del b
        return a

完整代码如下：

直接运行程序即可进行分析。 

运行效果如下：
::

    (py27env) [mike@local test]$ python test1.py
    Filename: test1.py

    Line #    Mem usage    Increment   Line Contents
    ================================================
         6     29.5 MiB      0.0 MiB   @profile
         7                             def my_func():
         8     29.5 MiB      0.0 MiB       a = [1] * (10*6)
         9     29.5 MiB      0.0 MiB       b = [2] * (10*7)
        10     29.5 MiB      0.0 MiB       del b
        11     29.5 MiB      0.0 MiB       return a


profile分析完整代码地址：https://github.com/mike-zhang/pyExamples/tree/master/profileOpt

        
        