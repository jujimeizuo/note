---
counter: true
comment: true
---

# WildGS-SLAM

> [!abstract]
> - paper：[:book: WildGS-SLAM: Monocular Gaussian Splatting SLAM in Dynamic Environments](https://arxiv.org/abs/2504.03886)
> - code：[:material-github: WildGS-SLAM](https://github.com/GradientSpaces/WildGS-SLAM)

## Introduction

> [!Question] 问题导向
> 3DGS 如何引入动态环境单目 SLAM？

> [!Done] 解决方案
> 利用不确定性感知几何映射来处理动态环境。
> 1. 整合深度和不确定性信息；
> 2. 引入一种不确定性地图，由一个浅层 MLP 和 DINOv2 features 预测得出，用于引导动态物体的去除，增强了 DBA 和高斯地图优化；
> <center><img src="/assets/images/cv/slam/wildgs-slam-1.jpg"></center>


## Method

### Uncertainty Prediction

- 采用 NeRF-On-the-go 和 WildGaussians 的不确定性组件，在训练过程中加入自定义的深度不确定性损失。对于输入帧，提取 DINOv2 特征，并利用 MLP 实时训练，用来预测像素级的不确定性图；
- **Feed-Forward Uncertainty Estimation**：DINOv2 使用了微调的版本：[57]，提取后的 features 作为 MLP 的输入，输出为不确定性图；
- **Uncertainty Loss Function**：采用改进的 SSIM 以及来自 NeRF-On-the-go 的两个 regularizations terms，以及 L1 depth loss term，$$ 这个额外的深度信号可以提高模型区分干扰项的能力，增强不确定性 MLP 的训练；

    $$
    \mathcal{L}_{\mathrm{uncer}}=\frac{\mathcal{L}_{\mathrm{SSIM}}^{\prime}+\lambda_{1}\mathcal{L}_{\mathrm{uncer_D}}}{\beta_{i}^{2}}+\lambda_{2}\mathcal{L}_{\mathrm{reg_V}}+\lambda_{3}\mathcal{L}_{\mathrm{reg_U}}
    $$

### Tracking

- 基于 DROID-SLAM，在 DBA 中融入 depth 和 uncertainty，引入 Loop Closure 和 online global BA；
- **Depth and Uncertainty Guided DBA**：将估计出的 uncertainty map 整合到 BA 优化目标，处理动态，利用 Metric3D V2 [13] 估计出的度量深度稳定 DBA 层；因为 MLP 是在线训练，并能给出准确不确定性估计，所以在跟踪的早期阶段，对于每个新插入的关键帧，首先估计单目度量深度，并将其与光流一起添加到 DBA 目标优化：

$$
\arg\min_{\boldsymbol{\omega},d}\sum_{(i,j)\in E}\left\|\tilde{p}_{ij}-\Pi_{c}\left(\boldsymbol{\omega}_{j}^{-1}\boldsymbol{\omega}_{i}\Pi_{c}^{-1}\left(p_{i},d_{i}\right)\right)\right\|_{\Sigma_{ij}/\beta_{i}^{2}}^{2}+\lambda_{4}\sum_{i\in V}\left\|M_{i}\left(d_{i}-1/\tilde{D}_{i}\right)\right\|^{2}
$$

### Mapping

- 预测出插入的 keyframe 的 pose 后，按照 MonoGS 的 RGBD 策略，扩展高斯地图覆盖新探索的区域；在优化之前，如果先前 keyframe 的 pose 通过 Loop Closure 或全局 BA 更新，则会像 Splat-SLAM 主动 defrom 高斯地图；
- **Map Update**
    - 对高斯模型进行迭代优化，类似 MonoGS 采用 inter-frame covisibility 选择 keyframe，维持一个 local window，每次迭代中，至少 50% 的概率从 local window 中的 keyframe 均匀随机采样一个 keyframe，而所有其他 keyframe 平均分配剩余概率。对于选定的 keyframe，通过最小化 render loss $\mathcal{L}_{\mathrm{render}}$ 优化高斯地图：

    $$
    \mathcal{L}_{\mathrm{render}}=\frac{\lambda_5\mathcal{L}_{\mathrm{color}}+\lambda_6\mathcal{L}_{\mathrm{depth}}}{\beta^2}+\lambda_7\mathcal{L}_{\mathrm{iso}} \\
    \mathcal{L}_{\mathrm{color}}=(1-\lambda_{\mathrm{ssim}})\|\hat{I}-I\|_1+\lambda_{\mathrm{ssim}}\mathcal{L}_{\mathrm{ssim}}
    $$

    - 引入不确定性图 $\beta$ 作为 $\mathcal{L}_{\mathrm{color}}$ 和 $\mathcal{L}_{\mathrm{depth}}$ 的加权因子，同时用各向同性正则化损失 $\mathcal{L}_{\mathrm{iso}}$ 对高斯进行约束，防止在稀疏观测区域过度生长
    - 每次迭代中，还会计算 $\mathcal{L}_{\mathrm{uncer}}$，用于与地图优化并行训练 MLP

## Experiments

<center><img src="/assets/images/cv/slam/wildgs-slam-2.jpg"></center>

## Reference

- [13] Metric3d v2: A versatile monocular geometric foundation model for zero-shot metric depth and surface normal estimation.
- [39] Splat-slam: Globally optimized rgb-only slam with 3d gaussians.
- [57] Improving 2d feature representations by 3d-aware fine-tuning.
- [60] Glorie-slam: Globally optimized rgb-only implicit encoding point cloud slam.