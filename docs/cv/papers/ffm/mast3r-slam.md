---
counter: true
comment: true
---

# MASt3R-SLAM

> [!abstract]
> - paper：[:book: MASt3R-SLAM: Real-Time Dense SLAM with 3D Reconstruction Priors](https://arxiv.org/abs/2412.12392)
> - code：[:material-github: MASt3R-SLAM](https://github.com/rmurai0610/MASt3R-SLAM)
> - video: [:clapper: MASt3R-SLAM](https://youtu.be/wozt71NBFTQ)

## Introduction

> [!Question] 问题导向
> SLAM 并未成为一种即插即用的算法，因为需要硬件专业知识和校准，即使不配备 IMU 或其他额外传感器设备的最简单摄像头参数，也不存在一种能在实际场景中同时提供精确位姿和稠密地图的 SLAM 方案。

> [!Done] 解决方案
> 提出一个即插即用的单目 SLAM 系统，除了假设相机中心，不假设其他（固定或相机参数模型等等），能获取全局统一的 pose 和密集的几何形状。(15 FPS)
> <center><img src="/assets/images/cv/slam/mast3r-slam-2.jpg"></center>

## Method

### Pointmap Matching

- 解决 MASt3R 输出的点图和特征基础上，寻找两幅图像间像素匹配集合的问题。
- 暴力匹配、kd-tree，包括 MASt3R 提出的方案，在密集像素匹配的运行时间都在秒级，所以 MASt3R-SLAM 不专注于全局匹配搜索的有效方法，而是**基于迭代投影的匹配方法**。
- **基于投影的匹配方法**：基于 MASt3R 输出的点图 $X_i^i, X_i^j$，通过迭代优化参考帧中的像素坐标 $p$，使 $X_i^i$ 投影的 3D 点 $x$ 与 $[X_i^i]_p$ 对应的光线误差最小化：$\mathbf{p}^*=\arg\min_\mathbf{p}\left\|\psi\left([\mathbf{X}_i^i]_\mathbf{p}\right)-\psi\left(\mathbf{x}\right)\right\|^2$
- 该过程对每个点单独进行，10 次迭代内收敛。没有投影坐标 $p$ 的初始化时，所有像素初始化为单位映射，跟踪时利用上一帧的匹配结果作为初始化，加快收敛。
- 为处理遮挡和异常值，会剔除 3D 空间中距离过大的匹配。
- **基于特征的匹配优化**：利用几何信息得到的像素匹配只是初始估计，通过在局部 patch 窗口内更新像素位置，使其达到最大特征相似度，进行基于图像的**coarse-to-fine search**。
- CUDA 加速。

### Tracking and Pointmap Fusion

- 需要估计当前帧 $I_f$ 和上一帧 $I_k$ 的相对变换 $T_{kf}$，并且只使用网络的单词前向传播来估计变换。
- 由于 Pointmap 预测中深度不一致的问题，导致跟踪误差会降低 KeyFrame Pointmap 的质量，影响后端处理，所以将最终的预测 fusion 成一个单一的 Pointmap（平均所有预测），会降低误差。
- **基于光线误差的跟踪优化**：**利用在中心相机假设下 Pointmap 预测可转化为光线的特性**，计算方向射线误差。同时防止系统在纯旋转情况下退化，添加一个相机中心距离差异的小权重误差项，如下图所示。

<center><img src="/assets/images/cv/slam/mast3r-slam-1.jpg"></center>

- **Pointmap Fusion 策略**：系统不仅对几何估计进行滤波，还对光线定义的相机模型进行滤波，求解相对变换 $T_{kf}$ 后通过滑动加权平均滤波器更新 Pointmap。利用滤波融合所有帧的信息，无需在后端对所有相机位姿进行优化。

### Graph Construction and Loop Closure

- **关键帧添加与图构建**：当前帧与关键帧之间的有效匹配数量或唯一关键帧像素数量低于阈值，会降当前帧添加为新的关键帧，并且在图中添加一条从新关键帧到上一关键帧的双向边到 list 中，这样系统能够按时间顺序对估计的位姿进行约束。
- **回环检测机制**：借鉴 MASt3R-SfM 中的**聚合选择性匹配核 ASMK** 进行图像检索，来检测回环。
- **数据库更新**：完成回环检测和添加新的回环边后，将新关键帧的编码特征添加到倒排索引中。

### Backend Optimisation

- 实现所有关键帧位姿和场景几何的全局一致性。
- 系统引入高效的**二阶优化方案，固定前 7 自由度的 Sim(3) 位姿来处理尺度和位姿的不确定性**。

### Relocalisation

- 在系统运行时，如果场景出现特征变化、遮挡等因素导致匹配数不足，系统会进行重定位。
- pipeline：检索数据库以更严格的阈值查询。一旦检索到的图像与当前帧有足够数量的匹配，然后将其作为一个新关键帧添加到图中，并恢复 track。

## Experiments

## Reference

- [论文阅读笔记之《MASt3R-SLAM: Real-Time Dense SLAM with 3D Reconstruction Priors》](https://kwanwaipang.github.io/File/Blogs/Poster/MASt3R-SLAM.html#dust3r:-geometric-3d-vision-made-easy)
- [实验笔记之——MASt3R-SLAM](https://kwanwaipang.github.io/MASt3R-SLAM/)
- [实验笔记之——动态场景下MASt3R及MASt3R-SLAM的测试](https://kwanwaipang.github.io/Dynamic-MASt3R/)
- [SLAM-3DGS算法研究之路：MASt3R-SLAM论文深入研读](https://zhuanlan.zhihu.com/p/17982445115)
- [杀疯了！帝国理工开源MASt3R-SLAM：实时、鲁棒、全局一致的稠密SLAM](https://zhuanlan.zhihu.com/p/14345405887)
- [MASt3R-SLAM_comment](https://github.com/KwanWaiPang/MASt3R-SLAM_comment)
