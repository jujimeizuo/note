# Raft

> [!abstract]
> - Raft 是一种复制状态机协议，一个复制服务通过多个副本 server 上存储其状态（数据）的完整副本来实现容错，复制使其即使部分 server 出现故障（崩溃或网络中断、不稳定），服务仍能继续运行，但问题在于，故障可能导致各个副本保存的数据不一致；
> - Raft 将 client requests 组织成一个序列（日志），并确保所有副本 servers 都能看到相同的日志。每个副本按照日志的顺序执行 client requests，将其应用于服务状态的本地副本；
> - 由于所有正常运行的副本都能看到相同的日志内容，它们都会以相同顺序执行相同的 requests，从而保持一致性服务状态；
> - 如果某个 server 发生故障但之后恢复，Raft 会负责使其日志更新到最新状态；
> - 只要至少大多数 server 处于活跃状态且能够相互通信，Raft 就会继续运行；
> - Raft 只能满足 CAP 理论中的 **CP**；
> - paper: :book: [In Search of an Understandable Consensus Algorithm](http://nil.csail.mit.edu/6.5840/2023/papers/raft-extended.pdf)
> - home: https://pdos.csail.mit.edu/6.824/labs/lab-raft1.html
> - [Students' Guide to Raft](https://thesquareplanet.com/blog/students-guide-to-raft/)
> - [Visualization of Raft](https://thesecretlivesofdata.com/raft/)

> [!Tip] Lab Materials
> - raft1/raft.go：Raft 的框架代码，包含发送 `sendRequestVote()` 和接收 `RequestVote()` RPC；
 

## Part 3A: leader election


> [!Question] leader election
> - 实现 Raft 的 leader 选举和 heartbeats 机制（不带日志条目的 AppendEntries RPC）；
> - 目标是选举出一个单一的 leader，在没有故障的情况下该 leader 保持其地位，并且当旧 leader 发生故障或旧 leader 之间的数据包丢失时，有新 leader 接管；


### Raft 节点 & 各参数

1. 单个 raft 节点、RequestVote RPC、AppendEntries RPC 的各个变量需完全遵循 paper 里的**图2**！
2. 每个 raft 节点可以是 leader | candidate | follower，都可以发送和接收 RPC，维护唯一一个运行的 goroutine；
3. 每个 raft 节点都有一个选举定时器，每次收到 heartbeat 或 log 的 RPC 时，都会重置选举定时器，发送者是 leader，接收者是 follwer，一旦选举定时器超时，节点转化为 candidate 并进行投票选举；

### 投票

> `ticker()`：运行在每个节点上，判断是否需要投票。

#### 发送方

- 若当前节点不是 leader 并且上一次心跳间隔 > 选举定时器，就要触发 leader election；
- 变量的定义，state 变为 candidate、term++、给自己投票、重置心跳时间戳等；
- 依次请求其他 raft 节点进行投票 `sendRequestVote()`，注意 term 的变更；
#### 接收方
- `RequestVote()` 接收来自 candidate 的投票请求；
- 根据自己角色的不同采取不同的投票措施，注意 votedFor 的变更;

---

> [!Tip]
> 1. 若投票超半数，则当选 leader 并广播给其他节点，否则重新一轮选举；
> 2. 避免脑裂：每个 candidate 都给自己投票，如果只有两个 follower 并且转化成 candidate 发起选举，都给自己投一票，就会形成脑裂，解决办法就是**随机设置选举定时器的超时时间**，至少超过 leader 的心跳间隔；
> 3. 心跳机制和发起投票是并行的，即使当前 candidate 正在选举，一旦选举计时器出发，应该开始另一次选举，避免 RPC 延迟或丢失；

### 心跳机制

> - leader 在任期期间，会不间断地发送心跳给所有 follower，防止触发超时选举；
> - 和 `AppendEntries()` RPC 相同，只是参数为空，表示发送心跳；

#### 发送方

- 与 `ticker()` 类似，区别在于当前角色是不是 leader，如果是则发送心跳给其他 follower，否则等待；
#### 接收方

- `AppendEntries()`：接收来自 leader 的追加条目，当前 Part 3A 不涉及日志相关，所以只更新一些参数变更如 term、心跳时间戳等；

## Part 3B: log

> [!Question] log
> - 实现日志存储；

> [!Solve]

## Part 3C: persistence

> [!Question] persistence

> [!Solve]

## Part 3D: log compaction

> [!Question] log compaction

> [!Solve]


## Reference

- [【论文解读 第1期】Raft共识算法论文翻译](https://zhuanlan.zhihu.com/p/702642993)
- [解析分布式共识算法之Raft算法](https://www.bilibili.com/video/BV1Kz4y1H7gw?vd_source=c5fdcb7e8bfbd07851554854d73aa1fa)
- [MIT6.5840(6.824)](https://vanilla-beauty.github.io/categories/CS%E8%AF%BE%E7%A8%8B%E7%AC%94%E8%AE%B0/MIT6-5840-6-824-2023/)
