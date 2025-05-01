---
counter: true
comment: true
---

# InstantSplat

> [!abstract]
> - paper：[:book: InstantSplat: Sparse-view Gaussian Splatting in Seconds](https://arxiv.org/abs/2403.20309)
> - code：[:material-github: InstantSplat](https://github.com/NVlabs/InstantSplat)

## Introduction

> [!Question] 问题导向
> COLMAP + 3DGS Pipleline 存在的问题：
> 1. 3DGS 很大程度上依赖 COLMAP 导出的点和 Pose 的精度，并且 COLMAP 非常耗时
> 2. 对于场景的稀疏视角重建，如果输入的图片很少并且缺乏重叠，COLMAP 很难估计准确的相机参数
> 3. 3DGS 对于点云的密集处理依靠 Adaptive Density Control，其灵敏度很高，会针对每个场景进行调整（调整阈值、遮挡稀疏点云、添加相机参数噪声等等），并显著影响性能
> 4. COLMAP 和 3DGS 是没有关联，相互独立，所以误差会逐步累积

> [!Done] 解决方案
> - 1+2: 使用 DUSt3R 代替 COLMAP
> - 3: DUSt3R 得到的是一个密集且精确的点云，GS 训练过程无需做高斯球的 ADC
> - 4: 自监督联合优化相机位姿以及 GS 参数


## Method

<center><img src="https://cdn.jujimeizuo.cn/note/cv/slam/instant-splat-1.jpg"></center>

### GS 参数和相机位姿的自监督联合优化


通过最小化光度误差的梯度下降法，联合优化所有高斯参数和调整相机参数 ，允许模型 G 在目标观察位置 T 处的视角的置信度误差，梯度在 DUSt3R 框架中从置信度图回传到相机位姿:

$$
\mathbf{G}^{*},\mathbf{T}^{*}=\underset{\mathbf{G},\mathbf{T}}{\operatorname*{\operatorname*{\operatorname*{\operatorname*{\arg\min}}}}}\sum_{v\in N}\sum_{i=1}^{HW}\left\|\tilde{\mathbf{C}}_{v}^{i}-\mathbf{C}_{v}^{i}(\mathbf{G},\mathbf{T})\right\|
$$

## Experiments



## Reference

- [【论文笔记】稀疏视角40秒左右生成GS模型-InstantSplat
](https://blog.csdn.net/m0_74310646/article/details/141145147)
- [InstantSplat配置记录](https://blog.csdn.net/m0_74310646/article/details/140935837?depth_1-utm_source=distribute.pc_relevant.none-task-blog-2~default~BlogCommendFromBaidu~Ctr-2-140935837-blog-141145147.235%5Ev43%5Econtrol)
- [英伟达&厦大等开源InstantSplat！训练几秒钟，涨点62%！](https://blog.csdn.net/CV_Autobot/article/details/141160765?depth_1-utm_source=distribute.pc_relevant.none-task-blog-2~default~BlogCommendFromBaidu~Rate-4-141160765-blog-141145147.235%5Ev43%5Econtrol)