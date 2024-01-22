---
counter: true
comment: true
---

# MPI 基础

!!! abstract
    参考：
    
    - [MPI 并行编程入门](https://scc.ustc.edu.cn/_upload/article/files/e0/98/a9f0c4964abdb3281233d7943f9e/W020121113517561886972.pdf)

## MPI 简介

- 什么是 MPI
    - 是函数库规范，而不是并行语言；操作如同库函数调用
    – 是一种标准和规范，而非某个对它的具体实现（MPICH等），与编程语言无关
    – 是一种消息传递编程模型，并成为这类编程模型的代表
- MPI 的产生
    - 扩充并行 I/O
    - 远程存储访问
    - 动态进程管理
- MPI 的语言绑定: Fortran、C
- 主要的 MPI 实现: MPICH、LAMMPI
- MPI 程序编译与运行
    - 程序编译：
        - C: `#!c %mpicc -o prog prog.c`
        - Fortran: `#!c %mpif77 -o prog prog.f`
    - 程序运行
        - `#!c %mpirun -np 4 prog`
    - 程序执行过程中不能动态改变进程的个数
    - 申请的进程数 np 与实际处理器个数无关

## MPI 基础知识

### 进程与消息传递

- 单个进程
- 单机内多个进程
- 包含于通过网络联接的不同处理器的多个进程
    - 进程独立存在，并位于不同的处理器
    - 进程间相互信息交换，可依靠消息传递
    - 最基本的消息传递操作包括发送消息 send、接受消息 receive、进程同步 barrier，规约 reduction 等

### MPI 重要概念

- 进程组（process group）：MPI 程序的全部进程集合的**一个有序子集**且进程组中每个进程被赋予一个在该组中唯一的序号（rank），用于在该组中标识该进程。
- 通信器（communicator）
    - 理解为一类进程的集合即一个进程组，且在该**进程组，进程间可以相互通信**
    - **任何MPI通信函数均必须在某个通信器内发生**
    - MPI 系统提供省缺的通信器 `MPI_COMM_WORLD`，所有启动的 MPI 进程通过调用函数 `MPI_Init()` 包含在该通信器内；各进程通过函数 `PI_Comm_size()` 获取通信器包含的(初始启动)的 `MPI` 进程个数
    - **组内通信器**和组间通信器
- 进程序号（rank）：用来在一个进程组或通信器中标识一个进程
    - **MPI 程序中的进程由进程组或通信器序号唯一确定**， 序号相对于进
    程组或通信器而言（假设 np 个处理器，标号 0...np-1）
    - **同一个进程在不同的进程组或通信器中可以有不同的序号**，进程的序
    号是在进程组或通信器被创建时赋予的
    - MPI 系统提供了一个特殊的进程序号 `MPI_PROC_NULL`，它代表空
    进程(不存在的进程)， 与 `MPI_PROC_NULL` 间的通信实际上没有任
    何作用
- 消息（message）
    - 分为 **数据（data）和包装（envelope）**两个部分
    - 包装由接受进程序号/发送进程序号、消息标号和通信器三部分组成；数据包含用户将要传递的内容
- MPI 对象：MPI 系统内部定义的数据结构，包括数据类型（如 `MPI_INT`）、通信器（`MPI_Comm`）、通信请求（`MPI_Request`）等，它们对用户不透明。
- MPI 联接器（handles）联接 MPI 对象的具体变量，用户可以通过它访问和参与相应MPI对象的具体操作。例如，MPI 系统内部提供的通信器 `MPI_COMM_WORLD`。

### MPI 函数的一般形式

```c
error = MPI_Xxxxx(parameters, ...);
MPI_Xxxxx(parameters, ...);
```

- 整形错误码由函数值返回
- 除 `MPI_Wtime()` 和 `MPI_Wtick()` 外，所有 MPI 的 C 函数均返回一个整型错误码。成功时返回 `MPI_SUCCESS`，其他错误代码依赖于执行

### MPI 程序基本结构

MPI include file -> 变量定义 -> MPI 环境初始化 -> 执行程序、进程间通信 -> 退出 MPI 环境

```c
#include <mpi.h>
void main(int argc, char *argv[]) {
    int np, rank, ierr;
    ierr = MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &np);
    /* Do Some Works */
    ierr = MPI_Finalize();
}
```

### MPI 基础函数

- **MPI_Init**：初始化 MPI 环境
- **MPI_Initialized**: 检查 MPI 环境是否已经初始化
- **MPI_Comm_size**：获取通信器中的进程数
- **MPI_Comm_rank**：获取通信器中当前进程的序号
- **MPI_Finalize**：结束 MPI 环境
- **MPI_Abort**：异常终止 MPI 程序
- **MPI_Get_processor_name**：获取当前进程所在处理器的名称
- **MPI_Wtime**：获取当前时间

### Hello World

```c
#include <mpi.h>
#include <stdio.h>
#include <math.h>
void main(int argc, char *argv[ ])
{
    int myid, numprocs, namelen;
    char processor_name[MPI_MAX_PROCESSOR_NAME];
    MPI_Init(&argc,&argv);
    MPI_Comm_rank(MPI_COMM_WORLD,&myid);
    MPI_Comm_size(MPI_COMM_WORLD,&numprocs);
    MPI_Get_processor_name(processor_name,&namelen);
    printf("Hello World! Process %d of %d on %s\n",myid, numprocs, processor_name);
    MPI_Finalize();
}
```

## 点对点通信

> **MPI 系统的通信方式都建立在点对点通信之上**

- 两个进程之间的通信
- 源进程发送消息到目标进程
- 目标进程接受消息
- 通信发生在同一个通信器内
- 进程通过其在通信器内的标号表示

<table>

</table>
| 通信类型 | 函数返回 | 对数据区操作 | 特性 |
| --- | --- | --- | --- |
| 阻塞式通信 | 1. 阻塞型函数需要等待制定操作完成返回 <br> 2. 或所涉及操作的数据要被 MPI 系统缓存安全备份后返回 | 函数返回后，对数据操作是安全的 | 1. 程序设计相对简单 <br> 2. 使用不当容易造成死锁 |
| 非阻塞式通信 | 1. 调用后立刻返回，实际操作在 MPI 后台执行 <br> 2. 需调用函数等待或查询操作的完成情况 | 函数返回后，即操作数据区不安全。可能与后台正进行的操作冲突 | 1. 可以实现计算与通信的重叠 <br> 2. 程序设计相对复杂 |

### 阻塞式点对点通信

#### MPI_Send

> 阻塞式消息发送

```c
int MPI_Send(
    void *buf,
    int count,
    MPI_Datatype datatype,
    int dest,
    int tag,
    MPI_Comm comm
)
```

- buf：发送缓冲区的起始地址
- count 不是字节数，而是指定数据类型的个数
- datatype 可是原始数据类型，或为用户自定义类型
- dest 是 发送目标的 rank
- tag 用来区分消息

#### MPI_Recv

> 阻塞式消息接收

```c
int MPI_Recv(
    void *buf,
    int count,
    MPI_Datatype datatype,
    int source,
    int tag,
    MPI_Comm comm,
    MPI_Status *status
)
```

- buf 是要将接收到的内容存入的 buffer 首地址（作为“输出”）
- count 是要接收的 buffer 元素个数
- datatype 是要接收的 buffer 中元素类型
- source 是接收来源的 rank（或者 MPI_ANY_SOURCE）
- tag 是 message tag（或者 MPI_ANY_TAG）
- comm 是 communicator
- status 是接收的状态结构体（作为“输出”）
    - 不需要时填写 MPI_STATUS_IGNORE
    - MPI_Status 中包含三个成员变量：MPI_SOURCE、MPI_TAG、MPI_ERROR
    - 可以通过 MPI_Get_count(MPI_Status status, MPI_Datatype datatype, int count) 函数来获取 count

#### MPI_Get_count

> 查询接收到的消息长度

```c
int MPI_Get_count(
    MPI_Status *status,
    MPI_Datatype datatype,
    int *count
)
```

- 该函数在 count 中返回数据类型的个数，即消息的长度
- count 属于 MPI_Status 结构的一个域，但不能被用户直接访问

#### MPI_Sendrecv

> 捆绑发送和接收

```c
int MPI_Sendrecv(
    void *sendbuf,
    int sendcount,
    MPI_Datatype sendtype,
    int dest,
    int sendtag,
    void *recvbuf,
    int recvcount,
    MPI_Datatype recvtype,
    int source,
    int recvtag,
    MPI_Comm comm,
    MPI_Status *status
)
```

#### MPI_Sendrecv_replace

> 捆绑发送和接收、收发使用同一缓存区

```c
int MPI_Sendrecv_replace(
    void *buf,
    int count,
    MPI_Datatype datatype,
    int dest,
    int sendtag,
    int source,
    int recvtag,
    MPI_Comm comm,
    MPI_Status *status
)
```

### 非阻塞式点对点通信

#### MPI_Isend

> 非阻塞式消息发送

```c
int MPI_Isend(
    void *buf,
    int count,
    MPI_Datatype datatype,
    int dest,
    int tag,
    MPI_Comm comm,
    MPI_Request *request
)
```

- MPI 系统会在后台完成消息发送
- 函数为该发送操作创建了一个请求，通过 request 变量返回
- request 可供之后（查询和等待）函数使用

#### MPI_Irecv

> 非阻塞式消息接收

```c
int MPI_Irecv(
    void *buf,
    int count,
    MPI_Datatype datatype,
    int source,
    int tag,
    MPI_Comm comm,
    MPI_Request *request
)
```

#### MPI_Wait

> 等待、检测一个通信请求的完成

```c
int MPI_Wait(
    MPI_Request *request,
    MPI_Status *status
)

int MPI_Test(
    MPI_Request *request,
    int *flag,
    MPI_Status *status
)
```

- MPI_Wait 阻塞等待通信函数完成后返回；MPI_Test 检测某通信，不论其是否完成，都立刻返回，如果通信完成，则 flag=true
- 当等待或检测的通信完成时，通信请求 request 被设置成 MPI_REQUEST_NULL
- 考察接收请求，status 返回与 MPI_Recv 一样；发送请求，则不确定
- MPI_Test 返回时，当 flag=false，status 不被赋值

#### MPI_Waitany

> 等待、检测一组通信请求中某一个的完成

```c
int MPI_Waitany(
    int count,
    MPI_Request array_of_requests[],
    int *index,
    MPI_Status *status
)
```

#### MPI_Waitall

> 等待、检测一组通信请求全部完成

```c
int MPI_Waitall(
    int count,
    MPI_Request array_of_requests[],
    MPI_Status array_of_statuses[]
)
```

#### MPI_Waitsome

> 等待、检测一组通信请求的部分完成

```c
int MPI_Waitsome(
    int incount,
    MPI_Request array_of_requests[],
    int *outcount,
    int array_of_indices[],
    MPI_Status array_of_statuses[]
)
```

#### MPI_Request_free

> 通信请求的释放（阻塞型）

```c
int MPI_Request_free(
    MPI_Request *request
)
```

#### MPI_Cancel

> 取消一个通信请求（非阻塞型）

```c
int MPI_Cancel(
    MPI_Request *request
)
```

#### MPI_Test_cancelled

> 检测一个通信请求是否被取消（非阻塞型）

```c
int MPI_Test_cancelled(
    MPI_Status *status,
    int *flag
)
```

#### MPI_Probe

> 消息探测（阻塞型）

```c
int MPI_Probe(
    int source,
    int tag,
    MPI_Comm comm,
    MPI_Status *status
)
```

#### MPI_Iprobe

> 消息探测（非阻塞型）

```c
int MPI_Iprobe(
    int source,
    int tag,
    MPI_Comm comm,
    int *flag,
    MPI_Status *status
)
```


## 集合通信
当需要进行进程之间一对多、多对一或多对多通信时（如划分任务、收集结果），使用多个 Send/Recv 不方便，可以使用集合通（Collective Communication）

### Barrier
```c 
int MPI_Barrier(MPI_Comm comm)
```
运行到此函数时进行等待，直到 communicator 中所有进程都运行到 Barrier 之后再一起继续运行

### 一对多
#### MPI_Bcast
```c 
int MPI_Bcast(
    void *buffer,
    int count,
    MPI_Datatype datatype,
    int root,
    MPI_Comm comm
)
```

- 比 MPI_Send 少了 dest，即将 buffer 从 root 发送到所有进程
    - 包含发送和接收（root 发送，其它接收，root 发送出 buffer，其它接收放到 buffer 中）
- MPI_Bcast 效率也比多个 Send/Recv 效率高（复用已经广播过的节点进行新的广播）

#### MPI_Scatter
```c 
int MPI_Scatter(
    const void *sendbuf,
    int sendcount,
    MPI_Datatype sendtype,
    void *recvbuf,
    int recvcount,
    MPI_Datatype recvtype,
    int root,
    MPI_Comm comm
)
```

与 Broadcast 不同的是，每个进程接收到的是 sendbuf 的一部分


### 多对一
#### MPI_Gather
```c 
int MPI_Gather(
    const void *sendbuf,
    int sendcount,
    MPI_Datatype sendtype,
    void *recvbuf,
    int recvcount,
    MPI_Datatype recvtype,
    int root,
    MPI_Comm comm
)
```

参数意义也都类似，将所有进程中的 sendbuf 发送给 root 进程，拼接到 recvbuf 中

#### MPI_Reduce
```c 
int MPI_Reduce(
    const void *sendbuf,
    void *recvbuf,
    int count,
    MPI_Datatype datatype,
    MPI_Op op,
    int root,
    MPI_Comm comm
)
```

类似 MPI_Gather，但将收集到的数据进行处理合并到 recvbuf 中

MPI_Op 可以是 MPI_MAX MPI_MIN MPI_SUM MPI_PROD MPI_LAND（逻辑与）MPI_BAND（位与）MPI_LOR MPI_BOR MPI_LXOR MPI_BXOR MPI_MAXLOC（最大值与位置）MPI_MINLOC

### 多对多
#### MPI_Allgather
```c 
int MPI_Allgather(
    const void *sendbuf,
    int sendcount,
    MPI_Datatype sendtype,
    void *recvbuf,
    int recvcount,
    MPI_Datatype recvtype,
    MPI_Comm comm
)
```

类似 MPI_Gather，但所有进程都会得到 MPI_Gather 中 root 得到的内容

#### MPI_Alltoall
```c 
int MPI_Alltoall(
    const void *sendbuf,
    int sendcount,
    MPI_Datatype sendtype,
    void *recvbuf,
    int recvcount,
    MPI_Datatype recvtype,
    MPI_Comm comm
)
```


## 持久通信


持久通信请求可用于以完全相同的方式（相同的通信器、收发缓冲区、数据类型与长度、源/目的地址和消息标签）重复收发的消息。目的是为了减少处理消息的开销及简化 MPI 程序


