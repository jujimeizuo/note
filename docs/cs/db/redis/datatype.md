# Redis 数据类型

# 1\. NoSQL

NoSQL(Not Only SQL )，意即不仅仅是SQL, 泛指非关系型的数据库。Nosql这个技术门类,早期就有人提出,发展至2009年趋势越发高涨。

## 1.1 单机Mysql时代

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632646360378.png)

## 1.2 Memcached(缓存) + Mysql + 垂直拆分（读写分离）

网站80%的情况都是在读，每次都要去查询数据库的话就十分的麻烦！所以说我们希望减轻数据库的压力，我们可以使用缓存来保证效率！ ![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632646410269.png)

## 1.3 分库分表 + 水平拆分 + Mysql集群

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632646422141.png)

## 1.4 如今最近的年代

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632646442039.png)

# 2\. 为什么是NoSQL

**NoSQL = Not Only SQL（不仅仅是SQL）**

Not Only Structured Query Language

关系型数据库：列+行，同一个表下数据的结构是一样的。

非关系型数据库：数据存储没有固定的格式，并且可以进行横向扩展。

NoSQL泛指非关系型数据库，随着web2.0互联网的诞生，传统的关系型数据库很难对付web2.0时代！尤其是超大规模的高并发的社区，暴露出来很多难以克服的问题，NoSQL在当今大数据环境下发展的十分迅速，Redis是发展最快的。

随着互联网网站的兴起，传统的关系数据库在应付动态网站，特别是超大规模和高并发的纯动态网站已经显得力不从心，暴露了很多难以克服的问题。如商城网站中对**商品数据频繁查询**、**对热搜商品的排行统计**、**订单超时问题**、以及**微信朋友圈（音频，视频）存储**等相关使用传统的关系型数据库实现就显得非常复杂，虽然能实现相应功能但是在性能上却不是那么乐观。nosql这个技术门类的出现，更好的解决了这些问题，它告诉了世界不仅仅是sql。

**了解：3V + 3高**

大数据时代的3V ：主要是描述问题的

1. 海量Velume
2. 多样Variety
3. 实时Velocity

大数据时代的3高 ： 主要是对程序的要求

1. 高并发
2. 高可扩
3. 高性能

# 3\. NoSQL的四大分类

## 3.1 键值(Key-Value)存储数据库

```bash
# 1.说明: 
- 这一类数据库主要会使用到一个哈希表，这个表中有一个特定的键和一个指针指向特定的数据。
# 2.特点
- Key/value模型对于IT系统来说的优势在于简单、易部署。  
- 但是如果DBA只对部分值进行查询或更新的时候，Key/value就显得效率低下了。
# 3.相关产品
- Tokyo Cabinet/Tyrant,
- Redis
- SSDB
- Voldemort 
- Oracle BDB
```

## 3.2 列存储数据库

```bash
# 1.说明
- 这部分数据库通常是用来应对分布式存储的海量数据。
# 2.特点
- 键仍然存在，但是它们的特点是指向了多个列。这些列是由列家族来安排的。
# 3.相关产品
- Cassandra、HBase、Riak.
```

## 3.3 文档型数据库

```bash
# 1.说明
- 文档型数据库的灵感是来自于Lotus Notes办公软件的，而且它同第一种键值存储相类似该类型的数据模型是版本化的文档，半结构化的文档以特定的格式存储，比如JSON。文档型数据库可 以看作是键值数据库的升级版，允许之间嵌套键值。而且文档型数据库比键值数据库的查询效率更高
# 2.特点
- 以文档形式存储
# 3.相关产品
- MongoDB、CouchDB、 MongoDb(4.x). 国内也有文档型数据库SequoiaDB，已经开源。  
```

## 3.4 图形(Graph)数据库

```bash
# 1.说明
- 图形结构的数据库同其他行列以及刚性结构的SQL数据库不同，它是使用灵活的图形模型，并且能够扩展到多个服务器上。
- NoSQL数据库没有标准的查询语言(SQL)，因此进行数据库查询需要制定数据模型。许多NoSQL数据库都有REST式的数据接口或者查询API。
# 2.特点
# 3.相关产品
- Neo4J、InfoGrid、 Infinite Graph、
```

# 4\. NoSQL应用场景

- 数据模型比较简单
- 需要灵活性更强的IT系统
- 对数据库性能要求较高
- 不需要高度的数据一致性

# 5\. 什么是Redis

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632473946054.png)

Redis 开源 遵循BSD 基于内存数据存储 被用于作为 数据库 缓存 消息中间件 **redis是一个内存型的数据库**

# 6\. Redis特点

- Redis是一个高性能key/value内存型数据库
- Redis支持丰富的数据类型
- Redis支持持久化
- Redis单线程,单进程

**单线程不一定比多线程慢，在CPU中，多线程需要跳转，而单线程不需要，减少了跳转的消耗，所以在某些场景里单线程可能比多线程快。**

# 7\. Ridis安装

略

# 8\. redis常用命令

## 8.1 set get命令，存值，取值

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632474345917.png)

## 8.2 切换数据库，redis默认有16个数据库，默认使用0号数据库，可以通过select切换

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632474418121.png)

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632474452155.png)

## 8.3 清空当前数据库：flushdb,清空所有数据库：flushall

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632474513302.png)

## 8.4 查询所有key: keys\*

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632474553482.png)

## 8.5 查询数据库的大小：dbsize

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632474583601.png)

## 8.6 查看key是否存在：exists keyName,存在返回1，否则返回0

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632474622298.png)

## 8.7 移除Key: move keyName 1

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632474665561.png)

## 8.8 为key设置过期时间: expire keyName timeout

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632474717857.png)

## 8.9 查看key的剩余存活时间：ttl keyName

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632474728589.png)

## 8.10 查看key的类型：type keyName

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632474775307.png)

# 9\. String详解

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632643699298.png)

```bash

| 命令                        | 说明                      |
| ------------------------- | ----------------------- |
| set                       | 设置一个key/value           |
| get                       | 根据key获得对应的value         |
| mset                      | 一次设置多个key value         |
| mget                      | 一次获得多个key的value         |
| getset                    | 获得原始key的值，同时设置新值        |
| strlen                    | 获得对应key存储value的长度       |
| append                    | 为对应key的value追加内容        |
| getrange 索引0开始            | 截取value的内容              |
| setex                     | 设置一个key存活的有效期（秒）        |
| psetex                    | 设置一个key存活的有效期（毫秒）       |
| setnx                     | 存在不做任何操作,不存在添加          |
| msetnx原子操作(只要有一个存在不做任何操作) | 可以同时设置多个key,只有有一个存在都不保存 |
| decr                      | 进行数值类型的-1操作             |
| decrby                    | 根据提供的数据进行减法操作           |
| Incr                      | 进行数值类型的+1操作             |
| incrby                    | 根据提供的数据进行加法操作           |
| Incrbyfloat               | 根据提供的数据加入浮点数            |
```

## 9.1 strlen:求value的长度，append：追加

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632475047844.png)

## 9.2 自增,自减操作：incr incrby decr decrby

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632475096207.png)

## 9.3 字符串的范围操作：getrange,setrange

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632475184254.png)

## 9.4 设置过期时间：setex（如果存在Key则覆盖，不存在则创建），setnx(如果不存在就设置)

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632475254467.png)

## 9.5 批量设置和获取值：mset,mget, msetnx(操作为原子性，要么都成功，要么都失败)

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632475380084.png)

## 9.6 存取对象

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632475484205.png)

## 9.7 组合操作：getset先获取再设置,如果不存在就返回nil

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632475553716.png)

> String类似的使用场景：value除了是我们的字符串还可以是我们的数字！
> 
> - 计数器
> - 统计多单位的数量
> - 粉丝数
> - 对象缓存存储

# 10\. list详解

list的命令都是l开头,list 列表 相当于java中list 集合 特点 元素有序 且 可以重复

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632643911652.png)

```bash
| 命令      | 说明                    |
| ------- | --------------------- |
| lpush   | 将某个值加入到一个key列表头部      |
| lpushx  | 同lpush,但是必须要保证这个key存在 |
| rpush   | 将某个值加入到一个key列表末尾      |
| rpushx  | 同rpush,但是必须要保证这个key存在 |
| lpop    | 返回和移除列表左边的第一个元素       |
| rpop    | 返回和移除列表右边的第一个元素       |
| lrange  | 获取某一个下标区间内的元素         |
| llen    | 获取列表元素个数              |
| lset    | 设置某一个指定索引的值(索引必须存在)   |
| lindex  | 获取某一个指定索引位置的元素        |
| lrem    | 删除重复元素                |
| ltrim   | 保留列表中特定区间内的元素         |
| linsert | 在某一个元素之前，之后插入新元素      |
```

## 10.1 左插：lpush,左删：lpop

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632475948773.png)

## 10.2 右插：rpush,右删：rpop

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632476072915.png)

## 10.3 获取列表元素：lrange

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632476697115.png)

## 10.4 通过下标获取元素：lindex

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632476474867.png)

## 10.5 获取列表长度：llen

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632476522194.png)

## 10.6 移除具体的值所在的键值对:lrem 列表 移除几个 移除的具体value

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632476605108.png)

## 10.7 截取操作：ltrim 列表 截取的开始下标 截取的结束下标

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632476724171.png)

## 10.8 rpoplpush:移除列表中的最后一个元素并将这个元素放到一个新的列表中

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632476771483.png)

## 10.9 判断列表是否存在：EXISTS list

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632476803379.png)

## 10.10 lset:更新列表中指定下标的元素的value,前提是该下标必须有值，否则报错

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632476840575.png)

## 10.11 在列表中插入值：前插和后插：linsert

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632476896464.png)

# 11\. set详解

set是无序不重复集合，set命令都是s开头 ![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632643954408.png)

```bash
| 命令          | 说明                        |
| ----------- | ------------------------- |
| sadd        | 为集合添加元素                   |
| smembers    | 显示集合中所有元素 无序              |
| scard       | 返回集合中元素的个数                |
| spop        | 随机返回一个元素 并将元素在集合中删除       |
| smove       | 从一个集合中向另一个集合移动元素 必须是同一种类型 |
| srem        | 从集合中删除一个元素                |
| sismember   | 判断一个集合中是否含有这个元素           |
| srandmember | 随机返回元素                    |
| sdiff       | 去掉第一个集合中其它集合含有的相同元素       |
| sinter      | 求交集                       |
| sunion      | 求和集                       |
```

## 11.1 添加：sadd

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632477064797.png)

## 11.2 查看所有: smembers

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632477127825.png)

## 11.3 查询set的元素个数：scard

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632477143763.png)

## 11.4 判断set中是否存在某元素：sismember

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632477172245.png)

## 11.5 移除某个元素：srem

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632477185068.png)

## 11.6 随机抽取一个元素：SRANDMEMBER

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632477211405.png)

## 11.7 随机移除一个元素：spop

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632477222068.png)

## 11.8 将一个集合中的元素移动到另一个集合中：smove

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632477296157.png)

## 11.9 集合之间求交并补集：sinter sunite sdiff

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632477331468.png)

### 差集sdiff

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632477435541.png)

### 交集sinter

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632477391019.png)

### 并集sunion

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632477447668.png)

# 12\. hash详解

hash的形式：key filed vlaue,相当于java中的map集合 hash命令都是h开头

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632643989267.png)

```bash
| 命令           | 说明              |
| ------------ | --------------- |
| hset         | 设置一个key/value对  |
| hget         | 获得一个key对应的value |
| hgetall      | 获得所有的key/value对 |
| hdel         | 删除某一个key/value对 |
| hexists      | 判断一个key是否存在     |
| hkeys        | 获得所有的key        |
| hvals        | 获得所有的value      |
| hmset        | 设置多个key/value   |
| hmget        | 获得多个key的value   |
| hsetnx       | 设置一个不存在的key的值   |
| hincrby      | 为value进行加法运算    |
| hincrbyfloat | 为value加入浮点值     |
```

## 12.1 向hash中添加值：hset

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632477692339.png)

## 12.2 得到hash中的指定filed的值：hget

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632477703371.png)

## 12.3 得到hash中的所有值:hgetall

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632477745829.png)

## 12.4 批量添加和获取：hmset hmget

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632477816044.png)

## 12.5 删除指定的字段：hdel

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632477844890.png)

## 12.6 获取hash的字段长度：hlen

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632477866011.png)

## 12.7 判断hash中的字段是否存在：hexist

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632477881187.png)

## 12.8 获取所有的key(字段)hkeys,获取所有的value：hvals

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632477896459.png)

## 12.9 指定增量：hincrby

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632477919981.png)

**hash变更的数据 user name age,尤其是是用户信息之类的，经常变动的信息！ hash 更适合于对象的存储，String更加适合字符串存储！**

# 13\. Zset详解

zset是有序不可重复的集合,zset命令都是z开头 ![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632644102803.png)

```bash
| 命令                     | 说明             |
| ---------------------- | -------------- |
| zadd                   | 添加一个有序集合元素     |
| zcard                  | 返回集合的元素个数      |
| zrange 升序 zrevrange 降序 | 返回一个范围内的元素     |
| zrangebyscore          | 按照分数查找一个范围内的元素 |
| zrank                  | 返回排名           |
| zrevrank               | 倒序排名           |
| zscore                 | 显示某一个元素的分数     |
| zrem                   | 移除某一个元素        |
| zincrby                | 给某个特定元素加分      |
```

## 13.1 添加数据：zadd

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632478034715.png)

## 13.2 获取所有值,按照索引获取：zrange

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632478071159.png)

## 13.3 获取所有值，按照score获取：zrangebyscore

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632478107108.png)

## 13.4 移除元素：zrem

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632478230841.png)

## 13.5 得到元素的个数:zcard

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632478172600.png)

## 13.6 获取指定区间的成员数量：zcount

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632478326343.png)

**ZSET 官方 可排序SET sortSet**

# 14\. geospatial

# 15\. bitmaps

**bitmap即位存储，适用于只有两面性的内容。如：可以用bitmap存储用户是否登录，是否注册，是否打卡等等。bitmap的值只有0和1两个值。**

## 15.1 存储数据：setbit

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632644429996.png)

## 15.2 获取指定下标的值：getbit

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632644452415.png)

## 15.3 统计bitmap中1的位数：bitcount

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632644484448.png)

# 16\. hyperloglogs

**用于统计基数（即不重复的数据）,可以用于统计网页访问量**

## 16.1 添加：pfadd

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632644672064.png)

## 16.2 计数：pfcount

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632644689711.png)

## 16.3 合并：pfmerge

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632644719576.png)
