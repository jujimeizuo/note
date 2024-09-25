---
comment: true
counter: true
---
# EndoscopyDepthEstimation

> [!abstract]
> - paper：[:book: Dense Depth Estimation in Monocular Endoscopy with Self-supervised Learning Methods](https://arxiv.org/abs/1902.07766)
> - code：[:material-github: EndoscopyDepthEstimation-Pytorch](https://github.com/lppllppl920/EndoscopyDepthEstimation-Pytorch)


## Idea

1. Training Data：使用的数据集是无标注的内窥镜视频
    1. **Data Preprocessing**：首先使用 SfM 进行稀疏重建、估计相机位姿和可见点，生成稀疏形式数据。
    2. **Sparse Depth Map**：单目深度估计模块，仅预测到全局范围内的深度。为了实现有效的损失计算，深度预测的规模和 SfM 结果必须匹配。
    3. **Sparse Soft Mask**：稀疏掩码能利用稀疏形式数据中有效稀疏信号，并忽略其余无效区域。使用的是 SFL。

<center><img src="https://cdn.jujimeizuo.cn/note/cv/slam/EDE-2.jpg"></center>

2. Network Architecture：架构如下图。依靠来自SfM的稀疏信号和两帧之间的几何约束来学习从单个内窥镜视频帧预测密集深度图，在应用阶段，该网络具有从单个帧进行深度估计的简单单分支架构，下面的所有自定义层都是可微分的，以便网络可以以端到端的方式进行训练。
    1. **Monocular Depth Estimation**：使用 DenseNet 的修改版本，将最后一个卷积层的通道数更改为1，并用线性激活替换最终激活，即 log-softmax。还将网络上过度部分中的转置卷积层替换为最近邻上采样和卷积层。
    2. **Depth Scaling Layer**：该层与单目深度估计的深度预测规模和相应的 SfM 结果相匹配，以进行正确的损失计算。
    3. **Flow from Depth Layer**：为了使用 SfM 结果生成的稀疏流图来进行后面描述的 SFL 网络训练，首先需要将缩放的深度图转换为具有相对相机位姿和内参的稠密流图（借鉴使用生成的稠密流图作为光流估计网络的输入）。稠密流图的本质上是描述 3D 点变为到 2D 点的转换。
    4. **Depth Warping Layer**：稀疏流图主要为来自 SfM 的稀疏信息投射到帧的区域进行，鉴于大多数帧只有一小部分像素的值在稀疏流图中有效，大多数区域仍然没有得到适当的引导。通过相机运动和相机内参，可以通过加强两个相应深度预测之间的一致性来利用两帧之间的几何约束。直觉是，从两个相邻帧分别预测的密集深度图是相关的，因为观察到的区域之间存在重叠。为了使后面描述的深度一致性损失中强制执行的几何约束可微分，深度预测的观点必须首先对齐。

<center><img src="https://cdn.jujimeizuo.cn/note/cv/slam/EDE-1.jpg"></center>

3. Loss Functions
    1. **Sparse Flow Loss (SFL)**
    2. **Depth Consistency Loss (DCL)**


## Experiments