---
counter: true
comment: true
---

# 前置知识

!!! abstract
    点云配准基础知识，主要为点云基础、处理方法和点云配准方法的介绍和比较等


## 点云基础

- 点云概念：点云是同一空间参考系下表达目标空间分布和目标表面特性的海量点集合，在获取物体表面每个采样点的空间坐标后，得到的是点的集合，称之为“点云”（Point Cloud）。
- 点云图像是最基础也是最常见的三维图像：三维图像是一种特殊的图像信息表达形式，相较于常见的二维图像，其最大的特征是表达了空间中三个维度（长度宽度和深度）的数据。
- 三维图像的表现形式：深度图（以灰度表达物体与相机的距离），几何模型（由 CAD 软件建立），点云模型（所有逆向工程设备都将物体采样成点云）。
- 点云根据测量原理主要分为两种
    - 根据激光测量原理得到的点云，包括三维坐标 XYZ 和激光反射强度 I。强度信息与目标的表面材质、粗糙度、入射角方向，以及仪器的发射能量，激光波长有关。
    - 根据摄影测量原理得到的点云，包括三维坐标 XYZ 和颜色信息 RGB。
    - 还有激光和摄影相结合在一起的多传感器融合技术，这种得到的包括三维坐标 XYZ、颜色信息 RGB 和激光反射强度 I。
- 点云的获取设备（只针对摄影）：RGBD设备（深度摄像机）。
- 点云的属性：空间分辨率、点云精度、表面法向量等。
- 点云存储格式 `.pts; .asc; .dat; .stl; .imw; .xyz; .las;`
- 点云的数据类型（以 PCL 库为例）：
    - `pcl::PointXYZ`：float x, y, z; 表示了 xyz3D 信息，可以通过 points[i].data[0] 或 points[i].x 访问 x 坐标值。
    - `pcl::PointXYZI`：float x, y, z, intensity; 表示了 XYZ 信息加上强度信息的类型。
    - `pcl::PointXYZRGB`：float x, y, z, rgb; 表示了 XYZ 信息加上 RGB 信息，RGB 存储为一个 float。
    - `pcl::PointXYZRGBA`：float x, y, z; uint32_t rgba; 表示了 XYZ 信息加上 RGBA 信息，RGBA 用 32bit 的 int 型存储的。
    - `pcl::PointXY`：float x, y; 表示了 XY 信息。
    - `pcl::Normal`：表示给定点所在样本曲面上的法线方向，以及对应曲率的测量值，用第四个元素来占位，兼容 SSE 和高效计算

## 点云处理

!!! note "图像处理的三个层次"
    - 低层次：图像强化，滤波，关键点/边缘检测等基本操作
    - 中层次：连通域标记，图像分割等操作
    - 高层次：物体识别，场景分析等操作
    - PCL 对点云处理方法给出较为明晰的层次划分，如下图所示：

    <center><img src="https://cdn.jujimeizuo.cn/note/cv/pcd/pcr/pc-processing.png" alt="点云处理方法"></center>

### 低层次处理方法

- 滤波方法：双边滤波、高斯滤波、条件滤波、直通滤波、随机采样一致性滤波
- 关键点：ISS3D、Harris3D、NARF、SIFT3D

### 中层次处理方法

- 特征描述：法线和曲率的计算、特征值分析、SHOT、PFH、FPFH、3D Shape Context、Spin Image
- 分割与分类：
    - 分割：区域生长、Ransac 线面提取、全局优化平面提取、K-Means、Normalize Cut （Context based）、3D Hough Transform（线、面提取）、连通分析
    - 分类：基于点的分类、基于分割的分类、基于深度学习的分类（PointNet、OctNet）

### 高层次处理方法

- 配准：点云配准分为粗配准（Coarse Registration）和精配准（Fine Registration）两个阶段。
    - **粗配准**是指在点云相对位姿完全位置的情况下对点云进行配准，可以为精配准提供良好的初始值。当前较为普遍的点云自动粗配准算法包括穷举搜索的配准算法和基于特征匹配的配准算法
        - **基于穷举搜索的配准算法**：遍历整个变换空间以选取使误差函数最小化的变换关系或者列举出使最多点对满足的变换关系。如 RANSAC 配准算法、四点一致集配准算法（4-Point Congruent Set，4PCS）、Super4PCS 算法等
        - **基于特征匹配的配准算法**：通过被测物体本身所具备的形态特性构建点云间的匹配对应，然后采用相关算法对变换关系进行估计。如基于点 FPFH 特征的 SAC-IA、FGR 等算法、基于点 SHOT 特征的 AO 算法以及基于线特征的 ICL 等
    - **精配准**的目的是在粗配准的基础上让点云之间的空间位置差别最小化。应用最为广泛的精配准算法应该是 ICP 以及 ICP 的各种变种（稳健 ICP、point to plane ICP、Point to line ICP、MBICP、GICP、NICP）
- SLAM 图优化
    - Ceres、g2o、LUM、ELCH、Toro、SPA
    - SLAM 方法：ICP、MBICP、IDC、likehood Field、NDT
- 三维重建
    - 柏松重建、Delaunay triangulations、表面重建、人体重建、建筑物重建、树木重建
    - 结构化重建：不是简单的构建一个 Mesh 网格，而是为场景进行分割，为场景结构赋予语义信息。场景结构有层次之分，在几何层次就是点线面
    - 实时重建：重建植被或者农作物的 4D（3D+时间）生长态势；人体姿态识别；表情识别
- 点云数据管理：点云压缩，点云索引（KD、Octree），点云 LOD（金字塔），海量点云的渲染


## 点云配准

> 点云配准（Point Cloud Registration），又名点云拼接、点云注册，对于两帧有重叠信息的点云，通过求解变换矩阵（旋转矩阵 R 和平移矩阵 T），使得重叠部分点云变换到同一个统一的坐标系下。

前期以传统方法为主，2018 年及以后基于深度学习的配准方法居上。

<center><img src="https://cdn.jujimeizuo.cn/note/cv/pcd/pcr/pcr-development-sequence.png" alt="点云配准的发展脉络图"></center>

点云配准可以基于以下 5 个方面学习和进阶：

1. **ICP 算法**：点云配准领域最为经典的算法，[Least-squares fitting of two 3-D point sets](https://www.researchgate.net/publication/224378053_Least-squares_fitting_of_two_3-D_point_sets_IEEE_T_Pattern_Anal)，证明了如何在已知点对的关系时用 SVD 求解变换矩阵。
2. **PFH 和 FPFH 特征和基于 RANSAC 的配准算法**：ICP 算法的缺点很明显，寻找点对应关系时是基于距离的，当初始位姿很差时，ICP 算法基本失效。基于特征 + RANSAC 的算法此时发挥优势，它通过点的特征寻找对应点对，只要点的特征表达能力够强，即使初始位姿很差，也可以找到正确的点对应关系，从而实现点云配准；但点的特征在大多数情况下是不鲁棒的，所以结合 RANSAC 算法是不错的选择。特征描述子建议查看 FPFH，对应论文为 [Fast point feature histograms (FPFH) for 3D registration (ICRA 2009)](https://www.cvl.iis.u-tokyo.ac.jp/class2016/2016w/papers/6.3DdataProcessing/Rusu_FPFH_ICRA2009.pdf)
3. **端到端的深度学习配准模型**：最近两三年的时间基于深度学习的配准模型出现很多，包括基于 global features-based 和 correspongence-based，两种模式。Global features-based 方法包括 [PointNetLK: Point Cloud Registration using PointNet (CVPR2019)](https://arxiv.org/pdf/1903.05711.pdf) 和 [PCRNet: Point Cloud Registration Network using PointNet Encoding (arXiv2019)](https://arxiv.org/pdf/1908.07906.pdf)。 这里可以优先看 PCRNet, 因为其算法和实现较为简单, 容易 follow。Correspondence-based 方法的典型代表包括 [DCP (ICCV2019)](https://arxiv.org/pdf/1905.03304.pdf), [PRNet (NeurIPS)](http://papers.nips.cc/paper/9085-prnet-self-supervised-learning-for-partial-to-partial-registration.pdf) 和 [RPMNet (CVPR2020)](https://arxiv.org/pdf/2003.13479.pdf). 这些方法都是开源的, 除了 PRNet 的代码在训练时容易崩溃外，其它的代码都是不错的。
4. **基于 RANSAC 的深度学习配准模型**：端到端的深度学习配准模型大多只在 ModelNet40 上是有效的，面对真实的数据集如 3DMatch 和 KITTI 时则效果表现不好。一部分原因是真实数据集较为复杂，另一部分原因是网络结构不足以准确学习大部分点的特征。由此就会导致 Inlier ratio 较低，端到端的配准网络不能发挥很好的效果。基于 RANSAC 的深度学习配准主要代表包括 [FCGF (ICCV 2019)](https://openaccess.thecvf.com/content_ICCV_2019/papers/Choy_Fully_Convolutional_Geometric_Features_ICCV_2019_paper.pdf), [D3Feat (CVPR2020)](https://arxiv.org/pdf/2003.03164.pdf) 和 [PREDATOR (CVPR2021)](https://arxiv.org/pdf/2011.13005.pdf).
5. **Open3D的使用**：最后但也是很重要的一环，一个高效处理点云的工具，推荐 [Open3D](http://www.open3d.org/docs/release/)。Open3D 提供了 4 个和配准有关的函数，包括 ICP 及其变种，基于 RANSAC 的算法和 FGR 算法等。