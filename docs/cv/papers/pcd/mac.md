---
counter: true
comment: true
---

# GeoTransformer


> [!abstract]
> - paper：[:book: 3D Registration with Maximal Cliques](https://arxiv.org/abs/2305.10854)
> - code：[:material-github: 3D-Registration-with-Maximal-Cliques](https://github.com/zhangxy0517/3D-Registration-with-Maximal-Cliques)

## Introduction

- 点云配准现有的解决方案：
    - 几何方法：使用 RANSAC 等算法进行迭代采样，但在离群值率高时性能下降，并且计算复杂度较高。
    - 深度学习方法：基于深度学习的方法则专注于改进配准过程中的特定模块，如更具区分度的关键点特征描述符或更有效的对应选择技术。部分方法采用端到端的方式进行配准。然而，基于深度学习的方法通常需要大量的训练数据，并且在不同数据集上缺乏泛化能力。
- 本文的贡献：
    - **引入了一种 MAC 的假设生成方法。**相比下先前的最大团约束，MAC 能够在图中挖掘更多的局部信息。证明了即使在存在大量离群值的情况下，MAC 生成的假设也具有很高的准确性。
    - **基于 MAC，提出了一种新颖的 PCR 方法。**

## Method

为了对齐两个点云 $P_s$ 和 $P_t$，**首先使用几何或学习到的描述符提取它们的局部特征**。假设 $p^s$ 和 $p^t$ 分别表示点云 $P^s$ 和 $P^t$ 中的点。通过**匹配特征描述符，形成初始对应集合 $C_{initial}=\{C\}$**，其中 $c=(p^s, p^t)$。**MAC 从 $C_{initial}$ 中估计 $P^s$ 和 $P^t$ 之间的 6-DoF 位姿变换。**

<center><img src="https://cdn.jujimeizuo.cn/note/cv/pcd/MAC-1.jpg"></center>

### Graph Construction

**图空间能够更准确地描述对应关系之间的亲和性关系，优于欧式空间。**本文考虑两种构建兼容性图的方法。

#### First Order Graph

一阶图（FOG）是基于对应关系对 $(c_i, c_j)$ 之间的刚性距离约束来构建的，可以通过以下方式进行定量测量：

$$
S_{dist}(c_i, c_j) = \left | \| p_{i}^s - p_{j}^s \| - \| p_{i}^t - p_{j}^t \| \right |
$$

$c_i$ 和 $c_j$ 之间的兼容性分数可以表示为（其中 $d_{cmp}$ 是一个距离参数）：

$$
S_{cmp}(c_i, c_j) = \exp(-\frac{S_{dist}(c_i, c_j)^2}{2d_{cmp}^2})
$$

#### Second Order Graph

二阶图（SOG）是基于一阶图（FOG）演化而来的。权重矩阵 WSOG 计算如下：

$$
W_{SOG} = W_{FOG} \odot (W_{FOG}  \times W_{FOG})
$$

SOG 与 FOG 相比：

- SOG 具有更严格的边缘构造条件，与相邻节点的兼容性更高
- SOG 更稀疏，便于更快速的搜索团

### Search Maximal Cliques

#### Searching for Maximal Cliques

论文提出一种使用最大团生成假设的方法。与之前的最大团约束相比，论文方法放宽了约束并利用最大团挖掘更多的局部信息。通过使用 igraph 库中的最大团函数，论文方法可以高效地搜索最大团。这种方法能够更好地挖掘对应关系之间的亲和性，提高假设的生成效果。

#### Node-guided Clique Selection

在执行最大团搜索过程中，获得了最大团集合 $MAC_{initial}$。实际上，$MAC_{initial}$ 通常包含数万个最大团，如果考虑所有最大团，将会非常耗时。因此引入了一种节点引导的最大团选择方法来减少 $MAC_{initial}$ 的数量。首先为 $MAC_{initial}$ 中的每个最大团计算权重。给定一个最大团 $C_i=(V_i, E_i)$，其权重 $w_{C_i}$ 计算如下：

$$
w_{C_i} = \sum_{e_j \in E_i} w_{e_j}
$$

其中，$w_{e_j}$ 表示 WSOG 中的边 $e_j$ 的权重。一个节点可能被多个最大团包含，论文只保留了该节点具有最大权重的最大团，同时提出几种技术进一步筛选最大团：

- **Normal Consistency**

在最大团中，**论文通过比较对应关系之间的法线向量的角度差来检查它们的法线一致性。**如果角度差满足特定阈值条件，就认为这些对应关系是法线一致的。这种法线一致性检查可以帮助筛选出满足一致性要求的对应关系，并进一步优化的最大团选择过程：

$$
\left | \sin  \alpha_{ij}^s - \sin \alpha_{ij}^t \right | < t_{\alpha}
$$

- **Clique Ranking**

论文根据最大团的权重 $w_{C_i}$ 对 $MAC_{initial}$ 进行排序。排名靠前的最大团更有可能产生正确的假设。这种排序方式可以灵活地控制假设的数量，通过选择排名前 K 的最大团来控制假设的个数。

- **Htpothesis Generation and Evaluation**：从上一步中过滤出来的每个最大团代表一组一致的对应关系。通过将 SVD 算法应用于每个一致性集，可以得到一组 6 自由度的姿态假设。
    - **Instance-equal SVD**：对于对应关系的转换估计通常使用奇异值分解（SVD）实现 。**Instance-equal** 指的是所有对应关系的权重相等。
    - **Weighted SVD**：在最近的 PCR 方法中，常常通过为对应关系分配权重来进行处理。对应关系的权重可以通过求解兼容性图构建的兼容性矩阵的特征向量来得到。在这里将 $W_{SOG}$ 的主特征值作为对应关系的权重。

MAC 的最终目标是估计最优的 6 自由度刚体变换（由旋转姿态 $R^* \in SO(3)$ 和平移姿态 $t^* \in R^3$ 组成），该变换最大化以下目标函数：

$$
(R^*, t^*) = \argmax_{R, t} \sum_{i=1}^N s(c_i)
$$

其中，$c_i \in C_{initial}, N = |C_{initial}|, s(c_i)$ 表示 $c_i$ 的得分。论文考虑了集中 RANSAC 假设评估指标，包括均方误差（MAE）、均方根误差（MSE）和内点数。然后选择最佳假设进行 3D 配准。

## Experiment



## Reference



- [CVPR2023 最佳论文候选 | 使用最大团约束进行点云配准](https://blog.csdn.net/CVHub/article/details/131039318)