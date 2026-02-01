---
counter: True
comment: True
---

# C++ Primer

> [!abstract]
> - HyperLogLog 是是一种概率性数据结构，目标是在不明确存储每个项目的情况下，统计海量数据流中唯一条目的数量；
> - 补充了 Spring 2023 的 COW Trie；
> - home: https://15445.courses.cs.cmu.edu/spring2025/project0/

> [!tip] HLL 的概率计数机制
> - `b`: 哈希值二进制表示中初始位的数量；
> - `m=2^b`: 寄存器（桶）数量，可以被视为一个内存块；
> - `p`：1 的最高有效位位置；

## Task 1

> [!question] 实现一个基本的 HyperLogLog，把最左侧 1 bit 的位置存储在寄存器中。
> 实现一个基本的 HyperLogLog，把最左侧 1 bit 的位置存储在寄存器中。

- `ComputeHash(hash)`: 直接调用 `std::bitset<64>` 的构造函数返回二进制即可；
- `PositionOfLeftmostOne(bset)`: 取除了 `n_bits` 以外剩余比特位中最高的 1 bit 的位置；
- `AddElem(val)`: 计算哈希值 `hash`，将其转为二进制并计算寄存器索引 `idx` 和 `p` 值，最后更新寄存器 `R[idx]`；
- `ComputeCardinality`: 使用公式即可 $N = \alpha_m * m^2 * (\sum_{j=0}^{m-1} 2^{-R[j]})^{-1}$；

> [!bug] 注意事项
> - n_bits 可能为负，需 return 处理；
> - 不可以使用 `std::pow(2, -r)`，因为 `r` 是 `uint8_t`，不可以变成负数，所以使用 `1.0 / std::pow(2, r)`；

## Task 2

> [!question] 实现 Presto 的 HLL 密集布局，把最右侧连续 0 的计数存储在寄存器中。
> - 实现 Presto 的 HLL 密集布局，把最右侧连续 0 的计数存储在寄存器中。

- `AddElem(bset)`: 
    1. 计算哈希值 `hash` 并转为二进制；
    3. 计算寄存器索引 `idx`；
    2. 计算最右连续 0 个数作为 `p` 值，分解为 `dense_value` 和 `overflow_value`（如果超过了 `DENSE_BUCKET_SIZE` 位）；
    3. 更新 `dense_bucket_[idx]` 和 `overflow_buckets_[idx]`；
- `ComputeCardinality()`: 
    1. 先从 `dense_bucket_` 和 `overflow_buckets_` 求出 bit （`dense_bucket_value` 和 `overflow_bucket_value`）；
    2. 合并这两个 bit，`merge = dense_bucket_value + (overflow_bucket_value << DENSE_BUCKET_SIZE)`；
    3. 最后使用公式计算基数； 

--- 

## Spring 2023

### Task 1: Copy-On-Write Trie

> [!question] Copy-On-Write Trie
> 修改 `trie.h` 和 `trie.cpp` 来实现一个 Copy-On-Write Trie；

- `Get(key)`：沿着 key 逐字符向下查找节点；如果路径不存在或节点值类型不匹配则返回空，否则返回该值指针。
- `Put(key, value)`：持久化插入/更新；递归创建或克隆路径上的节点，仅替换目标分支并保留其他分支，最后返回新的 Trie 根。
- `Remove(key)`：持久化删除；递归移除目标值并必要时回收空节点，保持其他分支不变，最终返回新的 Trie 根（可能为空）。

### Task 2: Concurrent Key-Value Store

> [!question] Concurrent Key-Value Store
> 在单线程的 Copy-On-Wirte Trie 基础上，实现一个支持多线程的并发 key-value store。

```text
┌───────────────────────────────────┐
│             TrieStore             │  ← 线程安全包装层
│  ┌─────────┐        ┌──────────┐  │
│  │root_lock│        │write_lock│  │  ← 两把锁分工
│  └────┬────┘        └─────┬────┘  │
│       │                   │       │
│       ▼                   ▼       │
│  ┌─────────────────────────────┐  │
│  │        Trie (COW)           │  │
│  │   root_: shared_ptr<const   │  │  ← 不可变数据结构
│  │           TrieNode>         │  │
│  └─────────────────────────────┘  │
└───────────────────────────────────┘
```

- COW Trie 本身是不可变的，所以读操作不需要锁，只需要保护根指针的读取；
- `root_lock_`：保护 `root_` 指针的读写（获取当前版本）
- `write_lock_`：序列化所有修改操作（`Put`/`Remove`）
- `Get(key)`：
    - `root_lock_` 只保护对 `root_` 的读取，获取 `snapshot` 后立刻释放；
    - 后续遍历无需上锁，因为 `snapshot` 是局部副本；
- `Put(key, value)` 和 `Remove(key)`：:
    - `write_lock_` 确保只有一个 writer 执行 `Put` 或 `Remove`，避免并发修改；
    - 实际的 `Trie::Put/Remove` 不在锁内执行，避免阻塞 writer；
    - 使用双锁策略，`write_lock_` 保护序列化，`root_lock_` 保护根指针安全；

> [!note] 为什么需要 `ValueGruad`?
> - 假设这样一个场景：`Get(key)` 返回指针后，另一个线程执行了 `Remove(key)`：
> ```text
> T1: auto val = trie_store.Get<int>("key");  // 获取值引用
> T2: trie_store.Remove("key");               // 删除键，COW 创建新 root
>     // 旧 root 的节点如果没有其他引用会被销毁
> T1: cout << *val;  // 如果 val 只存指针，这里会悬空！
> ```
> - 解决方案：ValueGuard 持有 Trie 的拷贝（root_），确保节点不会被销毁，即使其他线程修改了 TrieStore 的 root_，ValueGuard 持有的旧版本仍然有效（通过 shared_ptr 的引用计数）


