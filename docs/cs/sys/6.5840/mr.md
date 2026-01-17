# MapReduce

> [!abstract]
> - MapReduce 实际是定义了两个接口 Map 和 Reduce：
>       - Map 完成程序逻辑的分发；
>       - Reduce 完成并发结果的规约和收集；
> - paper: [:book: MapReduce: Simplified Data Processing on Large Clusters](http://research.google.com/archive/mapreduce-osdi04.pdf)
> - home: http://nil.csail.mit.edu/6.5840/2025/labs/lab-mr.html

> [!Tip] Lab Materials
> - main/mrcoordinator.go：启动一个 coordinator；
> - main/mrworker.go：加载 wc.so，启动一个 worker；
> - mr/mrsequential.go：以顺序方式运行 MapReduce 任务的参考实现；
> - mr/coordinator.go：初始化 Task，分配 Task，并监测 Task；
> - mr/worker.go：请求任务、处理任务、返回任务完成情况；
> - mr/rpc.go：RPC 的传入和传出参数格式；
> - mr/wc.go：一个简单的 word count MapReduce 程序的实现；

## Task: MapReduce

> [!Question] Task
> - 实现一个分布式的 MapReduce 框架，由 coordinator 和 worker 组成；
> - 系统中只会有一个 coordinator process，但会有一个或多个 worker processes 并行执行；
> - 本次 Lab 只在同一台机器上运行，worker 会通过 RPC 与 coordinator 通信；
> - 每个 worker 会在一个 for 中向 coordinator 请求任务，从一个或多个文件中读取任务的输入，执行任务，将任务的输出写入一个或多个文件，然后再次向 coordinator 请求新任务；
> - coordinator 需要监测 worker 是否在合理的时间内完成了任务，如果没有，则将相同的任务分配给另一个 worker。

<div style="display: flex; justify-content: center;">
  <div style="flex: 1; text-align: center; max-width: 400px;">
    <img src="/assets/images/cs/sys/6.5840/lab1/map.jpg" width=100%>
    <p><strong>Map 阶段</strong>：分散计算，将输入数据分割并并行处理</p>
  </div>
  <div style="flex: 1; text-align: center; max-width: 400px;">
    <img src="/assets/images/cs/sys/6.5840/lab1/reduce.jpg" width=100%>
    <p><strong>Reduce 阶段</strong>：聚合结果，汇总中间结果并生成最终输出</p>
  </div>
</div>

### Coordinator

- Task 分为 MapTask 和 ReduceTask，Coordinator 负责将任务分配给 Worker，并监测任务的完成情况；
- 当所有 Map 任务完成后，Coordinator 会分配 Reduce 任务；
- 如果 Worker 在合理时间内未完成任务，Coordinator 会将任务重新分配给其他 Worker。

### Worker

- Worker 通过 RPC 向 Coordinator 请求任务（MapTask 或 ReduceTask）；
- Worker 执行分配的任务，并将结果写入中间文件；
- Worker 处理完任务后，向 Coordinator 汇报任务完成情况。


## Reference

- [深入浅出讲解 MapReduce](https://www.bilibili.com/video/BV1Vb411m7go/?vd_source=5e048b202705330980eefcc9a56cc5d0)
- [MapReduce 简介](https://airekans.github.io/cloud-computing/2014/01/25/mapreduce-intro)
- [Lec1：入门介绍（以 MapReduce 为例）](https://github.com/chaozh/MIT-6.824/issues/2)