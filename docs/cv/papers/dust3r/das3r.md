---
counter: true
comment: true
---

# DAS3R

> [!abstract]
> - paper：[:book: DAS3R: Dynamics-Aware Gaussian Splatting for Static Scene Reconstruction](https://arxiv.org/abs/2412.19584)
> - code：[:material-github: das3r](https://github.com/kai422/DAS3R)

## Introduction

> [!Question] 问题导向
> 动态视频的场景分解和静态背景重建，特别是动态物体占据场景比例较大。

> [!Done] 解决方案
> 与先前方法提供的静态置信度相比，DAS3R 以 MonST3R 为基座，通过训练得到更准确的运动掩码，并将静态性作为高斯属性，实现静态场景建模为具有动态感知优化的高斯点云。
> <center><img src="https://cdn.jsdelivr.net/gh/jujimeizuo/note@gh-pages/assets/images/cv/slam/das3r-1.jpg"></center>

## Method

### Dynamic region segmentation

- 与语义分割网络不同，DAS3R 依赖于对两个重叠图像帧的推理，直接从图像训练动态分割掩码。
- 为减少计算量，仅对第一帧预测动态掩码，动态掩码预测采用 DPT head。

|                                               DAVIS                                                |                                               Sintel                                               |
| :------------------------------------------------------------------------------------------------: | :------------------------------------------------------------------------------------------------: |
| <img src="https://cdn.jsdelivr.net/gh/jujimeizuo/note@gh-pages/assets/images/cv/slam/das3r-2.jpg"> | <img src="https://cdn.jsdelivr.net/gh/jujimeizuo/note@gh-pages/assets/images/cv/slam/das3r-3.jpg"> |

### Staticness

- 为高斯球添加静态属性 s，每个三维高斯与它累积的动态概率 M 相关联，该属性量化了高斯球属于静态区域的可能性 $s_{u,v,t} = 1 - \mathrm{M}_{u, v}^t,\in [0,1]$
- 渲染过程中， s 被纳入 $\alpha$-blend 计算中 $\mathcal{C}_{\mathrm{u,v}}=\sum_{i=1}^N\vec{c}_is_i\cdot\alpha_i\prod_{j=1}^{i-1}(1-s_j\cdot\alpha_j)$

## Experiments

## Reference

- [[论文审查] DAS3R: Dynamics-Aware Gaussian Splatting for Static Scene Reconstruction3](https://www.themoonlight.io/zh/review/das3r-dynamics-aware-gaussian-splatting-for-static-scene-reconstruction)
- [DAS3R](https://kai422.github.io/DAS3R/)