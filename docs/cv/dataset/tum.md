---
counter: true
comment: true
---

# TUM 数据集

!!! abstract
    TUM RGB-D 数据集由在不同的室内场景使用 Microsoft Kinect 传感器记录的39 个序列组成，包含了 
    
    - Testing and Debugging（测试）
    - Handheld SLAM（手持SLAM）
    - Robot SLAM（机器人SLAM）
    - Structure vs. Texture（结构 vs 低纹理）
    - Dynamic Objects（动态物体）
    - 3D Object Reconstruction（三维物体重建）
    - Validation Files（验证集）
    - Calibration Files（标定文件）

    等几种针对不同任务的数据集，每个种类有包含多个数据，可以用于多种任务的性能测试。其中之后验证集没有真值，只能通过 TUM 提供的在线测试工具评测我们的计算结果。TUM数据集带有标准的轨迹和一些比较工具，所以非常适合用来做研究。

    - 主页：https://vision.in.tum.de/data/datasets/rgbd-dataset/download
    - 在线测评工具：https://vision.in.tum.de/data/datasets/rgbd-dataset/online_evaluation


## 数据集格式

### ros bag

可用 ros 的 rosbag 命令进行播放，相应节点订阅图像话题即可。

### tgz

压缩后包含：

1. rgb.txt 和 depth.txt 文件记录了各文件的采集时间和对应的文件名
2. rgb/ 和 depth/ 目录存放采集到的 png 格式图像文件，以采集时间命名
3. groundtruth.txt 为外部运动捕捉系统采集到的相机位姿，格式为（time, tx, ty, tz, qx, qy, qw）

!!! note
    - 彩色图、深度图和标准轨迹的采集都是独立的，轨迹的采集频率比图像高很多。
    - 在使用数据之前，需要根据采集时间，对数据进行一次时间上的对齐，以便对彩色图和深度图进行配对。
    - 可以把采集时间相近于一个阈值的数据，看成是一对图像，并把相近时间的位姿，看作是该图像的真实采集位置。
    - TUM提供了 associate.py 程序，将其放入目录下执行即可得到记录彩色图像与深度图像匹配结果的 accelerometer.txt 文件，里面记录了彩色图像与深度图像的匹配关系。

### 动态数据集

研究动态 SALM 时用的是 TUM 的 Dynamic Objects 数据集（9个）以及 Validation Files 对应的部分，如下图所示：

<center><img src="https://cdn.jujimeizuo.cn/note/cv/dataset/dynadataset.png" alt="动态数据集"></center>

- fr2/desk_with_person 记录了一个人坐在办公桌前的典型办公室场景，在录制过程中，该人移动并与一些物体（屏幕、电话等）互动。
- 对于其他 8 个序列，sitting 类别的序列中两个人坐在办公桌前，交谈，并稍微打手势，序列旨在评估视觉 SLAM 和里程计算法对缓慢移动的动态对象的鲁棒性；walking 类别的序列中两个人走过一个办公室场景，旨在评估视觉 SLAM 在大部分可见场景中快速移动动态对象的鲁棒性。xyz，rpy，halfsphere，static 则对应了相机的移动方式。具体的 sitting 与 walking 数据集中的区别如下：

<center><img src="https://cdn.jujimeizuo.cn/note/cv/dataset/sitting_and_walking.png" alt="sitting and walking"></center>

相机运动轨迹的区别如下：

<center><img src="https://cdn.jujimeizuo.cn/note/cv/dataset/camera_track.png" alt="相机运动轨迹"></center>


### 数据集分析

对于动态环境下的SLAM问题，我们通常遵循以下两个准则来降低动态物体对定位精度的影响。

- 准则1：尽可能将运动的物体（区域）的去除。运动区域的特征点会引入一些错误的空间约束，极大的降低定位的精度及鲁棒性，因此对动态区域的容忍度是非常低的。
- 准则2：尽可能保留静态区域。如果场景中使用的特征点过少，也会间接降低定位的精度，所以在剔除动态区域的同时，尽量不要把静态点当做动态点去除掉。

在使用语义信息剔除动态区域的时候要考虑的问题：

1. 先验知识里静止的物体（比如椅子，书）可能是运动的，如果一个人推着椅子运动的话也需要将椅子区域的特征点进行剔除，否则定位时也会使用一些动态的不安全的特征点，即违背了准则1
2. 先验知识里移动的物体（比如人和汽车）可能是静止的，如果这些区域去掉的话，会因为静态点的减少而降低定位精度，即违反了准则2。
3. 一些物体可能是缓慢运动的。一些论文常常使用两帧之间计算外点，通过物体上外点的数量判断物体是否在移动，然而如果物体是在缓慢运动，那么很难在前后两帧图像之间通过外点的方式检测出来，即违背了准则1。
4. 一些物体可能是局部运动局部静止的。比如 TUM 数据集中 sitting 中的部分，人的大部分区域在静止的，但是有一小部分是动态的，不能将人作为一个整体进行运动判断，也就不能同时满足准则1与准则2。

针对TUM数据集，具体需要考虑的因素包括：

1. walking中移动的人
2. sitting中局部运动的人
3. 静止的人
4. 移动的椅子和书籍

