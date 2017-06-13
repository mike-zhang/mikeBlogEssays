golang之log rotate
====================

操作系统： CentOS 6.9_x64 
   
go语言版本： 1.8.3

问题描述
----------------

golang的log模块提供的有写日志功能，示例代码如下：

::

    /*
    golang log example
    E-Mail : Mike_Zhang@live.com
    */
    package main

    import (
        "log"
        "os"
    )

    func main() {
        logFile,err := os.Create("test1.log")
        defer logFile.Close()
        if err != nil {
            log.Fatalln("open file error!")
        }
        logger := log.New(logFile,"[Debug]",log.Ldate | log.Ltime | log.Lshortfile)
        logger.Println("test debug message")
        logger.SetPrefix("[Info]")
        logger.Println("test info message")

    }

运行效果：
::

    [root@local t2]# go build logTest1.go
    [root@local t2]# ./logTest1
    [root@local t2]# cat test1.log
    [Debug]2017/06/13 23:18:36 logTest1.go:19: test debug message
    [Info]2017/06/13 23:18:36 logTest1.go:21: test info message
    [root@local t2]#

go语言的log模块没有提供log rotate接口，但实际开发中我们需要该功能：
我们不希望单个日志过大，否则文本编辑器无法打开，查看比较困难；
更不希望占用太大的存储空间，可以指定最多存多少个日志文件。

解决方案
-----------
借助带缓冲的channel来实现。

示例代码如下：
::

    /*
        golang log rotate example
        E-Mail : Mike_Zhang@live.com
    */

    package main

    import (
        "fmt"
        "log"
        "os"
        "time"
    )

    const (
        BACKUP_COUNT = 5
        MAX_FILE_BYTES = 2 * 1024 
    )

    func doRotate(fPrefix string) {
        for j := BACKUP_COUNT; j >= 1; j-- {
            curFileName := fmt.Sprintf("%s_%d.log",fPrefix,j)
            k := j-1
            preFileName := fmt.Sprintf("%s_%d.log",fPrefix,k)

            if k == 0 {
                preFileName = fmt.Sprintf("%s.log", fPrefix)
            }
            _,err := os.Stat(curFileName)
            if err == nil {
                os.Remove(curFileName)
                fmt.Println("remove : ", curFileName)
            }
            _,err = os.Stat(preFileName)
            if err  == nil {
                fmt.Println("rename : ", preFileName, " => ", curFileName)
                err = os.Rename(preFileName, curFileName)
                if err != nil {
                    fmt.Println(err)
                }
            }
        }
    }

    func NewLogger(fPrefix string) (*log.Logger, *os.File) {
        var logger *log.Logger
        fileName := fmt.Sprintf("%s.log", fPrefix)
        fmt.Println("fileName :", fileName)
        logFile, err := os.OpenFile(fileName, os.O_RDWR|os.O_CREATE|os.O_APPEND, 0666)

        if err != nil {
            fmt.Println("open file error!")
        } else {
            logger = log.New(logFile, "[Debug]", log.Ldate|log.Ltime|log.Lshortfile)
        }
        return logger, logFile
    }

    func logWorker(msgQueue <-chan string) {
        fPrefix := "msg"
        logger, logFile := NewLogger(fPrefix)
        for msg := range msgQueue {
            logger.Println(msg)
            fi, err2 := logFile.Stat()
            if err2 == nil {
                if fi.Size() > MAX_FILE_BYTES {
                    logFile.Close()
                    doRotate(fPrefix)
                    logger,logFile = NewLogger(fPrefix)
                }
            }
        }
        logFile.Close()
    }

    func main() {
        msgQueue := make(chan string, 1000)
        go logWorker(msgQueue)

        for j := 1; j <= 1000; j++ {
            msgQueue <- fmt.Sprintf("msg_%d", j)
            time.Sleep(1 * time.Second)
        }
        close(msgQueue)
        return
    }
        

运行效果如下：
::

    [root@local t2]# ./logRotateTest1
    fileName : msg.log
    rename :  msg.log  =>  msg_1.log
    fileName : msg.log
    rename :  msg_1.log  =>  msg_2.log
    rename :  msg.log  =>  msg_1.log
    fileName : msg.log
    rename :  msg_2.log  =>  msg_3.log
    rename :  msg_1.log  =>  msg_2.log
    rename :  msg.log  =>  msg_1.log
    fileName : msg.log
    ^C
  

    
讨论
------------
这里只是个简单的示例代码，实现了log rotate，更多功能需自行开发。



