---
counter: True
comment: True
---

# Fault-tolerant Key/Value Service


> [!abstract]
> - 这是一个基于 Raft 和 RSM 的 KV 数据库系统，多个 server 通过 Raft 协议来同步操作日志，保证所有 server 上的状态机保持一致；
> - 与 Lab2 类似，只是该服务并非单一 server，而是多个 server 组成的 Raft 集群；
> - paper: [:book: MapReduce: Simplified Data Processing on Large Clusters](http://research.google.com/archive/mapreduce-osdi04.pdf)
> - home: https://pdos.csail.mit.edu/6.824/labs/lab-kvraft1.html

> [!Tip]
> client.go: 供应用程序调用，发起 `Get()` 和 `Put()`；
> server.go: KV Server，接收 client 的 RPC 请求，并将其提交给 Raft 集群；
> rsm.go：复制状态机层，连接 KV Sotrage 和 Raft 的桥梁，负责将操作提交给 Raft、从 Raft 应用已提交的日志条目到状态机，以及管理快照；
> <center><img src="/assets/images/cs/sys/6.5840/lab4/kvraft.png"></center>

## Part 4A: replicated state machine (RSM)

> [!Question] replicated state machine (RSM)
> - 实现 rsm.go 中的 `Submit()` 和 一个 `reader()` goroutine；
> - 网络分区情况下如何保证数据一致性？
> - raft 节点 kill 时，applyCh 的处理？

### 数据一致性

> 可能因为网络分区、节点宕机等，会发生 leader 改变，client 只有在操作真正被正确的 term 提交、且内容未改动时，才能收到 OK。

- 为了保证数据一致性，rsm 维护一个哈希表 opMap：
    - key 为 Id，表示 op 的唯一 id，可以用 log 的 index 表示；
    - value 为 opEntry，包含期望的 Term、Req 和结果 channel；
- 如何保证数据一致性：
    - opMap 中是否存在 Id：
        - `rsm.opMap[applyMsg.CommandIndex]`
    - Req 比较：从 applyCh 读取到有 log 提交，就可以去应用，但是这个 Req 可能是旧 leader 的未提交 log，因此需要和当前 client 发起的 Req 做对比：
        - `!reflect.DeepEqual(opEntry.Req, op.Req)`
    - Term 比较：Term 的改变可能意味 leader 的改变，旧 leader 的未提交 log 可能会被覆盖：
        - `opEntry.Term != applyMsg.Term`


> [!important] 当 raft 节点 kill 时关闭了 applyCh，而此时 applier 还在把提交的命令发送给 applyCh，导致错误。
> 当 `Kill()` 时，`applyCond.Broadcast()` 唤醒所有等待的 goroutinue，并且用 `sync.WaitGroup` 等待所有 goroutine 退出；

### Submit()

1. 向 raft 使用 `rf.Start()` 等待 raft 提交请求，并发送给 applyCh；
2. 建立 OpEntry，记录期望的 Term、Req 和结果 channel；
3. 用 select 阻塞等待结果；

### reader()

1. 轮询 applyCh，读取已提交的 log；
2. 若 Raft 异常关闭，需要向 opMap 内所有待处理的 opEntry 发送 `ErrWrongLeader`，并清空 opMap 后退出；
3. 若 applyMsg 正确，则执行状态机 `rsm.sm.DoOp(op.Req)`，在加锁前执行，保证每个已提交日志都被应用一次；
    1. 如何保证只应用一次？reader() 从 applyCh 逐个接受日志，raft 本身保证每个已提交日志只应用一次，不会重复发送同一个 `CommandIndex` 的 applyMsg，所以 DoOp 只会执行一次；
    2. 为什么在加锁前？ 因为 DoOp 可能是耗时操作，若在加锁后执行，可能会阻塞其他 goroutine 的访问，影响性能；
4. 三层验证，opMap 是否存在 `CommandIndex`、`Term` 是否匹配、`Req` 是否匹配，正确与否都要做相应处理和回复；

## Part 4B: Key/value service without snapshots

> [!Question] Key/value service without snapshots


## Part 4C: Key/value service with snapshots

> [!Question] Key/value service with snapshots

## Reference

