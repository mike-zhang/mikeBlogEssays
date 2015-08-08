# curl操作couchDB

couchdb 服务器地址： 127.0.0.1 

端口：5984

## 添加数据库

- **连接到couchdb**

    curl -X GET http://127.0.0.1:5984   
    
    {"couchdb":"Welcome","uuid":"1c81fc63d761c82c4f48bac34afd5eb8","version":"1.6.0","vendor":{"name":"The Apache Software Foundation","version":"1.6.0"}}
    
- **创建一个数据库db1**
    
    curl -X PUT http://127.0.0.1:5984/db1
    
    {"ok":true}
    
- **创建数据库 db2**
    
    curl -X PUT http://127.0.0.1:5984/db2
    
    {"ok":true}
    
- **列出当前所有的数据库**

    curl -X GET http://127.0.0.1:5984/_all_dbs      
    
    ["_replicator","_users","db1","db2"]
    

- **删除db2数据库**
    
    curl -X DELETE http://127.0.0.1:5984/db2        
    
    {"ok":true}     
    
    删除成功        
    
## 数据库操作


- **向数据库添加数据**
> 
 **首先，获取一个uuid**       
    curl -X GET http://127.0.0.1:5984/_uuids        
    {"uuids":["1925a2a284289df9b55b390525001ca1"]}      
    注意：每次得到的uuid不一样。    
    获取10个uuid： curl -X GET http://127.0.0.1:5984/_uuids?count=10        
> 
 **使用uuid作为键插入一条数据**             
    curl -X PUT http://127.0.0.1:5984/db1/1925a2a284289df9b55b390525001ca1 -d '{"title":"test","content":"this is test!"}'         
    {"ok":true,"id":"1925a2a284289df9b55b390525001ca1","rev":"1-4d3e6350fdcc39f7b482c4cab8ff5d9a"}
    
- **更新记录**

    curl -X PUT http://127.0.0.1:5984/db1/1925a2a284289df9b55b390525001ca1 -d '{"title":"test","content":"this is test!modifyied!"}'        
    
    {"error":"conflict","reason":"Document update conflict."}           
    失败了。因为，couchdb是按版本提交的，同一个源提交多次会造成一定的混乱。所以，其采用了版本进行控制。           
    
    curl -X PUT http://127.0.0.1:5984/db1/1925a2a284289df9b55b390525001ca1 -d '{"_rev":"1-4d3e6350fdcc39f7b482c4cab8ff5d9a","title":"test","content":"this is test!"}'          
    
    {"ok":true,"id":"1925a2a284289df9b55b390525001ca1","rev":"2-f6f24194b29981316f2412e288cda320"}      
    这样就没有问题了。           
    
- **获取记录**
    
    curl -X GET http://127.0.0.1:5984/db1/1925a2a284289df9b55b390525001ca1          
    
    {"_id":"1925a2a284289df9b55b390525001ca1","_rev":"2-f6f24194b29981316f2412e288cda320","title":"test","content":"this is test!"}
    

- **列出db1库下的所有文档**

    curl -X GET http://127.0.0.1:5984/db1/_all_docs
    
    {"total_rows":2,"offset":0,"rows":[             
    {"id":"1925a2a284289df9b55b390525001ca1","key":"1925a2a284289df9b55b390525001ca1","value":{"rev":"2-f6f24194b29981316f2412e288cda320"}},        
    {"id":"1925a2a284289df9b55b390525002c29","key":"1925a2a284289df9b55b390525002c29","value":{"rev":"1-4a1158c264f8cc636e1fc54a7a696de6"}}         
    ]}          
   
- **删除记录**

    curl -X DELETE http://127.0.0.1:5984/db1/1925a2a284289df9b55b390525001ca1?rev=2-f6f24194b29981316f2412e288cda320        
  
### 上传附件

  curl -X PUT http://127.0.0.1:5984/db1/40dab8a067c56aef572307dd1f0119c8 -d '{"title":"test","content":"this is test!"}'            
  curl -X PUT http://127.0.0.1:5984/db1/40dab8a067c56aef572307dd1f0119c8/atwork.jpg?rev=2-2739352689 --data-binary @atwork.jpg -H "Content-Type:image/jpg"          
  atwork.jpg是当前目录下的图片文件。            
  
## 数据库复制
        
-  **本地复制**
  
    curl -X PUT http://127.0.0.1:5984/albums-replica            
    curl -X POST http://127.0.0.1:5984/_replicate -d '{"source":"albums","target":"albums-replica"}' -H "Content-Type: application/json"        

- **本地到远端复制**
    
    curl -X POST http://127.0.0.1:5984/_replicate -d '{"source":"albums","target":"http://example.org:5984/albums-replica"}' -H "Content-Type:application/json"     
    
    如果远端服务器有密码，可以采用这种格式：http://username:pass@remotehost:5984/demo           

- **远端到本地**

    curl -X POST http://127.0.0.1:5984/_replicate -d '{"source":"http://example.org:5984/albums-replica","target":"albums"}' -H "Content-Type:application/json"     

- **远端到远端**

    curl -X POST http://127.0.0.1:5984/_replicate -d '{"source":"http://example.org:5984/albums","target":"http://example.org:5984/albums-replica"}' -H "Content-Type: application/json"            
    