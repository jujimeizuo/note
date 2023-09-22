---
counter: true
comment: true
---

# 概论

## 什么是超算

> 超级计算机，是指能够执行一般个人电脑无法处理的高速运算的计算机，规格与性能比个人计算机强大许多。
> <div style="text-align: right">———— 维基百科</div>


## 开发工具

### SIMD: AVX/SSE

> 高级向量扩展指令集（AVX）是 x86 架构微处理器中的指令集。
> <div style="text-align: right">———— 维基百科</div>

单指令多数据流（Single Instruction Multiple Data），在硬件层面上提供了通过一条指令运行多个运算的方法

在 x86 架构下，SIMD 一半和 SSE 和 AVX 等指令集联系在一起，SSE 和 AVX 指令集中提供了大量可以单指令操作多个数据单元的指令

下面是 SISD 和 SIMD 的比较

!!! note "SISD"
    ```C++
    vectorAdd(float* a, float* b, float* c) {
        for (int i = 0; i < 8; i++) {
            c[i] = a[i] + b[i];
        }
    }
    ```

!!! note "SIMD"
    通过一条 CPU 指令，并行执行 8 个 float 的加
    ```C++
    __m256 vectorAdd(__m256 a, __m256 b, __m256 c) {
        return _mm256_add_ps(a, b);
    }
    ```

### SIMT: CUDA/ROCM/OPENCL

<center><img src="https://cdn.jujimeizuo.cn/note/cs/hpc/simt.jpg"></center>

> CUDA（Compute Unified Device Architecture, 统一计算架构）是由英伟达 NVIDIA 所推出的一种集成技术，是该公司对于 GPU 的正式名称。
> ROCm 是 Advanced Micro Devices（AMD）的软件栈，用于图形处理单元 GPGPU 编程。
> OpenCL（Open Computing Language，开放计算语言）是一个为异构平台编写程序的框架，此异构平台可由 CPU、GPU、DSP、FPGA 或其它类型的处理器与硬体加速器所组成。
> <div style="text-align: right">———— 维基百科</div>

!!! note "CUDA"
```C++
__global__ void vectorAdd(float* a, float* b, float* c) {
    int tid = blockIdx.x;
    if (tid < 8)
        c[tid] = a[tid] + b[tid];
}
```

!!! note "OpenCL"
```C++
_kernel void vectorAdd(global const float* a, global const float* b, global const float* c) {
    int gid = get_global_id(0);
    if (gid < 8)
        c[gid] = a[gid] + b[gid];
}
```

###  MULTI-THREAD: OPENMP

> OpenMP 是一套支持跨平台共享内存方式的多线程并发的编程 API。
> <div style="text-align: right">———— 维基百科</div>

为了利用多线程，我们可以使用一些更低层的库进行开发（Linux 下的 pthread），OpenMP 提供了一种更统一且简洁且跨平台的方式进行开发。

!!! note "OpenMP"
    ```C++
    vectorAdd(float* a, float* b, float* c) {
        #pragma omp for
        for (int i = 0; i < 8; i++) {
            c[i] = a[i] + b[i];
        }
    }
    ```

## 性能调优

### CPU

- CPU 通过将数据缓存到 L1/L2/L3
- Cache 中避免对内存的频繁访问造成的低效
- 优化方法
    - 循环展开
    - 内存预取
    - ...

<center><img src="https://cdn.jujimeizuo.cn/note/cs/hpc/l1-l2-l3.jpg"></center>

- CPU 本身是一个流水线结构，执行每一条指令分为多个阶段，流水线地执行。
- 在出现分支的地方可能导致流水线无法正常被填充
- 优化方法
    - 分支预测

### GPU

- CUDA 开发中的问题
    - 线程束分化
    - 理解 GPU 内存模型
    - 并发
    - ...


<center><img src="https://cdn.jujimeizuo.cn/note/cs/hpc/gpu-model.jpg"></center>

### RDMA

在数据中心领域，远程直接内存访问。适合大规模并行计算机集群。