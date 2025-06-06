---
counter: true
comment: true
---

# 4DTAM

> [!abstract]
> - paper：[:book: 4DTAM: Non-Rigid Tracking and Mapping via Dynamic Surface Gaussians](https://arxiv.org/abs/2505.22859)
> - code：[:material-github: 4DTAM](https://github.com/muskie82/4dtam)
> - video: [:clapper: 4DTAM](https://youtu.be/MRGhggLmTF0?si=51bqfAe9pYQNWgf-/)

## Introduction

> [!Question] 问题导向
> 4D-SLAM 没有解决，即使使用 2.5D 信号，由于优化空间的高维度，问题也很难解决。

> [!Done] 解决方案
> 提出第一种 4D 跟踪与映射的方法，通过可微渲染联合优化执行相机定位和非刚性表面重建。通过联合优化场景几何形状、外观、动态以及相机自身运动，从带有深度测量值或预测的彩色图像在线流中捕捉 4D scene。
> 1. 引入一种基于高斯表面基元的 SLAM 方法，更有效地利用深度信号，从而实现精确的表面重建；
> 对非刚性变形进行建模，采用由 MLP 表示的变形场，引入新颖的相机位姿估计技术以及有助于时空重建的表面正则化项；
> <center><img src="https://cdn.jsdelivr.net/gh/jujimeizuo/note@gh-pages/assets/images/cv/slam/4dtam-1.jpg"></center>


## Method

### Analytic Camera Pose Jacobian

- 3DGS 的输入是已标定位姿的图像，并且不提供相机位姿的梯度。为了加速优化，作者推导出 2DGS 的相机位姿的解析 Jacobian（W2C 相机位姿矩阵的最小 Jacobian）；
- 2DGS 在 优化 3D 均值期间将梯度反向传播到 $\mathbf{M}^T=\mathbf{W}\mathbf{H}$，推导偏导数 $\frac{\partial\mathbf{M}^T}{\partial\tau}$；
- 2DGS 还渲染 normal map，从中计算出损失进行监督，$\mathbf{n}_c=\boldsymbol{T}_{CW}\mathbf{t}_w$，同样推导偏导数 $\frac{\partial\mathbf{n}_c}{\partial\boldsymbol{\tau}}=\frac{\mathcal{D}\mathbf{n}_c}{\mathcal{D}\boldsymbol{T}_{CW}}=\begin{bmatrix}\boldsymbol{I}&-\mathbf{n}_c^\times\end{bmatrix}$；

### Warp Field

- 为了对 time-varying 变形进行建模，使用一个基于 coord 的 MLP 作为 warp-field [64]；
- 规范空间的 2D Gaussians 的时间 t 和 中心位置 x 作为输入，deformation MLP $f_{\theta}$ 产生偏移量，随后将规范 2D Gaussians 变换到 deformed 空间，输出为平均位置、旋转和缩放的偏移量：

    $$
    (\delta\boldsymbol{x},\delta\boldsymbol{r},\delta\boldsymbol{s})=\mathbf{f}_\theta(\gamma_1(\boldsymbol{x}),\gamma_2(t))
    $$

### Tracking and Mapping

#### Tracking

- 为最新传入的帧估计粗略的相机位姿，通过最小化传感器观测值与可变性高斯模型渲染之间的光度和深度渲染误差来实现；
- 假设在 latest keyframe timestamp $t_{kf}$ 处变形的场景结构最接近当前状态，从而相对于 $t_{kf}$ 时刻的变形高斯估计相机位姿；
- 进一步优化仿射亮度参数，every N frame 选择 keyframe，发送到 mapping 进一步优化；

#### Mapping

- mapping 在 sliding window 内对相机位姿、规范高斯和变形场进行联合优化；
- **Gaussian Management**：当注册一个新的 keyframe，根据 RGB-D 观测值反投影得到的点云，向规范高斯中添加新的高斯。与 3DGS 不同，2DGS 在其旋转向量中明确编码了表面法线信息，因此使用从深度传感器测量值估计的表面法线进行初始化，通过对相邻反投影深度点取有限差分来计算当前深度观测的表面法线，并将其指定为 2DGS $\mathbf{t}_w$ 的法向量：

    $$
    \mathbf{t}_w=\frac{\nabla_x\mathbf{p}_d\times\nabla_y\mathbf{p}_d}{|\nabla_x\mathbf{p}_d\times\nabla_y\mathbf{p}_d|}
    $$

- **4D Map Optimization**：对相机自身运动、外观、几何形状和场景动态进行联合优化。单相机缺乏时空密集观测，无法捕捉完整动态场景，要在时间 t 实现完整的空间 xyz 覆盖，引入了形状和运动的正则化项；除了光度和深度损失；
    - 还应用了基于传感器测量的法线正则化 $L_n=\sum_{i\in h\times w}(1-\mathbf{n}_i^\mathrm{T}\mathbf{N}_{sensor,i})$；
    - 为了约束未观测区域的运动，对高斯均值应用了 [27] 提出尽可能刚性的正则化损失 $L_{ARAP}$；
    - 还硬如了新的表面法线刚性损失，约束 2DGS 的表面法线在时间步 t1 和 t2 之间保持相似，以保持局部表面刚性；

    $$
    L_{total}=\lambda_{p}L_{p}+\lambda_{g}L_{g}+\lambda_{n}L_{n}+\lambda_{iso}L_{iso}+L_{ARAP}+L_{ARAP_n}
    $$

- **Global Optimization**：基于 sliding window 的全局优化会优先考虑最新的帧，这会导致过去 keyframe 信息随时间退化。跟踪完成后，如果还需要，可以执行全局优化来最终确定地图。此过程中，位姿和高斯数量是固定的，每次迭代会随机选择一个 keyframe，该过程使用 2DGS 的法向一致性损失。

## Experiments

## Reference

- [64] Deformable 3d gaussians for high-fidelity monocular dynamic scene reconstruction.