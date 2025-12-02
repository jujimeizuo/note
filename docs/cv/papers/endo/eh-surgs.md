---
counter: true
comment: true
---

# EH-SurGS

> [!abstract]
> - paper：[:book: EH-SurGS: Deformable Gaussian Splatting for Efficient and High-Fidelity Reconstruction of Surgical Scenes](https://arxiv.org/abs/2501.01101)
> - code：[:material-github: EH-SurGS](https://github.com/IRMVLab/EH-SurGS)

## Introduction

> [!Question] 问题导向
> 现有方法在处理不可逆的动态变化（如组织剪切）以及缺乏手术场景变形的分层建模方面存在一定的局限性。

> [!Done] 解决方案
> 1. 融合 3D Gaussians 生命周期的变形建模，有效捕捉常规变形和不可逆变形；
> 2. 自适应运动层次策略，用于区分场景中的静态和可变性区域，减少通过变形场的 3D Gaussians 数量，提高渲染速度；
> <center><img src="https://cdn.jsdelivr.net/gh/jujimeizuo/note@gh-pages/assets/images/cv/slam/eh-surgs-2.jpg"></center>
> <center><img src="https://cdn.jsdelivr.net/gh/jujimeizuo/note@gh-pages/assets/images/cv/slam/eh-surgs-1.jpg"></center>


## Method

### Deformation Modeling with Life Cycle

> [!Question] 场景中的剪切，现有方法通常会产生伪影。

- 使用可学习的高斯函数和权重来表示 3D Gaussians 的位置、旋转和尺度的变换，以此模拟变形，高斯函数为：$b(t)=\exp\left(-\frac{1}{2\sigma^2}(t-\theta)^2\right)$，在时间点 $t$ 处的变形表示为：$x_t=x_0+\sum_{j=1}^B\omega_j^xb^x(t)$；
- 为了对每个 Gaussians 的生命周期建模，不透明度 $\alpha$ 采用了与建模位置变换相同的方法：$\alpha_t=\alpha_0+\sum_{j=1}^B\omega_j^\alpha b^\alpha(t)$；

### Adaptive Motion Hierarchy Strategy

> [!Question] 现有方法通常采用简单的变形渲染策略，无法区分场景中不同区域的运动尺度，导致渲染降低。

- 使用一个与图像分辨率相同的掩码 $F \in R^{H \times W}$ 来区分可变性区域和静态区域，该掩码随着优化交替更新；
- **Update criteria**
    - 可变性区域和静态区域从两个角度进行区分：平均形变和动态与静态渲染损失：
    - **平均形变**：规范空间的 Gaussian 经过形变建模模块后，计算每个区域所有 Gaussians 的位置变化，然后归一化、求和取平均，得到每个区域的平均形变 $\Delta t$，如果超过设定的阈值 $\delta_1=0.05$，则该区域被加入潜在动态区域集 $Q$，否则放入潜在静态区域集 $W$；
    - **动态与静态渲染损失**：对于同一损失，计算启用和不启用形变模块时的 Gaussians 渲染损失，分别为 $L_d$ 和 $L_s$，如果该区域是静态的，则 $L_d$ 和 $L_s$ 应保持一致（差值小于 $\delta_2=0.5$），且该区域会被加入静态区域集 $W^\prime$，相反，如果该区域是动态的，$L_d$ 应远小于 $L_s$，此时该区域会被加入动态区域集 $Q^\prime$；
- **Update process**
    - **Initialization**：将输入的 RGB 划分为 $N \times N$ 个区域，每个区域 $i$ 的掩码 $F_i$ 初始化为动态 $F_i=0$；
    - **Update the mask**：当迭代次数达到阈值时，计算每个区域的平均形变 $\delta_t,L_d,L_s$，根据更新标准更新每个区域的掩码，$W$ 和 $W^\prime$ 的交集更新为静态，$Q$ 和 $Q^\prime$ 的交集更新为动态；
    - **Region splatting**：如果区域 $q \in W$ 且 $q \in Q^\prime$ 或 $q \in Q$ 且 $q \in W^\prime$，则该区域为冲突集合，需要切割，将原始区域均匀划分为四个动态区块，确保更细致的分隔；
    - **Update**：根据模型的优化进度动态更新 $N_m=N_m^{\prime}\times\mathrm{factor},\quad\mathrm{factor}=\frac{L_l}{L_c}$。

### Learning the Model

- 如果迭代达到掩码更新阈值 $N_m$，就更新掩码 $F$，否则由 $F$ 确定哪些 3D Gaussians 分布需要通过可变性模型，然后进行渲染损失；
- 引入排序损失 $L_{rank}$，$L = L_c + L_D + \lambda \mathcal{L}_{rank}$。


## Experiments


## Reference

- [[论文评述] Deformable Gaussian Splatting for Efficient and High-Fidelity Reconstruction of Surgical Scenes](https://www.themoonlight.io/zh/review/deformable-gaussian-splatting-for-efficient-and-high-fidelity-reconstruction-of-surgical-scenes)