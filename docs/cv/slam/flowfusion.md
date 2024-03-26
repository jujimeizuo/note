---
counter: true
comment: true
---

# FlowFusion

!!! abstract
    - paper：[:book: FlowFusion: Dynamic Dense RGB-D SLAM Based on Optical Flow](https://arxiv.org/abs/2003.05102)
    <!-- - code：[:material-github: DynaSLAM](https://github.com/BertaBescos/DynaSLAM) -->

## Introduction

- 基于流的动态/静态分割来处理动态SLAM问题。
- 提供了一种新颖的基于光流残差的动态分割和密集融合RGB-D SLAM方案。
- 通过改善动态因素的影响，在当前RGB-D帧中有效地提取动态片段，然后准确地重建静态环境。

## RELATED WORKS

- KinectFusion 和 ElasticFusion（EF） 实时重建静态室内环境。
- Co-Fusion（CF）是一个实时物体分割和追踪方法，结合了基于分层深度学习的分割方法和 EF 的静态稠密重建框架。
- 除了语义标记解决方案外，还有从稠密的 RGB-D 融合方案中找出动态点云作为异常值。例如联合运动分割和场景流估计方法（JF），以及一种静态背景重建方法（SF）。
- 利用基于深度学习的目标检测方法，通过预处理去除潜在的动态物体，然后重建环境。例如 PoseFusion（PF）。
- 将环境动态属性定义为语义概念，并利用 SLAM 工具解决。例如一种基于深度学习的 3D 场景流估计方法，该方法结合了两个深度学习网络。

## OPTICAL FLOW BASED JOINT DYNAMIC SEGMENTATION AND DENSE FUSION

<center><img src="https://cdn.jujimeizuo.cn/note/cv/slam/FlowFusion-1.jpg"></center>

### Visual Odometry in Dense RGB-D Fusion

- 输入两个连续的 RGB-D 帧 A 和 B，RGB 图像首先被馈送到 PWC-net 用于光流估计。
- 强度和深度对 A 和 B 被馈送到鲁棒相机自我运动估计器，以初始化相机运动

### Optical Flow Residual Estimated by Projecting the Scene Flow

- 通过计算每个簇的平均残差来区分是否为动态物体
    - 例如背景不移动，因此它们的残差较低
    - 动态物体的残差较高
- 深度和强度的残差不是一个好的指标，解决方案是使用场景流评估移动点云
- 为了摆脱相机的自身运动，引入了光流残差的概念，被定义为投影的 2D 场景流，以突出像素的动态属性。
- 下图是投影的 2D 场景在图像平面中流动
    - $x^p$ 是帧 A 中的一个对象点投影像素
    - $x^q$ 是帧 B 中的同一个 3D 点（属于移动对象）
    - 红色箭头表示场景流（世界空间运动）
    - 蓝色箭头是 $x^{a \to b}$ 中的光流
    - 绿色箭头 $x^{sf}$ 是图像平面中投影的 2D 场景流
    - $x^e$ 是摄像机自身运动产生的流

<center><img src="https://cdn.jujimeizuo.cn/note/cv/slam/FlowFusion-2.jpg"></center>

- 下图是迭代估计动态场景中的2D场景流.(a)是机器人向左移动而人类向右移动的场景.(b)是根据(a)的图像对估计的光流.颜色表示流动方向,强度表示像素位移.蓝色的流动是相机自我运动的结果.我们从光流中减去自我流,得到像平面上的场景流分量,如(c)所示.在(b)中迭代地移除场景流和 $x^e$ 在7次迭代之后就可以获得更好的2D场景流结果,如(d).

<center><img src="https://cdn.jujimeizuo.cn/note/cv/slam/FlowFusion-3.jpg"></center>

### Dynamic Clusters Segmentation

- 已经定义了三个残差 $r_I, r_D, r_F$，分别表示为强度、深度和光流
- 通过两步来区分簇是否为动态而不依靠平均残差
    1. 计算一个指标来组合这三个残差
    2. 设计一个最小化函数来限定簇的动态类别

## DYNAMIC SLAM EXPERIMENTS AND EVALUATIONS

略。