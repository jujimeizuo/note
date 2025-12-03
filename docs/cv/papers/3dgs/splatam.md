---
counter: true
comment: true
---

# SplaTAM

> [!abstract]
> - paper：[:book: SplaTAM: Splat, Track & Map 3D Gaussians for Dense RGB-D SLAM](https://arxiv.org/pdf/2312.02126)
> - code：[:material-github: gaussian-splatting](https://github.com/spla-tam/SplaTAM?tab=readme-ov-file)

## Idea

### Introduction

- 第一个 3DGS 结合 SLAM 的系统，用 3DGS 表示场景，可以用无位姿的单目 RGB-D 相机实现密集 SLAM
- 解决神经辐射场场景表示的局限性，包括快速渲染和优化，确定区域是否被 map 的能力，以及通过添加和删除高斯的结构化地图扩展
- 采用了一个在线跟踪和建图框架，同时裁剪它，以专门使用底层的高斯表示和通过可微渲染的silhouette(轮廓)引导的优化
- 同时优化位姿估计、场景重建和新视角合成，允许实时渲染高分辨率的密集 3D 地图

### 高斯地图表示

- 场景中的底层地图表示为一组三维高斯分布，简化原始 GS，**只使用与视图无关的颜色，并迫使高斯分布是各向同性**
- 每个高斯值只有 8 个参数（RGB 3 个，中心位置 3 个，半径 1 个，不透明度 1 个）
- 根据高斯分布的不透明度加权的标准（非归一化）高斯方程，每个高斯分布都影响三维空间 $x \in R^3$ 的一个点：

$$
f(\mathcal{x}) = o \exp \left ( - \frac{\left \| \mathcal{x} - \mathcal{\mu} \right \|^2 }{2r^2} \right)
$$

### 泼溅的可微渲染

- 能够将底层高斯地图中的高保真颜色、深度和轮廓图像渲染到任何可能的相机参考帧中
- 可微渲染允许直接计算底层场景表示（高斯）和相机参数的梯度，利用渲染和真实的 RGB-D 帧之间的误差，并更新高斯和相机参数来减少误差
- 高斯渲染 RGB 图像的过程：给定一个三维高斯和相机位姿的集合，首先从前往后对所有高斯进行排序，通过**在像素空间中，依次 $\alpha$-合成每个高斯分布的二维投影，来渲染 RGB 图像**
- 像素 $p=(u,v)$ 渲染颜色公式：

$$
\begin{aligned}
C(\mathcal{p}) = \sum_{i=1}^n \mathcal{c}_i f_i(\mathcal{p}) \prod_{j=1}^{i-1}(1 - f_j(\mathcal{p})) \\
\mathcal{\mu}^{2D} = K \frac{E_t \mathcal{\mu}}{d}, \ \ \ r^{2D} = \frac{fr}{d}, \ \ \ where d = (E_t \mathcal{\mu})_z
\end{aligned}
$$

- $K$ 是相机内参，$E_t$ 是第 $t$ 帧处的相机旋转和平移的外参，$f$ 是焦距，$d$ 是相机坐标系下第 $i$ 个高斯值的深度
- 类似的深度渲染（可以与输入深度图比较，返回相对于 3D 地图的梯度）

$$
D(\mathcal{p}) = \sum_{i=1}^n d_i f_i(\mathcal{p}) \prod_{j=1}^{i-1}(1 - f_j(\mathcal{p}))
$$

- 渲染一个 silhouette（轮廓）图像来确定可见性，例如一个像素是否包含来自当前地图的信息：

$$
S(\mathcal{p}) = \sum_{i=1}^n f_i(\mathcal{p}) \prod_{j=1}^{i-1}(1 - f_j(\mathcal{p}))
$$


### SLAM 系统

<center>
<img src="/assets/images/cv/slam/SplaTAM-2.jpg">
</center>


> [!tip]
> 从高斯底层表示和可微渲染器建立一个 SLAM 系统。
> 假设有一个现有的地图（通过一组三维高斯分布表示），已经拟合了第 1 帧到第 t 帧。给定一个新的 RGB-D 帧 t+1，SLAM 系统会进行以下操作：
> 
> 1. **相机跟踪**：利用 t + 1 帧的相机位姿，最小化 RGB-D 序列的图像和深度重建误差，但只评估轮廓内的像素的误差
> 2. **高斯密度**：根据渲染的轮廓和输入深度，向地图中添加新的高斯
> 3. **地图更新**：给定从第 1 帧到 第 t+1 帧的相机位姿，最小化所有图像的 RGB 和深度误差来更新高斯分布参数。代码中，为保持批处理大小和可管理性，将对选好的，与最近帧重叠的关键帧子集进行优化

#### 初始化

第一帧跳过跟踪，将相机位姿设置为 identity，稠密化中，由于渲染的轮廓为空，**所有像素都用于初始化新的高斯**。对于每个像素，添加一个颜色为像素的新高斯，中心位置为投影的像素深度，不透明度为 0.5，半径等于一个像素半径投影到 2D 图像的深度除以焦距 $r = \frac{D_{GT}}{f}$

#### 相机跟踪

- 估计当前输入的在线 RGB-D 图像的相机位姿。通过对相机中心 + 四元数空间中姿态参数的恒定速度正向投影，为一个新的时间步初始化相机位姿

$$
E_{t+1}=E_t + (E_t - E_{t-1})
$$

- 通过基于梯度的优化，通过可微分渲染 RGB、深度、和轮廓图，并更新相机参数，同时保持高斯参数不变，以最小化损失：

$$
L(t) = \sum_\mathcal{p} (S(\mathcal{p}) > 0.99)(L_1(D(\mathcal{p}))+0.5L_1(C(\mathcal{p})))
$$

- 上述为深度和颜色上的 $L_1$ 损失，颜色的权重少一半，只应用以上损失于通过轮廓图渲染的像素。轮廓图捕获了地图的不确定性。这对于跟踪新的相机位姿非常重要，因为新帧通常包含在地图中尚未捕获或经过良好优化的新信息。如果一个像素没有 GT 深度，则 $L_1$ 损失为 0

#### 高斯稠密化

- 为每个新进入帧在地图中初始化新的高斯分布。
	- 在跟踪之后，对新进入帧的相机位姿有一个准确的估计
	- 对于深度图像，对高斯分布在场景中的位置有了好的估计
	- 当前的高斯已经准确地表示场景几何，不需要添加高斯，因此创建一个密集化 mask 来确定哪些像素应该被密集化

	$$
	M(\mathcal{p}) = (S(\mathcal{p})<0.5) + (D_{GT}(\mathcal{p})<D(\mathcal{p}))(L_1(D(\mathcal{p}))>50 MDE)
	$$

- 此 mask 只显示地图密度不足的地方 ($S < 0.5$)，或者在当前估计的几何图形前面有新的几何图形。对于每个像素，基于这个 mask，添加一个新的高斯进行第一帧初始化


#### 高斯地图更新

- 基于估计的在线相机位姿下，更新三维高斯地图的参数。通过可微渲染和基于梯度的优化来实现，**和跟踪不同的是，相机位姿是固定的，高斯分布的参数被更新**
- 和已知相机位姿的图像拟合辐射场的经典问题相似，有两个优化的地方：
	- 不是从头开始，而是从最近构建的地图中预热，开始优化
	- 不优化所有之前的关键帧，而是选择可能影响新添加的高斯分布的帧。将每 n 帧保存为关键帧，并选择 k 帧进行优化，包括当前帧、最近的关键帧，以及 k−2 之前与当前帧重叠最高的关键帧。重叠是通过取当前帧深度图的点云，并确定每个关键帧的错误点数来确定的
- 优化和跟踪的损失相似，但不使用轮廓 mask（因为要优化所有像素）。另外在 RGB 渲染中添加一个 SSIM 损失，并剔除不透明度接近 0 的无用高斯分布


## Experiment

<center>
<img src="/assets/images/cv/slam/SplaTAM-1.png">
</center>

## Reference

- [学习笔记之——3D Gaussian SLAM，SplaTAM配置（Linux）与源码解读-CSDN博客](https://blog.csdn.net/gwplovekimi/article/details/135647242)
- [实验笔记之——基于TUM-RGBD数据集的SplaTAM测试\_jiyu tum-rgbd数据集的splatam测试-CSDN博客](https://blog.csdn.net/gwplovekimi/article/details/135671402)
- [【三维重建】【SLAM】SplaTAM：基于3D高斯的密集RGB-D SLAM(CVPR 2024)-CSDN博客](https://blog.csdn.net/qq_45752541/article/details/136349064)
- [论文复现《SplaTAM: Splat, Track & Map 3D Gaussians for Dense RGB-D SLAM》\_splatam论文解析-CSDN博客](https://blog.csdn.net/weixin_65688914/article/details/137918527?depth_1-utm_source=distribute.pc_relevant.none-task-blog-2~default~BlogCommendFromBaidu~Rate-7-137918527-blog-136349064.235%5Ev43%5Epc_blog_bottom_relevance_base7)