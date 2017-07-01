python之tcp自动重连
====================

操作系统： CentOS 6.9_x64 
   
python语言版本： 2.7.13

问题描述
----------------

现有一个tcp客户端程序，需定期从服务器取数据，但由于种种原因（网络不稳定等）需要自动重连。

测试服务器示例代码：

::

    #! /usr/bin/env python
    #-*- coding:utf-8 -*-

    import socket
    import threading

    class ThreadedServer(object):
        def __init__(self, host, port):
            self.host = host
            self.port = port
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind((self.host, self.port))

        def listen(self):
            self.sock.listen(5)
            while True:
                client, address = self.sock.accept()
                client.settimeout(60)
                threading.Thread(target = self.listenToClient,args = (client,address)).start()

        def listenToClient(self, client, address):
            size = 1024
            while True:
                try:
                    data = client.recv(size)
                    if data:                    
                        response = data
                        client.send(response)
                        print "secndLen: ",len(data)                    
                    else:
                        raise error('Client disconnected')
                except:
                    client.close()
                    return False

    if __name__ == "__main__":
        while True:
            port_num = 12345
            try:
                port_num = int(port_num)
                break
            except ValueError:
                pass

        ThreadedServer('',port_num).listen()

解决方案
-----------

::

    '''
    tcp client with reconnect
    E-Mail : Mike_Zhang@live.com
    '''

    #! /usr/bin/env python
    #-*- coding:utf-8 -*-

    import os,sys,time
    import socket

    def doConnect(host,port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try :         
            sock.connect((host,port))
        except :
            pass 
        return sock
            
    def main():   
        host,port = "127.0.0.1",12345
        print host,port    
        sockLocal = doConnect(host,port)   
        
        while True :
            try :
                msg = str(time.time()) 
                sockLocal.send(msg) 
                print "send msg ok : ",msg                
                print "recv data :",sockLocal.recv(1024)
            except socket.error :
                print "\r\nsocket error,do reconnect "
                time.sleep(3)
                sockLocal = doConnect(host,port)   
            except :
                print '\r\nother error occur '            
                time.sleep(3) 
            time.sleep(1)
        
    if __name__ == "__main__" :
        main()
        

运行效果：
::
    
    (py27env) [root@local t1]# python tcpClient1_reconnect.py
    127.0.0.1 12345    
    send msg ok :  1498891374.98
    recv data : 1498891374.98
    send msg ok :  1498891375.98
    recv data : 1498891375.98
    send msg ok :  1498891376.98
    recv data :

    socket error,do reconnect
    send msg ok :  1498891381.99
    recv data : 1498891381.99
    send msg ok :  1498891382.99
    recv data : 1498891382.99   

    
讨论
------------
这里只是个简单的示例代码，实现了python的tcp自动重连。

