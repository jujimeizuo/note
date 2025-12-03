---
counter: true
comment: true
---

# Deform3DGS

> [!abstract]
> - paper：[:book: Deform3DGS: Flexible Deformation for Fast Surgical Scene Reconstruction with Gaussian Splatting](https://arxiv.org/abs/2405.17835)
> - code：[:material-github: Deform3DGS](https://github.com/jinlab-imvr/Deform3DGS)

## Introduction

> [!Question] 问题导向
> 现有方法虽能达到较高的重建质量，但存在渲染速度慢、训练时间长的问题。

> [!Done] 解决方案
> 1. 整合点云初始化将 3DGS 引入手术场景；
> 2. 提出灵活形变建模方案（FDM），用于单个高斯层面学习组织形变动态，能通过高效的表示方式对表面形变进行建模，从而实现实时渲染性能。
> <center><img src="/assets/images/cv/slam/deform3dgs-1.jpg"></center>


## Method

### Flexible Deformation Modeling (FDM)

> [!Question] 
> 1. Hexplane 表示的隐式形变场在训练时会产生显著的计算开销，无法满足手术视频的实时处理需求；
> 尽管每个高斯都能通过权重调整来适应形变，但时间形变被局限于规范运动，导致不同查询时间的形变表示不一致。为了确保整体轨迹的连贯性，模型可能不得不放弃某些特定运动，这在存在复杂精细形变的场景（如器械与组织的交互）中是不利的；
> 在特定时间戳学习到的形变会全局影响整个轨迹，导致在不同查询时间的局部形变表示欠佳。

- 利用可学习参数为基函数提供灵活性和适应性，采用具有可学习性中心 $\theta$ 和方差 $\sigma$ 的高斯函数；

$$
\tilde{b}(t ; \theta, \sigma)=\exp \left(-\frac{1}{2 \sigma^{2}}(t-\theta)^{2}\right)
$$

- 对于点云中的每个高斯分布、位置和旋转自然与组织运动相关，而尺度会不断变化，因为在器械介入过程中，组织容易发生弹性形变：
    - 为每个高斯分布引入一组额外的可学习参数，分别描述其位置、旋转和尺度的时间形变；

$$
\psi^{\mu,x}(t;\boldsymbol{\Theta}^{\mu,x})=\sum_{j=1}^B\omega_j^{\mu,x}\tilde{b}(t;\theta_j^{\mu,x},\sigma_j^{\mu,x})
$$

### Point Cloud Initialization

- 在形变建模之前引入高斯点云初始化：
    - 利用相机模型和内参矩阵提取每一帧的三维组织点云 $P_i = K^{-1}D_i(I_i \odot M_i)$；选择第一针来初始化高斯点云作为标准状态；
- 由于存在工具遮挡，导致初始化点云上出现空洞和局部稀疏的情况，这种分布不均匀的初始化会耗费更多时间来 densify 点云，并导致效率欠佳：
    - 基于密集的高斯点分布有助于手术场景中剧烈变形区域进行重建这一假设，开发了一种运动感知点融合（MAPF），用于选择性地表现出剧烈运动的点；
    - 运动感知遮挡掩码 $F$ 是通过将遮挡区域与逐像素平均图像有较大颜色差异的像素相结合：$\boldsymbol{F}=\mathbb{I}\left(\left|\boldsymbol{C}_{0}-\sum_{j}^{N} \boldsymbol{C}_{j} / N\right|>\tau\right) \cup\left(\mathbf{1}-\boldsymbol{M}_{0}\right)$
    - $F$ 对具有大幅运动的区域以及初始化的高斯点的局部稀疏性进行掩码操作；
    - 在掩码 $F$ 中具有二维投影像素的三维点 $P_i$ 将与 $P_n$ 融合，以初始化规范状态。

### Optimization

$$
\mathcal{L}_C = \| M \odot (\hat{C} - C) \| \quad \mathcal{L}_D = \| M \odot (\hat{D}^{-1} - D^{-1}) \|
$$

## Experiments


## Reference

- [[论文评述] Deform3DGS: Flexible Deformation for Fast Surgical Scene Reconstruction with Gaussian Splatting](https://www.themoonlight.io/zh/review/deform3dgs-flexible-deformation-for-fast-surgical-scene-reconstruction-with-gaussian-splatting)