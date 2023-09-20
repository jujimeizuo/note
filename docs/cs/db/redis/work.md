---
counter: true
---

# Redis 事务

## redis的事务操作

**redis的单条命令保证原子性，但是redis的事务不保证原子性**

redis的事务没有隔离级别。redis事务实际上就是一组命令的集合，这些命令在事务中会被序列化，然后按照命令的先后顺序一次性全部执行，在执行的过程中不能被打断。 即：redis的事务在执行时是一次性，顺序性和排他性的

### 开启事务：multi

### 命令入队:

### 执行事务:exec

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632644879581.png)

### 放弃事务：discard

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632644930162.png)

## 事务异常

**在开启事务后，如果编写的命令有语法错误，则会立即报错，且整个事务队列中的所有命令都不会执行.**

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632645058718.png)

**如果在开启事务后，命令中没有语法错误，但是却有运行错误，即命令能够成功入队，但是不能够执行，则在事务提交后只有该命令抛错，其他命令可以正常执行。**

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632645139695.png)

## redis的乐观锁

- 乐观锁：就是它会认为所有的事务都不会失败，因此它不会给事务上锁。它只会在更新的时候判断在此期间是否有人修改过数据
- 悲观锁：它认为所有的事务都会执行失败，因此做任何事情它都会加锁，这样是及其影响效率的。

### redis的乐观锁实现命令：watch

#### 单线程下运行

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632645356164.png)

#### 多线程修改值

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632645487019.png)

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632645565809.png)

![file](http://cdn.jujimeizuo.cn/blog/2021/09/image-1632645644690.png)

#### 如果事务执行失败，需要先解锁，再加锁，解锁命令为：unwatch
