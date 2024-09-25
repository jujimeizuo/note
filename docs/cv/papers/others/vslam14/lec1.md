# 初识 SLAM

!!! abstract
    - **SLAM** 是 **S**imultaneous **L**ocalization and **M**apping 的缩写，即同时定位与建图。它是指机器人在未知环境中同时建立地图并确定自身位置的过程。
    - 同时 SLAM 分为 **视觉 SLAM** 和 **激光 SLAM**，这里主要学习视觉 SLAM，其实它们的差距不是很大，都是通过传感器获取环境信息，然后通过算法进行处理，最后得到地图和机器人的位置，只不过一个是相机，一个是激光。
    - 可以观看 [机器人工匠阿杰](https://www.bilibili.com/video/BV1FW4y1M7PV/?spm_id_from=333.788&vd_source=5e048b202705330980eefcc9a56cc5d0) 来了解 SLAM 在做什么，怎么做。