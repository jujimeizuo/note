---
counter: true
comment: true
---

# 4DTAM

> [!abstract]
> - paper：[:book: 4D Gaussian Splatting SLAM](https://arxiv.org/abs/2503.16710)
> - code：[:material-github: 4DGS-SLAM](https://github.com/yanyan-li/4DGS-SLAM)
<!-- > - video: [:clapper: 4DTAM](https://youtu.be/MRGhggLmTF0?si=51bqfAe9pYQNWgf-/) -->

## Introduction

> [!Question] 问题导向
> 

> [!Done] 解决方案
> 1. 提出一种新颖的 4DGS Pipeline，用于在高斯辐射场中定位相机位姿并表示动态场景；
> 2. 将基元分为静态和动态高斯，并引入稀疏控制点以及一个多层感知器（MLP）来对动态高斯的运动进行建模；
> 3. 一种 2D 光流渲染算法，提高 4D 高斯场的性能。分别从动态 GS 和一个预训练模型估计 2D 光流图，然后将其作为约束来学习动态高斯的运动。
> <center><img src="https://cdn.jsdelivr.net/gh/jujimeizuo/note@gh-pages/assets/images/cv/slam/4dgs-slam-1.jpg"></center>


## Method

## Experiments

## Reference
