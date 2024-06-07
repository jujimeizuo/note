---
comment: true
counter: true
---
# Detect-SLAM

> [!abstract]
> - paper：[:book:Detect-SLAM: Making Object Detection and SLAM Mutually Beneficial](http://www.jdl.link/doc/2011/2018122715554767015_fangwei%20zhong%20et%20al.%202018%20-%20detect-slam%20-%20wacv.pdf)
> - code：[:material-github: Detect-SLAM](https://github.com/liadbiz/detect-slam)

## Introduction

- 将视觉 SLAM 与深度神经网络 DNN 的目标检测结合。
- 利用语义信息消除 SLAM Pipeline 中移动对象的负面影响。
- 针对语义信息的时延主要由通信和检测引起的问题，提出了一种实时传播每个关键点的移动概率的方法。
- 第一个将 SLAM 和基于 DNN 的检测器结合起来的工作，解决： 
	1. 提高 SLAM 在动态环境中的鲁棒性
	2. 构建语义地图
	3. 提高目标检测性能

<center><img src="https://cdn.jujimeizuo.cn/note/cv/slam/Detect-SLAM-1.jpg"></center>

## Related Work

**SLAM**

- Paschalis 等人专注于 3D 点云，Sun 等人在 2D Patch 上。它们都包括分割和额外获取移动对象的掩码。
- Detect SLAM 省略了这些操作并通过更新特征的移动概率来过滤属于移动对象的特征，是基于特征级表示的，并且可以更加鲁棒和高效的。

**DNN Based Object Detection**

- Faster R-CNN、YOLOv2、SSD
- Detect-SLAM 中部署 SSD 作为检测器模块
- 为了克服 SLAM 和检测器之间的延迟，避免逐帧检测，并考虑连续帧的时空一致性

**Combining SLAM and Object Detection**

- Pillai 设计了一个支持 SLAM 的物体识别系统
- McCormac 将 SLAM 和 CNN 结合起来，高效生成语义 3D 地图
- Bowman 将离散识别和数据关联问题与连续 SLAM 优化整合到一个优化问题，得到更精确的轨迹
- Duncan 创建一种基于单目的方法，使用目标检测器来解决传统单目的方法，使用目标检测器来解决传统单目 SLAM 系统中尺度模糊和漂移问题
- Sucar 将基于卡尔曼滤波的单目 SLAM 与检测器提供的语义信息相结合，以贝叶斯方案估计 3D 模型的全局规模

## Detect-SLAM

Detect-SLAM 以 ORB-SLAM2 为基，与之相比，包括三个新流程：

1. 动态物体去除，过滤掉与动态物体相关的特征；
2. 对象建图，重建在关键帧中被检测到的静态物体，由分配有对象 ID 的稠密点云组成；
3. SLAM 增强检测器，利用对象地图作为先验知识来提高在具有挑战性的环境中的检测性能；

### Moving Objects Removal

针对逐帧使用 SSD 目标检测整个系统的速度也只有 3FPS，这一部分提出两个策略解决：

1. 仅在关键帧中做目标检测，然后更新局部地图中点的移动概率以加速线程；
2. 在相机位姿估计前，通过特征匹配和匹配点扩展在跟踪线程中传播运动概率，有效地去除动态物体上提取的特征；

把属于运动物体的特征点的概率称为运动概率。如下图所示，我们根据移动概率将这些关键点区分为四种状态。在匹配点扩展中使用两个高置信度点将移动概率传播到相邻的不匹配点。在每个点通过传播获得移动概率后，我们移除所有动态点，并使用RANSAC过滤其他异常值以进行姿态估计。

<center><img src="https://cdn.jujimeizuo.cn/note/cv/slam/Detect-SLAM2.jpg"></center>


**Updating Moving Probability**

考虑到检测的延迟和连续帧的时空一致性，只选择关键帧的彩色图像，通过 DNN 对图像进行预处理和前向传播，在跟踪线程中逐帧传播运动概率。一旦获得检测结果，我们将关键帧插入本地地图并更新本地地图中的移动概率。更新在关键帧中找到匹配关键点的 3D 点的概率：

$$
P_t(X^i)=(1-\alpha)P_{t-1}(X^i)+\alpha S_t(X^i) \quad \quad 本文中选择 \quad \alpha = 0.3
$$

<center><img src="https://cdn.jujimeizuo.cn/note/cv/slam/Detect-SLAM3.jpg"></center>


**Moving Probability Propagation**

在跟踪线程中，通过两个操作逐帧估计每个关键点的移动概率：

1. 特征匹配
2. 匹配点扩展（移动概率传播）


<center><img src="https://cdn.jujimeizuo.cn/note/cv/slam/Detect-SLAM-4.jpg"></center>

### Mapping Objects

**Predicting Region ID**

- 预测图像空间中每个检测到的区域的对象 ID。区域 ID 预测的目的是在对象图中找到对应的对象 ID，或者如果是第一次检测到则生成一个新的 ID。
- 对象 ID 预测基于几何假设，即如果两个区域属于同一对象，则投影和检测区域应该重叠。（用 IOU 处理）

**Cutting Background**

尽管检测器提供了图像中对象的边界框，但它是一个矩形框，其中包含一些意想不到的背景，用于构建干净的对象图。因此，我们使用 Grab - Cut 算法分割背景，将重叠区域中先前重建对象投影的点作为前景种子，将边界框外的点作为背景。然后我们从边界框中得到一个目标对象的段掩码，经过三次迭代。

**Reconstruction**

利用对象掩码，创建分配有对象 ID 的对象点云，并过滤 3D 空间中的噪声点。最后，将物体点云转换为带有相机位姿的世界坐标，并将它们插入到物体地图中。

### SLAM-enhanced Detector

**Region Proposal**

每个目标区域是通过 3D 目标图投影到 2D 平面提出的，跟踪估计当前相机位姿。对具有相同对象 ID 的像素进行聚类来提出可能包含对象的候选区域。

**Region Filter**

有不在预期的区域被提出，因此需要剔除区域大小 20x20 px 的小候选框。

**Hard Example Mining**

对原始SSD网络进行微调，以提高类似场景中的检测性能。
## Experiment

略