---
counter: true
comment: true
---

# NID-SLAM

!!! abstract
    - paper：[:book: NID-SLAM: Neural Implicit Representation-based RGB-D SLAM In Dynamic Environments](https://arxiv.org/abs/2401.01189)
    <!-- - code：[:material-github: DynaSLAM](https://github.com/BertaBescos/DynaSLAM) -->

## Idea

- 神经隐式 SLAM + 动态环境
- **动态物体去除**：
    - 深度修正：计算深度图的图像梯度，当图像的水平或垂直梯度超过阈值时，将梯度方向上后续像素点的深度置为 0
    - 基于深度的语义分割：采用基于边界框的网络（YOLO）进行输入图像的语义分割，输出为潜在动态或可移动物体的二进制掩码
    - 背景修复：使用以前的视点获得的静态信息修复被遮挡的背景
- **关键帧选择策略**：两种选择策略
    - 动态物体比率较低的帧（覆盖策略）：倾向于覆盖最大场景区域的帧，确保场景边缘区域的全面优化）
    - 当前帧与前一关键帧重叠率较低的帧（重叠策略）：倾向于从与当前帧视觉上重叠的关键帧随机选择
    - 两个比率的加权和小于阈值则插入关键帧集合
    - 静态场景默认使用重叠策略
    - 为避免过度关注边缘区域并反复优化相同区域，我们首先使用基于覆盖的策略优化整个场景，然后多次使用基于重叠的策略，重复多次
- **场景表示和图形渲染**

<center><img src="https://cdn.jujimeizuo.cn/note/cv/slam/NID-SLAM-1.jpg"></center>


## Experiments

<center><img src="https://cdn.jujimeizuo.cn/note/cv/slam/NID-SLAM-2.jpg"></center>

<center><img src="https://cdn.jujimeizuo.cn/note/cv/slam/NID-SLAM-3.jpg"></center>

<center><img src="https://cdn.jujimeizuo.cn/note/cv/slam/NID-SLAM-4.jpg"></center>