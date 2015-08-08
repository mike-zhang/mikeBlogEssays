# python操作couchDB

安装python couchDb库：

[https://pypi.python.org/pypi/CouchDB/0.10](https://pypi.python.org/pypi/CouchDB/0.10)
    
    
连接服务器

    >>> import couchdb
    >>> couch = couchdb.Server('http://example.com:5984/')

创建数据库

    >>> db = couch.create('test') # 新建数据库
    >>> db = couch['mydb'] # 使用已经存在的数据库

创建文档并插入到数据库：

    >>> doc = {'foo': 'bar'}
    >>> db.save(doc)
    ('e0658cab843b59e63c8779a9a5000b01', '1-4c6114c65e295552ab1019e2b046b10e')
    >>> doc
    {'_rev': '1-4c6114c65e295552ab1019e2b046b10e', 'foo': 'bar', '_id': 'e0658cab843b59e63c8779a9a5000b01'}

    save()方法会返回'_id','_rev'字段

通过id查询数据库

    >>> db['e0658cab843b59e63c8779a9a5000b01']
    <Document 'e0658cab843b59e63c8779a9a5000b01'@'1-4c6114c65e295552ab1019e2b046b10e' {'foo': 'bar'}>

更新文档 ：
    
    >>> data = db["5fecc0d7fe5acac6b46359b5eec4f3ff"]    
    >>> data['billSeconds'] = 191
    >>> db.save(data)
    (u'5fecc0d7fe5acac6b46359b5eec4f3ff', u'3-6b8a6bb9f2428c510dcacdd5c918d632') 
    
    
遍历数据库

    >>> for id in db:
    ...     print id
    ...
    'e0658cab843b59e63c8779a9a5000b01'

删除文档并清理数据库

    >>> db.delete(doc)
    >>> couch.delete('test') 

