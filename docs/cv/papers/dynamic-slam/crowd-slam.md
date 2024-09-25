---
counter: true
comment: true
---

# Crowd-SLAM

> [!Abstract]
> - paper：[:book: Crowd-SLAM: Visual SLAM Towards Crowded Environments using Object Detection](https://link.springer.com/article/10.1007/s10846-021-01414-1)
> - code：[:material-github: Crowd-SLAM](https://github.com/virgolinosoares/Crowd-SLAM)

## Idea

- 动态 SLAM + 目标检测（拥挤的人群）
- 基于 ORB-SLAM2，额外增加一个目标检测线程
- 目标检测使用改版的 YOLO，用 Crowdhuman 训练的 CYTi
- 将边界框里的关键点（人的特征点）全部视为外点，进行去除
- 检查过滤区域并更新特征点数量，特征点的个数从给定的初始值开始，随着滤波面积增加而增大，300/30%，500/60%，700/90%，1200/95%。

<center><img src="https://cdn.jujimeizuo.cn/note/cv/slam/Crowd-SLAM.jpg" alt="Framework of Crowd-SLAM"></center>


## Experiments

<center><img src="https://cdn.jujimeizuo.cn/note/cv/slam/Crowd-SLAM-2.jpeg"></center>

<center><img src="https://cdn.jujimeizuo.cn/note/cv/slam/Crowd-SLAM-3.jpeg"></center>


## Drawbacks

1. 由于人物的姿势和相机的接近，人物占据图像大部分区域，导致特征耗尽
2. 不过滤除人之外的动态物体