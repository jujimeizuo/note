---
counter: True
comment: True
---

# Key/Value Server

> [!abstract]
> - Key/Value Server 确保即使出现网络故障，每个 `Put` 最多执行一次，并且所有操作都是可线性化的；并且使用这个 Server 实现一个锁；后续实验也对类似的 Server 进行复制，以应对服务器崩溃的情况。
> - home: https://pdos.csail.mit.edu/6.824/labs/lab-kvsrv1.html

> [!Tip] Lab Materials
> - kvsrv1/client.go：实现了一个 Clerk，Client 使用它来管理与 Server 的 RPC 交互；Clerk 提供了 `Put` 和 `Get` 方法；
> - kvsrv1/server.go：实现 RPC requests Server 的 `Put` 和 `Get` handlers；
> - kvsrv1/rpc/rpc.g：RPC requests、replies 和 error；
> - kvsrv1/lock/lock.go：`Acquire` 和 `Release` 对锁操作；

## Task1

> [!Question] Key/value server with reliable network
> 实现在一个没有信息丢失时能正常工作的解决方案。

> [!Solve]
> - 每个 Client 通过 Clerk 与 KV Server 交互，Clerk 向服务器发送 RPC；
> - Client 可以向服务器发送 2 种不同 RPC：`Put(key, value, version)` 和 `Get(key)`；
> - Server 维护一个 kvMap，为每个 key 记录一个 (value, version)；
> - version 记录了该 key 被写入的次数；
> - 只有当 `Put` 的 version 与 Server 上的该 key 的 version 匹配时，`Put` 才会在 kvMap 中更新 value；
>       - 如果 version 匹配，Server 还会将该 key 的 version 加 1；
>       - 如果 version 不匹配，Server 应 return rpc.ErrVersion；
> - 如果 `Put` 的 version > 0 且该 key 不存在，Server 应 return rpc.ErrNoKey；
> - Client 可以通过调用 version 为 0 的 `Put` 来创建新 key（Server 存储的 version 为 1）。


## Task2

> [!Question] Implementing a lock using key/value clerk
> - 在 `clientClerk.Put` 和 `clientClerk.Get` 的调用之上实现一个锁；
> - 锁支持 `Acquire` 和 `Release` 操作；
> - 同一时间只有一个 Client 能获取锁，其他 Client 必须等待，直到第一个 Client 释放锁。

> [!Solve]
> - 把锁的信息以 kv 的形式存进 Server；
> - 将 l 作为 key，把 kvtest.RandValue(8) 作为 value 存进 kv server 中；
> - 用 `Get` 获取锁的状态，`Put` 改变锁的状态；

## Task3

> [!Question] Key/value server with dropped messages
> - 网络可能会对 RPC requests 或 reply 进行重新排序、延迟处理或丢弃，为了从被丢弃的 requests 或 reply 中恢复，client 必须持续重传 RPC，直到收到 server 的 reply 为止；
> - 如果网络丢弃了一条 RPC request，那么 client 重新发送该 request 就能解决问题，server 将会接收并执行重新发送的 request；
> - 然而，网络也可能会丢弃一条 RPC reply，client 并不知道哪条消息被丢弃了，它只知道自己没有收到 reply；
>       - 如果被丢弃的是 reply，而 client 重新发送 RPC request，那么 server 将会收到两份 request；这对于 `Get` 没有问题，因为 `Get` 不修改 server 的状态，重新发送带有相同 version 的 `Put` 也没有问题，因为 server 会根据 version 有条件地执行 `Put`；如果 server 已经接收并执行了该 `Put`，它会对重传的该 RPC 返回 rpc.ErrVersion，而不会再次执行 `Put`；
> - 如果 server 在响应 client 重传的 RPC 时返回了 rpc.ErrVersion：
>       - 客户端无法知道自己的 `Put` 是否被 server 执行，第一次 RPC 可能已被 server 执行，但网络可能丢弃了 server 的成功响应，因此 server 仅对重传的 RPC 返回 rpc.ErrVersion；
>       - 也可能在 client 的第一次 RPC 到达 server 之前，另一个 client 已更新了该 key，导致 server 未执行该 client 的任何一次 RPC，并对两次 RPC 都返回了 rpc.ErrVersion；
> - 如果 client 在重传的 `Put` 中收到 rpc.ErrVersion，client 的 `Put` 必须向应用程序返回 rpc.ErrMaybe 而非 rpc.ErrVersion，因为该 request 可能已被执行；之后，就由应用程序来处理这种情况；
> 如果 server 在对初始（未重传）的 `Put` 的响应中返回 rpc.ErrVersion，那么 client 应向应用程序返回 rpc.ErrVersion，因为该 RPC 肯定未被 server 执行；


> [!Solve]
> - 当网络出现丢弃时，client 需要重发；
> - client 重发时，需要等待一会儿，time.Sleep(100 * time.Millisecond)；

## Task4

> [!Question] Implementing a lock using key/value clerk and unreliable network
> 修改锁的实现，使其在网络不可靠时能与修改后的 key/value client 正确工作。

> [!Solve]
> - Task3 在 client 已经针对不可靠网络做了重发，但是这个重发不等于 `Get` 和 `Put` 一定会成功，只能保证 client 最终收到 server 的消息，但这个消息可能并不是想要的结果，所以在 lock.go 还要对 `Acquire` 和 `Release` 做修改，尤其是 `Release` 的返回值作判断，并加上重发机制；
