---
counter: true
comment: true
---

# LoopSplat

> [!abstract]
> - paper：[:book: LoopSplat: Loop Closure by Registering 3D Gaussian Splats](https://arxiv.org/abs/2408.10154)
> - code：[:material-github: LoopSplat](https://github.com/GradientSpaces/LoopSplat)

## Introduction

> [!Question] 问题导向
> 3DGS 未能通过 loop closure / global BA 解决场景**全局一致性**问题。

> [!Done] 解决方案
> LoopSplat 以 RGB-D 作为输入，利用 3DGS 子地图和帧到模型跟踪进行 dense mapping。
> - LoopSplat 在线触发 loop closure，并通过 3DGS 配准直接计算子地图之间的相对回环边约束，与传统的全局到局部点云配准相比，提高了效率和准确性。
> - 采用一种鲁棒的位姿图优化公式，并对各子地图进行刚性对齐以实现全局一致性。
> <center><img src="https://cdn.jsdelivr.net/gh/jujimeizuo/note@gh-pages/assets/images/cv/slam/loop-splat-1.jpg"></center>


## Method

### GS SLAM

- **Submap Initialization**：每个子地图对观察特定区域的一系列 keyframe 进行建模。随着场景扩大，会初始化新的 submap，与使用固定数量 keyframe 的方法不同，当当前帧相对于第一个 keyframe 的相对位移和旋转超过 thre，会触发新的 submap initialization；
- **Frame-to-model Tracking**：基于恒定运动假设初始化位姿，通过最小化 tracking loss 优化位姿；
- **Submap Expansion**：submap 按固定时间选择 keyframe。点当前 keyframe 被定位，主要在覆盖稀疏的区域扩展 3D Gaussian map。从 RGB-D 中计算带 pose 的 dense pc，然后从累积透明度值低于 thre 或出现显著深度差异的区域中均匀采样 $M_k$ 个点。只有当 radius 内不存在现有的 3D Gaussian mean 时，才将新的 3D Gaussian splats 添加到当前子地图中；
- **Submap Update**：添加新的高斯后，当前 submap 中的所有高斯通过最小化 render loss 进行固定次数的迭代优化，由 submap 上的所有 keyframe 计算得出；

### Registration of Gaussian Splats

- **Overlap Estimation**：作者发现，通过匹配局部特征直接估计高斯重叠区域效果不好，相反，从每个 submap 中识别出具有相似视觉内容的视点。首先将所有 keyframe 通过 NetVLAD [2] 提取它们的全局描述符，然后计算两组 keyframe 之间的 cosine similarity，并保留前 k 对进行配准；
- **Registration as Keyframe Localization**
    - 3DGS submap 以及视点可被视为一个刚体，所以作者将 3DGS 配准视为关键帧定位问题；
    - 固定地图参数，最小化 render loss 优化刚体变换；
    - 并行估计选定视点的刚体变换，通过从估计的重叠区域中采样前 k 个视点作为选定视点，在不重叠视点处不会出现冗余；
    - 首先估计视点变换，然后用于计算 submap 的全局变换；
- **Multi-view Pose Refinement**：由于渲染残差表明变换后的视点与原始观测的拟合程度，将残差的倒数作为每个估计值的权重，并应用加权旋转平均来计算全局旋转；

    $$
    \bar{\mathbf{R}}=\arg\min_{\mathbf{R}\in SO3}\sum_{i=1}^k\frac{1}{\varepsilon_i}\|\mathbf{R}-\mathbf{R}_i\|_F^2+\sum_{i=k+1}^{2k}\frac{1}{\varepsilon_i}\|\mathbf{R}-\mathbf{R}_i^{-1}\|_F^2
    $$


### Loop Closure with 3DGS

- 当创建新的 submap 时会触发 loop closure，构建包含所有历史 submap 的位姿图，然后用 3DGS 配准计算位姿图的回环边约束，最后执行位姿图优化；
- **Loop Closure Detection**
    - 为了检测系统是否访问过同一地点，首先使用预训练的 NetVLAD [2] 提取全局描述符；
    - 计算第 i 个 submap 的 all keyframe 的 cosine similarity，确定对于第 p 个百分位数的自相似性分数 $s_{self}^i$；
    - 然后应用相同的方法计算第 i 和 第 j 个 submap 之间的交叉相似性 $s_{cross}^{i,j}$；
    - 如果 $s_{cross}^{i,j} > \min{s_{self}^i, s_{self}^j}$，则添加一个新的 loop；
    - 然后仅依靠视觉相似性进行 loop closure，可能会产生错误的闭环边，因此还评估两个 submap 的高斯之间的初始几何重叠率，保留 $r>0.2$ 的 loop；
- **Pose Graph Optimization**：当检测到新的 loop，都会创建一个新的位姿图进行优化位姿矫正；
- **Globally Consistent Map Adjustment**：从位姿图优化输出的位姿矫正，对于每个子 submap，更新相机 pose、Gaussian mean说 和 convariances

## Experiments


## Reference

- [2] Netvlad: Cnn architecture for weakly supervised place recognition.