复习要点：第五天「MySQL数据库+Redis数据库」

---

01-关系型数据库与非关系型数据库的区别与使用场景

简单理解：

```
1.关系型数据库通过外键关联来建立表与表之间的关系，
2.非关系型数据库通常指数据以对象的形式存储在数据库中，而对象之间的关系通过每个对象自身的属性来决定
```

区别表格

| 数据库 类型                                                  | 特性                                                         | 优点                                                         | 缺点                                                         |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| RDBMS(Relational Database Management System)              关系型数据库 SQLite、Oracle、mysql、slqserver | 1、关系型数据库，是指采用了关系模型来组织 数据的数据库； 2、关系型数据库的最大特点就是事务的一致性； 3、简单来说，关系模型指的就是二维表格模型， 而一个关系型数据库就是由二维表及其之间的联系所组成的一个数据组织。 | 1、容易理解：二维表结构是非常贴近逻辑世界一个概念，关系模型相对网状、层次等其他模型来说更容易理解； 2、使用方便：通用的SQL语言使得操作关系型数据库非常方便； 3、易于维护：丰富的完整性(实体完整性、参照完整性和用户定义的完整性)大大减低了数据冗余和数据不一致的概率； 4、支持SQL，可用于复杂的查询。 | 1、为了维护一致性所付出的巨大代价就是其读写性能比较差； 2、固定的表结构； 3、不能高并发读写需求； 4、海量数据的高效率读写茶； |
| 非关系型数据库 MongoDb、redis、HBase                         | 1、使用键值对存储数据； 2、分布式； 3、一般不支持ACID特性； 4、非关系型数据库严格上不是一种数据库，应该是一种数据结构化存储方法的集合。 | 1、无需经过sql层的解析，读写性能很高； 2、基于键值对，数据没有耦合性，容易扩展； 3、存储数据的格式：nosql的存储格式是key,value形式、文档形式、图片形式等等，文档形式、图片形式等等，而关系型数据库则只支持基础类型。 | 1、不提供sql支持，学习和使用成本较高； 2、无事务处理，附加功能bi和报表等支持也不好； |

注1：数据库事务必须具备ACID特性，ACID是Atomic原子性，Consistency一致性，Isolation隔离性，Durability持久性。

注2：数据的持久存储，尤其是海量数据的持久存储，还是需要一种关系数据库。

了解更多：

https://blog.csdn.net/chenchaofuck1/article/details/51461529

https://blog.csdn.net/t146lla128xx0x/article/details/78737290 数据库引擎

---

02-关系型数据库的设计

```
数据库设计三范式：
	第一范式（1NF）：强调的是列的原子性，即列不能够再分成其他几列
	第二范式（2NF）：首先是 1NF，另外包含两部分内容，一是表必须有一个主键；二是没有包含在主键中的列必须完全依赖于主键，而不能只依赖于主键的一部分。
	第三范式（3NF）：首先是 2NF，另外非主键列必须直接依赖于主键，不能存在传递依赖。即不能存在：非主键列 A 依赖于非主键列 B，非主键列 B 依赖于主键的情况。
	
简单原则理解：1，将字段拆到不能拆分；2，将表拆到不能拆分；3，在数据表之间建立合适的关系；4，适当的冗余字段可以提高查询效率；	

    
E-R模型：
	E表示entry，实体，设计实体就像定义一个类一样，指定从哪些方面描述对象，一个实体转换为数据库中的一个表
	R表示relationship，关系，关系描述两个实体之间的对应规则，关系的类型包括包括一对一、一对多、多对多
	关系也是一种数据，需要通过一个字段存储在表中
关系类型：
	一对一，一对多，多对多

逻辑删除
    对于重要数据，并不希望物理删除，一旦删除，数据无法找回
    删除方案：设置isDelete的列，类型为bit，表示逻辑删除，默认值为0
    对于非重要数据，可以进行物理删除
    数据的重要性，要根据实际开发决定

扩展阅读：
	58到家数据库30条军规解读：https://mp.weixin.qq.com/s/Yjh_fPgrjuhhOZyVtRQ-SA?

```

---

03-SQL语句与MySQL数据库

```
SQL语句：
	SQL是结构化查询语言，是一种用来操作RDBMS的数据库语言，当前关系型数据库都支持使用SQL语言进行操作,也就是说可以通过 SQL 操作 oracle,sql server,mysql,sqlite 等等所有的关系型的数据库

SQL语句主要分为：
    DQL：数据查询语言，用于对数据进行查询，如select
    DML：数据操作语言，对数据进行增加、修改、删除，如insert、udpate、delete
    TPL：事务处理语言，对事务进行处理，包括begin transaction、commit、rollback
    DCL：数据控制语言，进行授权与权限回收，如grant、revoke
    DDL：数据定义语言，进行数据库、表的管理等，如create、drop
    CCL：指针控制语言，通过控制指针完成表的操作，如declare cursor
对于web程序员来讲，重点是数据的crud（增删改查），必须熟练编写DQL、DML，能够编写DDL完成数据库、表的操作，其它语言如TPL、DCL、CCL【专业DBA人士做的事情】了解即可。
SQL 是一门特殊的语言,专门用来操作关系数据库，不区分大小写

MySQL数据库的特点：
	开源 免费 不要钱 使用范围广,跨平台支持性好,提供了多种语言调用的 API
	更多请查看课件

MySQL数据库的常用数据类型与约束条件：
	可以通过查看帮助文档查阅所有支持的数据类型
	使用数据类型的原则是：够用就行，尽量使用取值范围小的，而不用大的，这样可以更多的节省存储空间
	详细内容请参考课件：03.Python高级和MySQL————MySQL基本使用————数据完整性
```

---

04-MySQL的基本使用与查询操作

```mysql
⚠️：每个命令结束后都要跟上一个分号“;”
数据库操作：
    show databases;
    select database();
    use db_name;
    create database db_name charset=utf8;
    drop database db_name;
数据表操作：
    show tables;
    desc tb_name;
    create table tb_name (
        col_name	dataType [contrai,...]
        ......
    );
    alter table tb_name (add|change|modify|drop) col_name [[new_cl_name] dataType [contrai]];
    drop table tb_name;
    show create table tb_name;
增改查删(curd)：
curd的解释: 代表创建（Create）、更新（Update）、读取（Retrieve）和删除（Delete）
	select col_name,[col_name1,...] from table;
	INSERT [INTO] tb_name [(col_name,...)] {VALUES | VALUE} ({expr | DEFAULT},...),(...),...
	UPDATE tbname SET col1={expr1|DEFAULT} [,col2={expr2|default}]...[where 条件判断]
	DELETE FROM tbname [where 条件判断]
数据备份与恢复：
	mysqldump –uroot –p db_name > xxx.sql;
	mysql -uroot –p db_name < xxx.sql
	第二种恢复的方式：
		进去mysql-client终端：
		use 相应的数据库
		source 备份文件的路径

重点：查询操作总结！！！！！！！：
	查询的完整格式 ^_^ 不要被吓到 其实很简单 ! _ !
    SELECT select_expr [,select_expr,...] [      
          FROM tb_name
          [WHERE 条件判断]
          [GROUP BY {col_name | postion} [ASC | DESC], ...] 
          [HAVING WHERE 条件判断]
          [ORDER BY {col_name|expr|postion} [ASC | DESC], ...]
          [ LIMIT {[offset,]rowcount | row_count OFFSET offset}]
    ]
    执行顺序为：
        from 表名
        where ....
        group by ...
        select distinct *
        having ...
        order by ...
        limit start,count
        实际使用中，只是语句中某些部分的组合，而不是全部
更多操作的名称：
	设置别名，消除重复行，条件，排序，聚合函数，分组，分页，连接，自关联，子查询

```

---

05-MySQL与Python交互

链接数据库的host参数可以使用一个域名，而不是必须要IP地址，前提是有域名解析服务器帮助解析到一个IP地址

自己封装SQL语句的查询比直接使用第三方ORM映射模块的效率更高

```python
# pip3 install pymysql
from pymysql import connect

# 创建Connection连接
conn_ob = connect(
	host='db_host',
    port=3306,
    database='db_name',
    user='root',
    password='mysql',
    charset='utf8'
)
# 获得Cursor对象
cur_ob = conn_ob.cursor()

# 增加
# 执行insert语句，并返回受影响的行数：添加一条数据 
count = cur_ob.execute('insert into goods_cates(name) values("硬盘")')
#打印受影响的行数
print(count)
count = cur_ob.execute('insert into goods_cates(name) values("光盘")')
print(count)

# # 更新
# count = cur_ob.execute('update goods_cates set name="机械硬盘" where name="硬盘"')
# # 删除
# count = cur_ob.execute('delete from goods_cates where id=6')

# 提交之前的操作，如果之前已经之执行过多次的execute，那么就都进行提交
conn_ob.commit()

# 查询
# 执行select语句，并返回受影响的行数：
count = cur_ob.execute('select id,name from goods where id>=4')
# 打印受影响的行数
print("查询到%d条数据:" % count)

# for i in range(count):
#     # 获取查询的结果
#     result = cs1.fetchone()
#     # 打印查询的结果
#     print(result)
#     # 获取查询的结果

result = cur_ob.fetchall()
# 返回的结果是一个元组
print(result)

# 关闭Cursor对象
cur_ob.close()
# 关闭Connection对象
conn_ob.close()
```

---

06-Redis数据基础知识

```
简介：
    Redis是一个开源的使用ANSI C语言编写、支持网络、可基于内存亦可持久化的日志型、Key-Value数据库，并提供多种语言的API。从2010年3月15日起，Redis的开发工作由VMware主持
    Redis是一个开源（BSD许可）的、内存中的数据结构存储系统，它可以用作数据库、缓存和消息中间件
    redis是一个高性能的key-value存储系统。和Memcached类似，它支持存储的value类型相对更多，包括string(字符串)、list(列表)、set(集合)、zset(sortedset--有序集合)和hash（哈希类型）。redis的出现，很大程度补偿了memcached这类key/value存储的不足，在部分场合可以对关系数据库起到很好的补充作用。它提供了Python，Ruby，Erlang，PHP客户端，使用很方便
    Redis支持主从同步。数据可以从主服务器向任意数量的从服务器上同步，从服务器可以是关联其他从服务器的主服务器。这使得Redis可执行单层树复制。从盘可以有意无意的对数据进行写操作。由于完全实现了发布/订阅机制，使得从数据库在任何地方同步树时，可订阅一个频道并接收主服务器完整的消息发布记录。同步对读取操作的可扩展性和数据冗余很有帮助
    
Redis默认有16个数据库可以使用！【0-15】

数据类型与使用注意：
	redis是key-value的数据结构，每条数据都是一个键值对
    键的类型是字符串
    注意：键不能重复
    值的类型分为五种：
        字符串string
        哈希hash
        列表list
        集合set
        有序集合zset
    中文官网查看命令文档：http://redis.cn/commands.html
```

---

07-Redis的终端命令

```redis
键命令：
	keys pattern  查找键，支持正则表达式
	exists key_name	  判断键是否存在，如果存在返回1，不存在返回0
	type key_name 	查看键对应的value的类型
	del key1 key2 ...	删除键及对应的值
	expire key_name seconds	设置过期时间，以秒为单位;如果没有指定过期时间则一直存在，直到使用DEL移除
	ttl key_name  查看剩余有效时间，以秒为单位，如果结果为-2，表示不存在
	
不同类型数据的操作命令：	
    string
        set、setex、mset、append、get、mget
    hash
        hset、hmset、hkeys、hget、hmget、hvals、hdel 
    list
        lpush、rpush、linsert、lrange、lset、lrem
    set
        sadd、smembers、srem
    zset
        zadd、zrange、zrangebyscore、zscore、zrem、zremrangebyscore
   ⚠️：不要硬记，用的时候去查！！！
   记住中文网址：http://redis.cn/commands.html

```

---

08-Redis与Python交互

```python
# pip3 install redis
from redis import StrictRedis

#创建StrictRedis对象，与redis服务器建立连接
sr=StrictRedis(host="db_host", port=6379)
#添加键py1，值为gj
result=sr.set('py1','gj')
#输出响应结果，如果添加成功则返回True，否则返回False
print result
```

⚠️：Python中使用的方法名基本和终端中使用命令名保持一致

了解更多使用技巧：

https://www.cnblogs.com/progor/p/8567640.html

redis的发布和订阅功能可以用来做进程间通讯（单方面的：非常符合生产者消费者开发模式）

https://www.cnblogs.com/alamZ/p/7207784.html

---

09-Redis数据的使用场景：

	保存临时验证数据：session，验证码

	消息中间件：异步发送邮件，【订阅与发布功能】

	分布式锁：利用redis是单线程的特征实现锁定代码中的操作

	对变化较少的数据做缓存，提高查询效率【页面静态化】

	计数器和去重【利用了某些数据类型的特征】

	

	

	