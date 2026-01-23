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
> - raft1/raft.go：Raft 的框架代码；
> - raft1/raft_test.go：Lab 3 的所有测试代码，必要时要自己构造测试，然后 debug 发现问题；
 

## Part 3A: leader election


> [!Question] leader election
> - 实现 Raft 的 leader 选举和 heartbeats 机制（不带日志条目的 AppendEntries RPC）；
> - 目标是选举出一个单一的 leader，在没有故障的情况下该 leader 保持其地位，并且当旧 leader 发生故障或旧 leader 之间的数据包丢失时，有新 leader 接管；
> - 选举定时器的重置时机；


### Raft 节点

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
### 心跳机制

> leader 在任期期间，会不间断地发送心跳给所有 follower，防止触发超时选举；

#### 发送方

- 采用轮询的方式，设置一个心跳间隔，依次发送心跳；
- 与投票类似，区别在于当前角色是不是 leader，如果是则发送心跳给其他 follower，否则等待；
#### 接收方

- `AppendEntries()`：接收来自 leader 的心跳或日志，当前 Part 3A 不涉及日志相关，所以只更新一些参数变更如 term、心跳时间戳等；

---

> [!Tip]
> 1. 若投票超半数，则当选 leader 并广播给其他节点，否则重新一轮选举；
> 2. **避免脑裂**：每个 candidate 都给自己投票，如果只有两个 follower 并且转化成 candidate 发起选举，都给自己投一票，就会形成脑裂，解决办法就是**随机设置选举定时器的超时时间**，并且至少超过 leader 的心跳间隔；
> 3. 心跳机制和发起投票是并行的，即使当前 candidate 正在选举，一旦选举计时器出发，应该开始另一次选举，避免 RPC 延迟或丢失；

## Part 3B: log

> [!Question] log
> - 实现日志存储；
> - 心跳和日志的区别？
> - 日志的两阶段提交如何实现？日志复制的逻辑？
> - leader 和 follower 接收到新的日志时，各个 index 如何处理？
> - 如果 follower 的日志不一致时如何恢复？
> - 但 follower 的日志不一致时，有无优化机制用于减少日志同步的 RPC 次数，而非逐条日志回退？

### 心跳和日志

- 日志是带有 logEntry 的心跳；
- 每个节点都需要将 log 写入到磁盘中；
- 心跳仅有 Term，而日志还带有 Command；
- leader 除了维护自己的 log，还要同步 follower 的 log，必要时解决冲突；
- 心跳和日志都使用同一个发射器，通过 `nextIndex` 和 `len(log)` 的大小来判断是心跳还是日志；
- 为了简化操作，心跳和日志共同使用 `AppendEntries` RPC 来处理；

### Start()

- 仅仅将 command 追加到 leader 的 log 中，不需要保证 command 是否提交，交给心跳/日志协程处理；

### 两阶段提交

#### 日志复制
1. **客户端请求**：leader 收到 client 的 command 后，追加到自己的本地 log 中；
2. **并发分发**：leader 通过 `AppendEntries` RPC 将这条日志并行地分发到集群中的所有 follower；
3. **预持久化**：follower 收到日志后，会先处理冲突日志，保证不冲突会将其追加到自己的本地 log 中（此时日子处于未提交/不安全状态），并向 leader 返回 `Sucess = true`；
#### 日志提交
1. **达成多数派**：当 leader 收到超过半数的 true 时，认为该日志已经安全；
2. **更新 commitIndex**：leader 将这条日志标记为 `commited`，并 applied 到自己的状态机中；
3. **通知 follower**：leader 在之后的心跳中，会携带最新的 `LeaderCommit` 索引，follower 收到后也会将该日志 applied 到自己的状态机中。

### 应用状态机

- 同样是一个轮询的协程，用条件变量来实现；
- 不断检查 `rf.commitIndex > rf.lastApplied`，然后封装 ApplyMsg 并通过 applyCh 发送给应用层；

### 快速回退

> [!Question] RPC 次数
> 当日志冲突时，如果采用逐条日志回退，导致 `AppendEntries` 的 RPC 次数增多，所以采用快速回退的优化机制，能使 leader 能够一次性地跳过整个冲突的 Term，减少 RPC 次数。

- 日志冲突条件：`len(rf.log) <= args.PrevLogIndex || rf.log[args.PrevLogIndex].TermId != args.PrevLogTermId`；
- 定义三个变量 XTerm、XLen、XIndex：
	- XTerm：冲突 log 对应的 Term，如果 PrevLogIndex 位置上没有 log 则为 -1；
	- XIndex：follower 上对应 Term 为 XTerm 的第一条 Log 的 index；
	- XLen：follower 日志的实际总长度；
#### follower 发现日志冲突

```go
// fast rollback
reply.XLen = len(rf.log)
if len(rf.log) <= args.PrevLogIndex {
	reply.XTerm = -1
	reply.XIndex = -1
} else if rf.log[args.PrevLogIndex].TermId != args.PrevLogTermId {
	reply.XTerm = rf.log[args.PrevLogIndex].TermId
	reply.XIndex = args.PrevLogIndex
	for reply.XIndex > 0 && rf.log[reply.XIndex-1].TermId == reply.XTerm {
		reply.XIndex -= 1
	}
}
```

#### leader 调整日志冲突

```go
if reply.XTerm == -1 {
	rf.nextIndex[server] = reply.XLen
} else {
	if rf.log[reply.XIndex].TermId != reply.XTerm {
		rf.nextIndex[server] = reply.XIndex
	} else {
		for j := reply.XIndex; j < len(rf.log); j++ {
			if rf.log[j].TermId != reply.XTerm {
				rf.nextIndex[server] = j
				break
			}
		}
	}
}
```

#### follower 处理日志冲突

```go
conflictIndex := -1
for i, entry := range args.Entries {
	index := args.PrevLogIndex + 1 + i
	if index >= len(rf.log) {
		break
	}
	if rf.log[index].TermId != entry.TermId {
		conflictIndex = index
		break
	}
}
if conflictIndex != -1 {
	rf.log = rf.log[:conflictIndex]
}
```

---

> [!Tip]
> paper 中图2说到：“**at least as up-to-date as receiver’s log, grant vote**”，因此判断的条件有两个：（而我踩的坑是 "index≥"且"term≥"）
> - `LastLogTerm > rf.log[len(rf.log)-1].TermId`
> - `LastLogTerm == rf.log[len(rf.log)-1].TermId && LastLogIndex ≥ len(rf.log)-1`

## Part 3C: persistence

> [!Question] persistence



## Part 3D: log compaction

> [!Question] log compaction




## Reference

- [【论文解读 第1期】Raft共识算法论文翻译](https://zhuanlan.zhihu.com/p/702642993)
- [解析分布式共识算法之Raft算法](https://www.bilibili.com/video/BV1Kz4y1H7gw?vd_source=c5fdcb7e8bfbd07851554854d73aa1fa)
- [MIT6.5840(6.824)](https://vanilla-beauty.github.io/categories/CS%E8%AF%BE%E7%A8%8B%E7%AC%94%E8%AE%B0/MIT6-5840-6-824-2023/)
