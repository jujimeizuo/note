---
counter: true
comment: true
---

# EndoGaussian

> [!abstract]
> - paper：[:book: EndoGS: Deformable Endoscopic Tissues Reconstruction with Gaussian Splatting](https://arxiv.org/abs/2401.11535)
> - code：[:material-github: EndoGS](https://github.com/HKU-MedAI/EndoGS)

## Introduction

> [!Question] 问题导向
> 内窥镜视频在处理非刚性形变和工具遮挡异常困难，以往基于 NeRF 的方法，例如 EndoNeRF 和 LerPlane，存在优化耗时或重建质量不足的问题。

> [!Done] 解决方案
> 1. 首个基于 Gaussian Splatting 的内窥镜组织重建方法；
> 2. 结合静态 Gaussian 和时空形变参数来表示动态手术场景，并利用深度引导的监督和时空权重掩码来处理单目优化中的工具遮挡问题，同时引入表面对齐正则化项，以更好地捕捉组织几何结构；
> <center><img src="/assets/images/cv/slam/endogs-1.jpg"></center>


## Method

### Training Combined with Tool Masks and Depth Maps

- 使用标记的 $M_i \in \{0, 1\}$ 表示工具遮挡；
- 引入时空重要性采样策略，指示与遮挡相关的关键区域；
- 重要性图 $\mathcal{V}_i = (1-M_i) \odot \left ( 1 + \alpha \sum_{j=1}^T M_j / \left \| \sum_{j=1}^T M_j \right \|_F \right )$；
- $L_1$ 用于图像空间的监督：$\mathcal{L}_{L1}(i)=|I_i \odot \mathcal{V}_i - \hat{I}_i \odot \mathcal{V}_i|$；
- 使用估计的深度图引入深度引导损失，采用 Huber 损失 $\mathcal{L}_D(i)$ 进行深度正则化；
- 使用空间和时间维度上的 Total Variation (TV) 损失作为额外的正则化项。

### Surface-Aligned Gaussians

- 为了在三维线索有限的区域（特别是工具遮挡周围）减少伪影，为确保高斯分布与组织表面紧密结合，通过控制高斯分布的密度函数来进行表面对其归一化，可定义为 $d(p) = \sum_g \sigma_g \exp (-\frac{1}{2}(p - \mu_g)^T \sum_g^{-1}(p-\mu_g))$；
- 如果高斯分布与表面对其，可以做出三个假设：
    1. 离点 $p$ 最近的高斯分布 $g^* = \argmin_g \{(p-\mu_g)^T \sum_g^{-1}(p-\mu_g)\}$ 对密度 $d(p)$ 的贡献最大；
    2. 为确保三维高斯分布是扁平的，每个高斯分布 $g$ 的三个缩放因子中都有一个接近 0；
    3. 高斯分布是不透明的，可以通过交叉熵损失函数促使 $\sigma_i$ 为 1；
    - 在这些假设下，可以将密度近似表示为 $\tilde{d}(p)$，并将理想距离函数近似为 $f(p)$；
- SDF 损失：$\mathcal{L}_{SDF} = \frac{1}{\mathcal{P}} |\hat{f}(p) - f(p)|$；
- 法线向量正则化：$\mathcal{L}_{norm} = \frac{1}{\mathcal{P}} \sum_{p \in \mathcal{P}} \left \| \frac{\triangledown f(p)}{\|\triangledown f(p) \|_2} - n_{g^*}\right \|_2^2$；
- 不透明度正则化项：$\mathcal{L}_{opacity}(i) = -\sum_j (\sigma + \Delta \sigma)_j \log{\sigma + \Delta \sigma}_j$；
- 总优化目标为：

$$
\mathcal{L}(i) = \mathcal{L}_{L1}(i) + \lambda_D \mathcal{D}(i) + \lambda_{TV1} \mathcal{L}_{tv-spatial}(i) + \lambda_{TV2} \mathcal{L}_{tv-temporal} + \lambda_S (\mathcal{L}_{SDF} + \mathcal{L}_{norm} + 0.5 \mathcal{L}_{opacity}(i))
$$

## Experiments


## Reference

- [[论文审查] EndoGS: Deformable Endoscopic Tissues Reconstruction with Gaussian Splatting](https://www.themoonlight.io/zh/review/endogs-deformable-endoscopic-tissues-reconstruction-with-gaussian-splatting)