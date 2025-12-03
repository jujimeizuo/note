---
counter: true
comment: true
---

# MonST3R

> [!abstract]
> - paper：[:book: MonST3R: A Simple Approach for Estimating Geometry in the Presence of Motion](https://arxiv.org/abs/2410.03825)
> - code：[:material-github: MonST3R](https://github.com/HengyiWang/spann3r)

## Introduction

> [!Question] 问题导向
> DUSt3R 在动态场景中的局限性：
> 1. DUSt3R 对齐了移动的前景物体，但由于只在静态场景中进行训练，导致静态背景元素的对齐出现不正确的对齐。
> 2. DUSt3R 无法估计前景物体的几何形状和深度，并将它们放在背景中。
> <center><img src="/assets/images/cv/slam/monst3r-1.jpg"></center>

> [!Done] 解决方案
> MonST3R 直接从动态场景中估计每个 timestep 下的的 pointmap。然而缺乏适合的训练数据（带深度标签的动态视频），作者将该问题视为微调任务，识别多个适合的数据集，并在有限的数据上训练模型，即使没有明确的运动表示也能处理动态场景。
> <center><img src="/assets/images/cv/slam/monst3r-3.jpg"></center>
> 从动态场景中估算的 pointmap，则是根据物体的移动把动态物体的点云也显示出来。而静态部分的场景则需要实现 Multi-frame alignment。


## Method

<center><img src="/assets/images/cv/slam/monst3r-2.jpg"></center>

- 对于 finetune 过程，只微调了 prediction head 以及 decoder，而 encoder 固定不变。
- 额外增加了 RAFT 和 SAM2 用来分离动态和静态。
- 对于 多个视角下的全局优化仍然采用 DUSt3R 的全局 alignment 的模块，但是分别构建了三个 loss（光流、相机位姿的平衡、全局对齐）进而实现动态场景下的全局 pointmap 的构建。

## Experiments


## Reference

- [论文学习及实验笔记之——《MonST3R: A Simple Approach for Estimating Geometry in the Presence of Motion》](https://kwanwaipang.github.io/MonST3R/)
- [【动态三维重建】MonST3R：运动中的几何估计
](https://blog.csdn.net/qq_45752541/article/details/143260800)
- [MonST3R | UC伯克利、DeepMind等提出的运动状态下估算几何图形的先进方法](https://blog.csdn.net/moxibingdao/article/details/143154491)