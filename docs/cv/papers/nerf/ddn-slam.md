---
comment: true
counter: true
---
# DDN-SLAM

> [!abstract]
> - paper：[:book: DDN-SLAM: Real-time Dense Dynamic Neural Implicit SLAM](https://arxiv.org/abs/2401.01545)
> - code: not open source
<!-- > - code：[:material-github: DDN-SLAM](https://github.com/liadbiz/detect-slam) -->


## Idea

1. 提出了基于**语义特征**的动态 SLAM，通过结合**语义检测框架**和**高斯混合模型**背景深度概率检查方法，区分前景和背景以消除干扰的动态特征点；
2. 通过对动态点**重投影误差**的二次检查并 BA 来建立长期的数据关联；
3. 提出一种混合的背景恢复和渲染策略，包括利用**特征的光流来区分动态掩码**以进行背景恢复；
4. 提出一种由**静态稀疏点云引导的采样策略**，以增强对静态表面的重建；
5. 提出一种基于**动态掩码的渲染损失**，包括运动一致性损失、深度损失和颜色损失，以约束动态物体的渲染鬼影并消除遮挡。

<center><img src="https://cdn.jujimeizuo.cn/note/cv/slam/DDN-SLAM-1.jpg"></center>



## Experiments

无源代码。