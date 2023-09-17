---
counter: true
---

# Redis 持久化

## 简介

由于redis是内存数据库，所以其数据断电易失，因此需要将数据保存到磁盘中。redis有两种持久化解决方案，分别是：RDB，AOF。

## 快照(Snapshot) / RDB

这种方式可以将某一时刻的所有数据都写入硬盘中,当然这也是redis的默认开启持久化方式,保存的文件是以.rdb形式结尾的文件因此这种方式也称之为RDB方式。

在指定时间间隔后，将内存中的数据集快照写入数据库 ；在恢复时候，直接读取快照文件，进行数据的恢复 ； 默认情况下， Redis 将数据库快照保存在名字为 **dump.rdb**的二进制文件中。文件名可以在配置文件中进行自定义。

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632802020120.png)

### RDB持久化的大致过程

在进行 RDB 的时候，redis 的主线程是不会做 io 操作的，主线程会 fork 一个子线程来完成该操作；

1. Redis 调用forks。同时拥有父进程和子进程。
2. 子进程将数据集写入到一个临时 RDB 文件中。
3. 当子进程完成对新 RDB 文件的写入时，Redis 用新 RDB 文件替换原来的 RDB 文件，并删除旧的 RDB 文件。

**这种工作方式使得 Redis 可以从写时复制（copy-on-write）机制中获益(因为是使用子进程进行写操作，而父进程依然可以接收来自客户端的请求。)**

#### bgsave：

客户端可以使用BGSAVE命令来创建一个快照,当接收到客户端的BGSAVE命令时,redis会调用fork来创建一个子进程,然后子进程负责将快照写入磁盘中,而父进程则继续处理命令请求。 **bgsave 是异步进行，进行持久化的时候，redis 还可以将继续响应客户端请求 ；** ![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632802962900.png)

#### save：

使用 save 命令，会立刻对当前内存中的数据进行持久化 ,但是会阻塞，也就是不接受其他操作了； **由于 save 命令是同步命令，会占用Redis的主进程。若Redis数据非常多时，save命令执行速度会非常慢，阻塞所有客户端的请求。** ![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632802954996.png)

#### shutdown：

当redis通过shutdown指令接收到关闭服务器的请求时,会执行一个save命令,阻塞所有的客户端,不再执行客户端执行发送的任何命令,并且在save命令执行完毕之后关闭服务器

#### 注意:

**SAVE命令并不常用,使用SAVE命令在快照创建完毕之前,redis处于阻塞状态,无法对外服务**

如果用户在redis.conf中设置了save配置选项,redis会在save选项条件满足之后自动触发一次BGSAVE命令,如果设置多个save配置选项,当任意一个save配置选项条件满足,redis也会触发一次BGSAVE命令

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632802337308.png)

### 优点

1. RDB文件紧凑，全量备份，非常适合用于进行备份和灾难恢复。
2. 生成RDB文件的时候，redis主进程会fork()一个子进程来处理所有保存工作，主进程不需要进行任何磁盘IO操作。
3. RDB 在恢复大数据集时的速度比 AOF 的恢复速度要快。

### 缺点

1. 需要一定的时间间隔进程操作！如果redis意外宕机了，这个最后一次修改数据就没有的了！
2. fork进程的时候，会占用一定的内容空间！！

### RDB触发机制

1. save的规则满足的情况下，会自动触发rdb规则
2. 执行 flushall 命令，也会触发我们的rdb规则！
3. 退出redis，也会产生 rdb 文件！

### 配置生成快照名称和位置

1. 修改生成快照名称 dbfilename dump.rdb
2. 修改生成位置 dir ./

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632802467233.png)

### 恢复rdb文件

1. 只需要将rdb文件放在redis启动目录中，redis启动时自动检查dump.rdb恢复其中的数据。
2. 查看其存在的位置

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632802829210.png) 如果/var/lib/redis这个目录存在dump.rdb文件，则启动时自动恢复数据。

## AOF

Append Only File

将我们所有的命令都记录下来，history，恢复的时候就把这个文件全部再执行一遍

### 什么是AOF

快照功能（RDB）并不是非常耐久（durable）： 如果 Redis 因为某些原因而造成故障停机， 那么服务器将丢失最近写入、以及未保存到快照中的那些数据。 从 1.1 版本开始， Redis 增加了一种完全耐久的持久化方式： AOF 持久化。

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632815754859.png)

### 特点

这种方式可以将所有客户端执行的写命令记录到日志文件中,AOF持久化会将被执行的写命令写到AOF的文件末尾,以此来记录数据发生的变化,因此只要redis从头到尾执行一次AOF文件所包含的所有写命令,就可以恢复AOF文件的记录的数据集.

### 开启AOF持久化

在redis的默认配置中AOF持久化机制是没有开启的，需要在配置中开启

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632815844362.png)

appendonly no yes则表示启用AOF

默认是不开启的，我们需要手动配置，然后重启redis，就可以生效了！

如果这个aof文件有错位，这时候redis是启动不起来的，我需要修改这个aof文件

redis给我们提供了一个工具redis-check-aof --fix

### 日志追加频率

```bash
修改日志同步频率
- 修改appendfsync everysec|always|no 指定
```

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632815884193.png)

### AOF文件的重写

#### AOF带来的问题

AOF的方式也同时带来了另一个问题。持久化文件会变的越来越大。例如我们调用incr test命令100次，文件中必须保存全部的100条命令，其实有99条都是多余的。因为要恢复数据库的状态其实文件中保存一条set test 100就够了。为了压缩aof的持久化文件Redis提供了AOF重写(ReWriter)机制。

#### AOF重写

用来在一定程度上减小AOF文件的体积

#### 触发机制

```bash
# 1.客户端方式触发重写
- 执行BGREWRITEAOF命令  不会阻塞redis的服务
# 2.服务器配置方式自动触发
- 配置redis.conf中的auto-aof-rewrite-percentage选项 参加下图↓↓↓
- 如果设置auto-aof-rewrite-percentage值为100和auto-aof-rewrite-min-size 64mb,并且启用的AOF持久化时,那么当AOF文件体积大于64M,并且AOF文件的体积比上一次重写之后体积大了至少一倍(100%)时,会自动触发,如果重写过于频繁,用户可以考虑将auto-aof-rewrite-percentage设置为更大
```

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632816040606.png)

#### 重写原理

**注意：重写aof文件的操作，并没有读取旧的aof文件，而是将整个内存中的数据库内容用命令的方式重写了一个新的aof文件,替换原有的文件这点和快照有点类似。**

```bash
# 重写流程
- 1. redis调用fork ，现在有父子两个进程 子进程根据内存中的数据库快照，往临时文件中写入重建数据库状态的命令
- 2. 父进程继续处理client请求，除了把写命令写入到原来的aof文件中。同时把收到的写命令缓存起来。这样就能保证如果子进程重写失败的话并不会出问题。
- 3. 当子进程把快照内容写入已命令方式写到临时文件中后，子进程发信号通知父进程。然后父进程把缓存的写命令也写入到临时文件。
- 4. 现在父进程可以使用临时文件替换老的aof文件，并重命名，后面收到的写命令也开始往新的aof文件中追加。
```

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632816192423.png)

### 优点

1. 每一次修改都会同步，文件的完整性会更加好
2. 没秒同步一次，可能会丢失一秒的数据
3. 从不同步，效率最高

### 缺点

1. 相对于数据文件来说，aof远远大于rdb，修复速度比rdb慢！
2. Aof运行效率也要比rdb慢，所以我们redis默认的配置就是rdb持久化

## 如何选择哪种持久化方式

一般来说， 如果想达到足以媲美 PostgreSQL 的数据安全性， 你应该同时使用两种持久化功能。

如果你非常关心你的数据， 但仍然可以承受数分钟以内的数据丢失， 那么你可以只使用 RDB 持久化。

有很多用户都只使用 AOF 持久化， 但并不推荐这种方式： 因为定时生成 RDB 快照（snapshot）非常便于进行数据库备份， 并且 RDB 恢复数据集的速度也要比 AOF 恢复的速度要快。
