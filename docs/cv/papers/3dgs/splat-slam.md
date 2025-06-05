---
counter: true
comment: true
---

# Splat-SLAM

> [!abstract]
> - paper：[:book: Splat-SLAM: Globally Optimized RGB-only SLAM with 3D Gaussians](https://arxiv.org/abs/2405.16544)
> - code：[:material-github: Splat-SLAM](https://github.com/google-research/Splat-SLAM)

## Introduction

> [!Question] 问题导向
> 3DGS-SLAM 要么不采用全局优化，要么使用单目深度。

> [!Done] 解决方案
> 首个采用密集 3D 高斯地图表示的仅 RGB SLAM 系统，通过动态适应关键帧位姿和深度更新，主动使 3D 高斯地图变形，从而利用 globally optimized tracking 的所有优势。此外，用单目深度估计器细化不准确区域的深度更新，可进一步提高 3D 重建的准确性。
> <center><img src="https://cdn.jsdelivr.net/gh/jujimeizuo/note@gh-pages/assets/images/cv/slam/splat-slam-1.jpg"></center>


## Method

### Tracking

> [!Done] 目标
> 为了预测相机运动，使用一个预训练的循环光流模型 RAFT，并结合 Disparity、Scale 和 位姿优化（DSPO）层来联合优化相机位姿和逐像素视差。

- 优化通过 GN 在因子图上进行，V 存储 keyframe 的 pose 和 disp，E 存储 keyframe 之间的 optical flow，通过计算到最后天机的 keyframe's optical flow，将里程计 keyframe edges 添加到图 G 中，如果 average optical flow > $\tau$l，则将新的 keyframe 添加到 G 中；local BA、loop closure、global BA 优化的是相同目标，但基于不同结构的因子图；
- DSPO 层由两个交替优化的目标组成：DBA + 引入 mono depth；
    - DBA：联合优化 keyframe 的 pose 和 disp，在当前帧的 sliding window 内定义的 local graph 上进行优化；
    - 引入 mono depth $D^{mono}$ 作为额外的数据项，$D^{mono}$ 由预训练的相对深度 DPT model [12] 预测；
- 计算 keyframe i 和 j 之间的像素对应关系，如果 (u, v) 分别对应的 $p_i$ 和 $p_j$ 之间的 L2 距离小于阈值，则估计的 $D_i(u, v)$ 在 i 和 j 之间是一致的。固定 i，遍历除 i 外的所有 keyframe 计算一致性，数量大于阈值则 $D_i(u, v)$ 有效；
- **Loop Closure**：通过计算 curr activate keyframe 与 all prev keyframe 的 average optical flow 实现。对于每对 keyframe，实现两个目标：
    1. 光流必须低于 thre，确保视图之间有足够的共视性；
    2. 帧之间的时间间隔必须超过 thre，防止在图中引入冗余边；
- **Global BA**：构建一个单独的图，包含截止到当前的 all keyframe；
    - 引入 [79]，根据 keyframe 之间的时间和空间关系引入边；
    - 引入 [75]，every 20 keyframe 执行一次 global BA；
    - 为了保持数值的稳定性，每次 global BA 之前，对 disp 和 pose 的尺度进行归一化；

### Deformable 3D Gaussians Scene Representation

- 该表示法在 DSPO 或 Loop Closure 下进行变形以实现全局一致性。
- **Map Initialization**：采用 MonoGS 的 RGBD 策略，将新的高斯添加到未探索的 scene 中，由于没有深度传感器，通过结合内点多视图深度和 mono depth 构建 proxy depth map D；
- **Keyframe Selection and optimization**：引入 MonoGS 的高斯共视性；
- **Map Deformation**：由于 tracking 是全局一致的，keyframe 的 pose 和 proxy depth map 的变化需要通过 non-rigid deform 3D 高斯地图；尽管高斯 means 是直接优化的，但随着优化后的 pose 和 proxy depth map 被提供，可以让优化器对地图进行 deform；作者发现，主动对 3D 高斯地图进行变形有助于渲染，在映射之前，将 deformation 应用于所有接收到更新 pose 和 depth 的高斯上；

## Experiments

## Reference

- [12] Omnidata: A scalable pipeline for making multi-task mid-level vision datasets from 3d scans.
- [75] Glorie-slam: Globally optimized rgb-only implicit encoding point cloud slam.
- [79] Go-slam: Global optimization for consistent 3d instant reconstruction.