golang之tcp自动重连
====================

操作系统： CentOS 6.9_x64 
   
go语言版本： 1.8.3

问题描述
----------------

现有一个tcp客户端程序，需定期从服务器取数据，但由于种种原因（网络不稳定等）需要自动重连。

测试服务器示例代码：
::

    /*
    tcp server for test
    E-Mail : Mike_Zhang@live.com
    */


    package main

    import (
        "fmt"
        "net"
        "os"
        "strings"
        "time"
    )

    func checkError(err error) {
        if err != nil {
            fmt.Println(err)
            os.Exit(1)
        }
    }

    func handleClient(conn net.Conn) {
        conn.SetReadDeadline(time.Now().Add(3 * time.Minute))
        request := make([]byte,1024)
        defer conn.Close()

        for {
            recv_len,err := conn.Read(request)
            if err != nil {
                fmt.Println(err)
                break
            }
            if recv_len == 0 {
                break
            }
            recvData := strings.TrimSpace(string(request[:recv_len]))
            fmt.Println("recv_len : ",recv_len)
            fmt.Println("recv_data : " + recvData)
            daytime := time.Now().String()
            conn.Write([]byte(daytime + "\n"))
            request = make([]byte,1024)
        }
    }

    func main() {
        bindInfo := ":12345"
        tcpAddr,err := net.ResolveTCPAddr("tcp4",bindInfo)
        checkError(err)
        listener,err := net.ListenTCP("tcp",tcpAddr)
        checkError(err)
        for {
            cc,err := listener.Accept()
            if err != nil {
                continue
            }
            go handleClient(cc)
        }
    }


解决方案
-----------

::

    /* 
    tcp client with reconnect
    E-Mail : Mike_Zhang@live.com
    */

    package main

    import (
        "net"
        "fmt"
        "bufio"
        "time"
    )

    func doTask(conn net.Conn) {
        for {
            fmt.Fprintf(conn,"test msg\n")
            msg,err := bufio.NewReader(conn).ReadString('\n')
            if err != nil {
                fmt.Println("recv data error")
                break
            }else{
                fmt.Println("recv msg : ",msg)
            }
            time.Sleep(1 * time.Second)
        }

    }

    func main() {
        hostInfo := "127.0.0.1:12345"

        for {
            conn,err := net.Dial("tcp",hostInfo)
            fmt.Print("connect (",hostInfo)
            if err != nil {
                fmt.Println(") fail")
            }else{
                fmt.Println(") ok")
                defer conn.Close()
                doTask(conn)
            }
            time.Sleep(3 * time.Second)
        }   
    }


运行效果：
::

    [root@local t1]# ./tcpClient1
    connect (127.0.0.1:12345) ok
    recv msg :  2017-06-12 21:10:32.110977137 +0800 CST

    recv msg :  2017-06-12 21:10:33.111868746 +0800 CST

    recv data error
    connect (127.0.0.1:12345) fail
    connect (127.0.0.1:12345) fail
    connect (127.0.0.1:12345) ok
    recv msg :  2017-06-12 21:10:43.117203432 +0800 CST

    recv msg :  2017-06-12 21:10:44.11853427 +0800 CST


    
讨论
------------
这里只是个简单的示例代码，实现了tcp自动重连。



