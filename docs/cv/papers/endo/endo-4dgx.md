---
counter: true
comment: true
---

# Endo-4DGX

> [!abstract]
> - paper：[:book: Endo-4DGX: Robust Endoscopic Scene Reconstruction and Illumination Correction with Gaussian Splatting](https://arxiv.org/abs/2506.23308)
> - code：[:material-github: Endo-4DGX](https://github.com/lastbasket/Endo-4DGX)

## Introduction

> [!Question] 问题导向
> 照明变化剧烈的场景（低光和过曝）下表现不佳。

> [!Done] 解决方案
> 1. 融入光照嵌入，能够建模与视角相关的亮度变化；
> 2. 引入区域感知增强模块，在高斯层面建模子区域的亮度；
> 3. 引入空间感知调整模块，学习视角一致的亮度调整；
> 4. 采用曝光控制损失，将不良曝光下的外观恢复到正常水平，实现适应光照的优化。
> <center><img src="/assets/images/cv/slam/endo-4dgx-1.jpg"></center>


## Method

### Illumination Embedding

- 为每个特定视角时间初始化可训练的光照 embeddings $e \in R^{N \times k}$，这些 embeddings 将与 Gaussians 联合优化；
- 在训练前，通过一个前向-逆向照明估计算法 $\mathcal{D}(\cdot)$ 进行预处理，得到输出的 $p = \mathcal{D}(I)$ 作为亮度先验（Bright 和 Dark），训练图像的光照条件（IC）为：

$$
IC(I) = 
\left\{\begin{matrix}
Bright, & if \quad mean(I) > mean(p) \\
Dark,   & if \quad mean(I) \leq mean(p)
\end{matrix}\right.
$$

### Region-Aware Enhancement

> [!Question] 使用单个网络同时处理 Bright 和 Dark 图像的矫正会导致严重的训练不平衡和收敛失败的问题。

- 使用两个分别对应不同光照条件（Bright 和 Dark）的独立网络（三层 MLPs 和 sigmoid），将训练图像按不同光照条件分组，每次将隐藏网络设置生针对 Bright 和 Dark 图像进行增强处理；
- 将区域感知增强构建为用于 Gaussian level 光照增强的仿射变换，给定特定视角的颜色 $C$，将特定视角的光照 embedding 输入到一个轻量级网络 $f_{region}$ 中；
- 网络的输出拆分为两个 1-channel 的参数 $\beta, \gamma$，对于 Gaussian 视角相关颜色，增强后的颜色为 $c_{tone}=\beta \cdot c + \gamma, | \beta,\gamma = f_{region}(c,e)$，这个模块基于学习到的光照 embedding 和特定视角特征，建模和微调 Gaussian 的子区域亮度。

### Spatial-Aware Illumination Adjustment

> [!Question] 尽管区域感知增强可以解决场景中单个元素或小区域的光照不均匀问题，但缺乏空间层面的调整能力，不足以应对图像级空间光照的挑战。

- 使用光照 embedding $e$ 和一个轻量级网络 $f_{spatial}$（三层 MLPs 和 tanh）预测一个参数 $\delta$，然后对 $c_{tone}$ 应用二次曲线调整：$\widetilde{C}_{tone} = C_{tone} + \delta \cdot C_{tone} (1-C_{tone}) | \delta = f_{spatial}(e)$。


### Illumination-Adaptive Optimization

> [!Question] 如何在变化的光照条件下保持稳定训练。

- 使用 $\mathcal{L}_1$ 损失和 $\mathcal{L}_{tv}$ 损失监督微调后的渲染颜色 $\widetilde{C}_{tone}$ 和渲染深度 $D$（深度监督使用立体匹配或 Depth-Anything 得到的深度 $\hat{D}$；

$$
\mathcal{L}_{color} = | \widetilde{C}_{tone} - \hat{C} | \odot M + \lambda_{tv} \mathcal{L}_{tv}(\widetilde{C}_{tone}) \\
\mathcal{depth} = \lambda_{depth} | \frac{D}{D_{max}} - \frac{\hat{D}}{D_{max}} | \odot M + \lambda_{tv} \mathcal{L}_{tv}(D)
$$

- 针对没有光照 embedding 的渲染颜色 $C$ 提出一种全局曝光控制损失，确保及时输入存在过曝光或欠曝光情况，重建场景也能具有一致且正常的曝光：

$$
\mathcal{Exposure} = \| avgpool1d(\frac{1}{3} \sum_{j \in R,G,B} C_j) - E \|^2
$$

- 最终损失函数：$\mathcal{L} = \mathcal{L}_{color} + \mathcal{L}_{depth} + \mathcal{L}_{Exposure}$

## Experiments


## Reference

- [[论文审查] Endo-4DGX: Robust Endoscopic Scene Reconstruction and Illumination Correction with Gaussian Splatting](https://www.themoonlight.io/zh/review/endo-4dgx-robust-endoscopic-scene-reconstruction-and-illumination-correction-with-gaussian-splatting)