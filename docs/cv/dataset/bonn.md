# Bonn

> [!abstract]
> - 动态序列：共 24 个动态序列，场景中包含人物执行各种任务，如搬运箱子、玩气球等；
> - 静态序列：额外提供 2 个静态序列 用于对比实验；
> - 图像分辨率：所有 RGB 和深度图像分辨率均为 640×480；
> - 采集设备：使用 Microsoft Kinect 相机采集 RGB-D 数据；
> - 相机位姿真值：通过 Optitrack Prime 13 运动捕捉系统记录；
> - 静态环境点云真值：使用 Leica BLK360 地面激光扫描仪获取，提供完整点云（约 3.94 亿点）和下采样版本（约 5,468 万点），格式为 PLY ASCII。
> 
> - Paper: https://arxiv.org/abs/1905.02082
> - Github: https://github.com/PRBonn/refusion
> - Home: https://www.ipb.uni-bonn.de/data/rgbd-dynamic-dataset/index.html


## 数据集格式

数据集遵循TUM RGB-D数据集的格式。每个序列包含以下文件：

```text
sequence_name/
├── rgb/               # RGB 图像（PNG 格式，640×480）
├── depth/             # 深度图像（PNG 格式，16位，单位毫米）
├── accelerometer.txt  # 加速度计数据（部分序列）
├── groundtruth.txt    # 相机位姿真值（时间戳 + 平移 + 四元数）
```

## 应用场景

- 动态 SLAM 算法评估；
- 动态物体检测与分割；
- 深度估计与重建；
- 语义 SLAM 与运动一致性分析。