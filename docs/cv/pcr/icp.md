---
counter: true
comment: true
---

# ICP

!!! abstract
    ICP（Iterative Closest Point）是一种迭代算法，用于将两组点云进行配准，即找到两组点云之间的最优刚体变换（旋转矩阵和平移向量），使得两组点云之间的误差最小化。


## 问题描述

点云配准（Point Cloud Registration）指的是输入两幅点云 $P_s$（source）和 $P_t$（target），输出一个变换 $T$ 使得 $T(P_s)$ 和 $P_t$ 的重合程度尽可能高。变换 $T$ 可以是刚性的(rigid)，也可以不是，本文只考虑刚性变换，即变换只包括旋转、平移。

目前应用最广泛的点云精配准算法是迭代最近点算法（Iterative Closest Point, ICP）及各种变种 ICP 算法。

## 算法描述

对于 $T$ 是刚性变换的情形，点云配准问题可以描述为：

$$
R^\ast, t^\ast = \argmin_{R, t} \frac{1}{|P_s|} \sum_{i=1}^{|P_s|} \| p_t^i - (R \cdot p_s^i + t) \|^2
$$

这里$p_s$ 和 $p_t$ 是源点云和目标点云一一对应点。 

- ICP 算法的直观想法：
    - 如果我们知道两幅点云上点的对应关系，那么可以用 Least Squares 来求解 R，t 参数。
    - 怎么知道点的对应关系呢？如果我们知道了一个大概靠谱的 R，t 参数，那么可以通过贪心的方式找两幅点云上的点的对应关系（直接找距离最近的点作为对应点）。
- ICP 算法实际上就是交替进行上述两个步骤，迭代进行计算，直到收敛。

??? note "ICP 算法流程"
    1. 点云预处理：滤波、清理数据等
    2. 匹配：应用上一步求解出的变换，找最近点
    3. 加权：调整一些对应点对的权重
    4. 提出不合理的对应点对
    5. 计算 loss
    6. 最小化 loss，求解当前最优变换
    7. 回到 2，进行迭代，直到收敛

- 整体上来看，ICP 把点云配准问题拆分成两个子问题：
    - 找最近点
    - 找最优变换

### 找最近对应点

利用初始 $R_0、t_0$ 或上一次迭代得到的 $R_{k-1}、t_{k-1}$ 对初始点云进行变换，得到一个临时的变换点云，然后用这个点云和目标点云比较，找出源点云中每一个点在目标点云中的最近邻点。

如果直接进行比较最近邻点，需要进行两重循环，计算复杂度为 $\mathcal{O}(|P_s| \cdot |P_t|)$，这一步比较耗时，常见的加速方法有：

- 设置距离阈值，当点与点距离小于一定阈值就认为找到了对应点，不用遍历完整个点集。
- 使用 ANN 加速查找，常见的有 KD-tree。KD-tree 建树复杂度为 $\mathcal{O}(N \log N)$，查找复杂度为 $\mathcal{O}(\log N)$（最坏情况下为 $\mathcal{O}(N)$）。

### 求解最优变换

对于 point-to-point ICP 问题，求最优变换是有闭形式解（closed-form solution）的，可以借助 SVD 分解来计算。

结论：在已知点的对应关系的情况下，设 $\overline{p}_s, \overline{p}_t$ 分别表示源点云和目标点云的质心，令 $\hat{p}_s^i=p_s^i-\overline{p}_s，\hat{p}_t^i=p_t^i-\overline{p}_t$，令 $H=\sum_{i=1}^{|P_s|}\hat{p}_s^i \hat{p}_t^{i^\top}$，这是一个 $3 \times 3$ 的句子，对 H 进行 SVD 分解得到 $H=U\Sigma V^\top$，则 point-to-point ICP 问题最优旋转为：

$$R^{\ast} = V U^\top$$

最优平移为：

$$t^{\ast} = \overline{p}_t - R^\ast \hat{p}_s$$

#### 计算最优平移

令 $N=|P_s|$，设 $F(t)=\sum_{i=1}^N \|(R \cdot p_s^i + t) - p_t^i \|^2$，对其进行求导，则有：

$$
\begin{aligned} \frac{\partial F}{\partial t} &= \sum_{i=1}^{N} 2 (R \cdot p_s^i + t - p_t^i) \\ &= 2nt + 2R\sum_{i=1}^{N}p_s^i - 2\sum_{i=1}^{N}p_t^i \end{aligned}
$$

令导数为 0，则有：

$$
\begin{aligned} t &= \frac{1}{N} \sum_{i=1}^{N} p_t^i - R \frac{1}{N} \sum_{i=1}^{N} p_s^i \\ &= \bar p_t - R \bar p_s \end{aligned}
$$

无论 R 取值如何，根据上式都可以求得最优的 t，使得 loss 最小。


#### 计算最优旋转

经过最优平移的推导，知道无论旋转如何取值，都可以通过计算点云的质心来得到最优平移，为了计算方便，不妨不考虑平移的影响，先将源点云和目标点云都转换到质心坐标下，这也就是令 $\hat{p}_s^i=p_s^i-\hat{p}_s, \hat{p}_t^i=p_t^i-\hat{p}_t$ 的意义。

下面用 $\hat{p}_s^i$ 和 $\hat{p}_t^i$ 进行推导。不考虑平移，则 loss 可以写成：

$$
F(R) = \sum_{i=1}^{N} \|R \cdot \hat p_s^i - \hat p_t^i \|^2
$$

先简化 $\|R \cdot \hat p_s^i - \hat p_t^i \|^2$：

$$
\begin{aligned} \|R \cdot \hat p_s^i - \hat p_t^i\|^2 &= (R \cdot \hat p_s^i - \hat p_t^i)^\top(R \cdot \hat p_s^i - \hat p_t^i) \\ &= ({\hat p_s^i}^\top R^\top - {\hat p_t^i}^\top)(R \cdot \hat p_s^i - \hat p_t^i) \\ &= {\hat p_s^i}^\top R^\top R {\hat p_s^i} - {\hat p_t^i}^\top R {\hat p_s^i} - {\hat p_s^i}^\top R^\top {\hat p_t^i} + {\hat p_t^i}^\top {\hat p_t^i} \\ &= \|{\hat p_s^i}\|^2 + \|{\hat p_t^i}\|^2 - {\hat p_t^i}^\top R {\hat p_s^i} - {\hat p_s^i}^\top R^\top {\hat p_t^i} \\ &= \|{\hat p_s^i}\|^2 + \|{\hat p_t^i}\|^2 - 2{\hat p_t^i}^\top R {\hat p_s^i} \end{aligned}
$$

这里利用 $R^\top R=I$ 和 ${\hat p_t^i}^\top R {\hat p_s^i} = {\hat p_s^i}^\top R^\top {\hat p_t^i}$（标量的转置等于自身）的性质。

由于点的坐标是确定的（和 R 无关），所以最小化原 loss 等价于求：

$$
R^{\ast} = \argmin_R (-2 \sum_{i=1}^{N} {\hat p_t^i}^\top R {\hat p_s^i})
$$

也即为求：

$$
R^{\ast} = \argmax_R (\sum_{i=1}^{N} {\hat p_t^i}^\top R {\hat p_s^i})
$$

注意到 $\sum_{i=1}^{N} {\hat p_t^i}^\top R {\hat p_s^i} = trace(P_t^\top R P_s)$（由矩阵乘法及 trace 的定义可得），所以问题转化为：

$$
R^{\ast} = \argmax_{R} \ trace(P_t^\top R P_s)
$$

根据 trace 的性质 $trace(AB)=trace(BA)$，（这里不要求 A 和 B 是方阵，只要 A*B 是方阵即可），有：

$$trace(P_t^\top RP_s)=trace(RP_sP_t^\top)$$

在利用前面定义的矩阵 H 和其 SVD 分解，带入上式得到：

$$
\begin{aligned} trace(P_t^\top R P_s) &= trace(R P_s P_t^\top) \\ &= trace(R H) \\ &= trace(R U \Sigma V^\top) \\ &= trace(\Sigma V^\top R U) \end{aligned}
$$

注意这里的 $V,U,R$ 都是正交矩阵，所以 $V^\top RU$ 也是正交矩阵。

令 $M=V^\top RU=\begin{bmatrix} m_{11} & m_{12} & m_{13} \\ m_{21} & m_{22} & m_{23} \\ m_{31} & m_{32} & m_{33} \end{bmatrix}$，则有：

$$
\begin{aligned} trace(\Sigma V^\top R U) &= trace(\Sigma M) \\ & = \sigma_1 m_{11} + \sigma_2 m_{22} + \sigma_1 m_{33} \end{aligned}
$$

根据奇异值非负的性质和正交矩阵的性质（正交矩阵中的元素绝对值不大于 1），容易证得只有当 $M$ 为单位阵时 $trace(\Sigma M)$ 最大，即：

$$
V^\top RU = I \\
R = VU^\top
$$

所以有 $R^\ast = VU^\top$。

最后还需要进行 Orientation rectification，即验证 $R^\ast = VU^\top$ 是不是一个旋转矩阵（检查是否有 $|R|=1$），因为存在 $|R|=-1$ 的可能，此时 $R$ 表示的不是旋转而是一个 reflection，所以还要给上述优化求解加上一个 $|R|=1$ 的约束。

根据矩阵行列式的性质，以及 $U,V$ 都是正交矩阵：

$$
\begin{aligned} |M| &= |V^\top| |U| |R| \\ &= |V^\top| |U| = \pm 1 \end{aligned}
$$

如果 $|VU^\top|=1$，则 $|M|=1，R^\ast = VU^\top$ 已经给出最优旋转；如果 $|VU^\top|=-1$，则 $|M|=-1$，我们需要求解此时的 $R$，也就是分析 $M$ 应该具有何种形式。具体的讨论参考[原论文](https://www.math.pku.edu.cn/teachers/yaoy/Fall2011/arun.pdf)，这里给出结论：当 $|M|=-1$ 时，使得 $trace(\Sigma M)$ 最大的 $M$ 为：

$$M = \left[ \begin{array}{cccc} 1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & -1 \end{array} \right]$$

综合考虑 $|M|=1$ 和 $|M|=-1$ 两种情况，我们可以得到：

$$
R^{\ast} = V \left[ \begin{array}{cccc} 1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & |V U^\top| \end{array} \right] U^\top
$$

到此公式推导完全，简单总结一下求解最优变换的步骤：

1. 计算源点云和目标点云的质心；
2. 将源点云和目标点云都转换到质心坐标系；
3. 计算矩阵 H（形式类似“协方差矩阵”）；
4. 对 H 进行 SVD 分解，根据公式求得 $R^\ast$；
5. 根据公式计算 $t^\ast$；

### 迭代

每一次迭代都会得到当前的最优变换参数 $R_k,t_k$，然后将该变换作用于当前源点云；“找最近对应点”和“求解最优变换”这两步不停迭代进行，直到满足迭代终止条件，常用的终止条件有：

- $R_k,t_k$ 的变化量小于一定值
- loss 变化量小于一定值
- 达到最大迭代次数

## ICP 的优缺点及一些改进算法

- ICP 优点
    - 简单，不必对点云进行分割和特征提取
    - 初值较好情况下，精度和收敛性都不错
- ICP 缺点
    - 找最近对应点的计算开销较大
    - 只考虑了点与点距离，缺少对点云结构信息的利用

原始的 ICP 算法计算开销大，对初始变换敏感，容易陷入局部最优解。自 ICP 提出以来，有相当多的 ICP 改进算法，简要列举一些：

- Point-to-Plane ICP，原始 ICP 算法的代价函数中使用的 point-to-point 距离，point-to-plane 则是考虑源顶点到目标顶点所在面的距离，比起直接计算点到点距离，考虑了点云的局部结构，精度更高，不容易陷入局部最优；但要注意 point-to-plane 的优化是一个非线性问题，速度比较慢，一般使用其线性化近似；
- Plane-to-Plane ICP，point-to-plane 只考虑目标点云局部结构， plane-to-plane 顾名思义就是也考虑源点云的局部结构，计算面到面的距离；
- Generalized ICP (GICP)，综合考虑 point-to-point、point-to-plane 和 plane-to-plane 策略，精度、鲁棒性都有所提高；
- Normal Iterative Closest Point (NICP)，考虑法向量和局部曲率，更进一步利用了点云的局部结构信息，其论文中实验结果比 GICP 的性能更好。

## 实际使用中的一些注意事项

- ICP 比较依赖于变换初值，平移比较简单，直接用点云质心来估计；旋转初值的话可以手动调一个粗略值，或者沿每个轴的旋转进行采样、组合来尝试（不适合实时性应用）；
- 点太多的话可以先降采样；
- 找到一些 anchor 点对（比如先用特征点匹配），可以帮助加速收敛；
- 对应用场景引入一些合理假设，比如限制旋转、平移的范围，变换自由度数量等。


## Reference

- [点云配准学习笔记-ICP（1）](https://zhuanlan.zhihu.com/p/137441104)
- [三维点云配准 -- ICP 算法](https://yilingui.xyz/2019/11/20/191120_point_cloud_registration_icp/)
- [https://igl.ethz.ch/projects/ARAP/svd_rot.pdf](https://igl.ethz.ch/projects/ARAP/svd_rot.pdf)
- [https://courses.cs.duke.edu//spring07/cps296.2/scribe_notes/lecture24.pdf](https://courses.cs.duke.edu//spring07/cps296.2/scribe_notes/lecture24.pdf)