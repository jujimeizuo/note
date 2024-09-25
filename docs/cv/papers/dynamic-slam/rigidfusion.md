---
counter: true
comment: true
---

# RigidFusion

> [!Abstract]
> - paper：[:book: RigidFusion: Robot Localisation and Mapping in Environments with Large Dynamic Rigid Objects](https://arxiv.org/abs/2010.10841)
<!-- > - code：[:material-github: RigidFusion](https://github.com/BertaBescos/DynaSLAM) -->


## INTRODUCTION


在真实的 SLAM 场景中，我们会发现在遇到大量动态障碍物的场景时候，特别容易造成跟丢的问题。传统的解决方法是通过将动态障碍物滤除，而本文中提到将动态物体看做刚体进行跟踪。

文中提出一种新的 RGB-D SLAM 方法，可以同时分割、跟踪和重建静态背景和可能遮挡相机视野主要部分的大型动态刚性物体。之前的方法将场景的**动态部分视为异常值，因此局限于场景中的少量变化**，或依赖场景中所有对象的先验信息，以实现鲁棒的摄像机跟踪。**本文提出将所有动态部件视为一个刚体，同时分割和跟踪静态和动态部件。** 因此，在动态对象造成大遮挡的环境中，能够同时定位和重建静态背景和刚性动态组件。

> [!info]
> - 一个新的SLAM框架，使用RGB-D摄像头，在整个SLAM框架中同时分割、跟踪和重建场景，通过具有潜在漂移的运动先验来完成静态背景和一个动态刚体的构建。
> - 使用稠密SLAM建图的方法，对视觉输入中的大型动态遮挡(超过视野的65%)具有鲁棒性。同时该SLAM模型不依赖静态和动态模型的初始化;
> - 提供一个新的RGB-D SLAM数据集，数据集中包括具有在场景中造成大遮挡的动态对象和真实轨迹。

## RELATED WORK

动态视觉SLAM或视觉里程计方法可以分为**直接、间接或多运动里程计方法**。 机器人本体感知还可用于支持动态环境中的定位。

- **直接法**：需要对场景中的对象有充分的了解，如果未检测到动态对象，则失败。
- **间接法**：当动态对象成为主要部分是无法处理图像。

## OVERVIEW

本文提出一种 SLAM 框架，将动态部件视为单个刚体，利用运动先验分割静态部件和动态部件。利用分割后的图像对摄像机进行跟踪，重建背景和目标模型。

重建流程如下图所示，首先需要连续两个 RGB-D 关键帧 A 和 B，以及静态和动态物体的先验信息，静态和动态物体的先验信息及 $\widetilde{\xi}_s$ 和 $\widetilde{\xi}_d$ 是属于 $se(3)$ 的，此外还需要前一帧的语义分割信息 $\widetilde{\Gamma}_A \in \mathbb{R}^{W \times H}$。首先根据运动先验信息检测物体是否为动态物体；然后当物体运动时，基于帧间对其，我们联合估计分割 $\widetilde{\Gamma}_B$ 和 刚体运动 $\widetilde{\xi}_s$ 和 $\widetilde{\xi}_d$。这些片段用于重建静态环境和动态对象，并利用帧与模型的对其实现摄像机的定位。

<center><img src="https://cdn.jujimeizuo.cn/note/cv/slam/RigidFusion-1.jpg" alt="RigidFusion Pipeline"></center>

### 图像聚合

每个新的强度和深度图像 $(I,D) \in \mathbb{R}^{W \times H}$ 对通过使用 K-均值聚类，被分割成 K 个几何簇 $V=V_i|i=1,...,K$。假设每个簇满足刚性条件，每个刚体可以通过簇的组合来近似。同时文中还为每个集群分配一个分数 $\gamma_u \in [0,1]$ 表示簇是否属于静态刚体的概率；$\gamma_i=0$ 表示动态簇，而 $\gamma_i=1$ 表示静态簇。对于 RGB-D 帧 A，将总体分数表示为 $\gamma_A \in \mathbb{R}^K$。
### 距离判断

如果两个运动先验之间的差 $||\widetilde{\xi}_s -\widetilde{\xi}_d||^2$ 小于阈值 $\hat{d}$，则将图像中的所有聚类视为静态和动态分割。否则将共同优化当前帧的分数 $\gamma_B$ 以及静态和动态刚体的相对运动 $\widetilde{\xi}_s$ 和 $\widetilde{\xi}_d$。
### 图像分割

从聚类和分数中计算像素级分割 $\widetilde{\Gamma}_B \in \mathbb{R}^{W \times H}$。与静态融合类似，从分割中计算静态和动态刚体的加权 RGB-D 图像 $\widetilde{\Gamma}_B$。这些加权图像用于重建背景和动态目标的模型，并通过帧-模型对其来细化估计的相机姿态。
### 坐标系转换

分别从 world-frame、camera-frame 和 object-frame 表示为 $F_W、F_C、F_O$。使用 $T_{XY} \in SE(3)$ 将坐标系 $F_Y$ 中某个点的齐次坐标转换为 $F_X$。在图像帧 A 中，相机和物体的姿态分别是 $T_{WC_A}$ 和 $T_{WO_A}$。考虑两个图像帧 A 和 B，$\xi_s$ 与摄像机位姿的关系为 $T(\xi_s)=T_{WC_A}^{-1}T_{WC_B}=T_{C_AC_B}$，求出机器人移动的信息，$\xi_d$ 与摄像机的位姿的关系为 $T(\xi_d)=T_{WC_A}^{-1}T_{WO_A}T_{WO_B}^{-1}T_{WC_B}=T_{C_AO_A}T_{C_BO_B}^{-1}$，最后转化为相机和物体的相对运动关系。其中 $\widetilde{\xi}_s$ 和 $\widetilde{\xi}_d$ 可以由本体感觉传感器提供，如车轮里程计和手臂正向运动学。

在本文中，静态运动先验 $\widetilde{\xi}_s$ 是通过车轮里程计或通过在相机地面真值轨迹上添加模拟漂移来计算。通过模拟对象真值轨迹上的漂移来生成 $\widetilde{\xi}_d$。

<center><img src="https://cdn.jujimeizuo.cn/note/cv/slam/RigidFusion-2.jpg"></center>
