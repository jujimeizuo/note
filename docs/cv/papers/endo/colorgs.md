---
counter: true
comment: true
---

# ColorGS

> [!abstract]
> - paper：[:book: ColorGS: High-fidelity Surgical Scene Reconstruction with Colored Gaussian Splatting](https://arxiv.org/abs/2508.18696)

## Introduction

> [!Question] 问题导向
> 内窥镜视频中可形变组织高保真重建的挑战，特别是现有方法在捕捉细微颜色变化和建模全局形变方面存在局限性。

> [!Done] 解决方案
> 提出 ColorGS，整合空间自适应颜色编码和增强形变建模。
> 1. 引入彩色高斯基元，采用具有可学习颜色参数的动态锚点来自适应地编码空间变化的纹理，提升在复杂光照和组织相似性条件下的颜色表现力；
> 2. 设计增强型变模型（EDM），将时间感知高斯基函数与可学习的时间无关形变相结合，能捕捉局部组织形变和全局运动一致性。
> <center><img src="/assets/images/cv/slam/colorgs-1.jpg"></center>


## Method

### Color Gaussian Primitives

> [!Question] 传统 3DGS 为每个 Gaussian primitive 分配固定的颜色属性，这在复杂照明条件和组织外观相似的手术场景中，难以捕捉到组织间细微的颜色差异，导致重建不佳。

- 为每个高斯基元引入 $k$ 个动态锚点 $A_i = (A_x^i, A_y^i)$，并带有颜色参数 $c_i$；
- 当光线与高斯基元相交并在渲染平面上生成焦点 $p=(u,v)$ 时，每个锚点对交点颜色的贡献通过指数衰减函数来衡量，衰减率取决于 $p$ 与锚点坐标 $A_i$ 之间的距离: $F_{A_i}(p) = e^{-\lambda_e \| p - A_i \|^2}$；
- 这些锚点产生的附加颜色 $F_c(p)$ 计算为所有锚点贡献的总和: $F_c(p) = \sum_{i=0}^{k-1} F_{A_i}(p)c_i$；
- 每个高斯基元的颜色函数 $c(p,d)$ 由方向 d 的 SH 分量和附加颜色 $F_c(p)$ 共同决定: $c(p,d) = SH(d) + F_c(p)$;
- where, $\lambda_e = 0.1, k=4$。

### Enhanced Deformation Model (EDM)

> [!Question] 现有方法通常利用时间感知基函数的线性组合来建模高斯基元的运动，然而，高斯基函数虽然能提供局部影响保留细节，但其局部性难以捕捉一致的拳击运动趋势，尤其在需要大量基函数和复杂参数优化才能精确拟合全局运动。

- EDM 将运动解耦为两部分：
    - 具有时间感知的高斯函数的线性组合所表示的局部动态；
    - 与时间无关的全局运动参数所建模的全局运动趋势；
- 高斯基函数：$\tilde{b}(t;\theta_j^x,\sigma_j^x)=\exp(-\frac{(t-\theta)^2}{2\sigma^2})$;
- 以高斯基元在 $x$ 方向的中心位置为例，任意时刻 $t$ 的位置可以表示为：$\psi^x(t,\Theta^x)=\sum_{j=0}^{B-1}\omega_j^x\tilde{b}(t;\theta_j^x,\sigma_j^x)+\delta_x$;
- where $B=17$。

### Optimization

$$
\mathcal{L}_{total} = \| M \odot (\hat{C} - C) \| + \| M \odot (\hat{D} - D) \|
$$

## Experiments


## Reference

- [[论文审查] ColorGS: High-fidelity Surgical Scene Reconstruction with Colored Gaussian Splatting](https://www.themoonlight.io/zh/review/colorgs-high-fidelity-surgical-scene-reconstruction-with-colored-gaussian-splatting)