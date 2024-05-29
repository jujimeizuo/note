---
counter: true
comment: true
---

# KITTI 数据集

!!! abstract
    waymo提供了两种数据集，`motion` 与 `perception` 两种，其中 `motion` 是鸟瞰图，官网中有介绍，主要用于轨迹预测之类的任务，`perception` 主要用于目标检测跟踪之类的任务，是第一视角，有相机和雷达信息。

    Waymo包含 798 个训练场景、202 个验证场景和 150 个测试场景，每个场景的时长为 20 s。Waymo 数据集的标注频率比 nuScenes 高 5 倍，场景数量是 nuScenes 数据集的 3 倍，有数量更多且更密集的 2D/3D 标签。Waymo 数据集对自动驾驶算法的鲁棒性和泛化能力提出了更高的要求，是目前为止最大、最多样化的数据集。

    - paper: https://arxiv.org/abs/1912.04838v7
    - github: https://github.com/waymo-research/waymo-open-dataset
    - 主页：https://waymo.com/open

<center><img src="https://cdn.jujimeizuo.cn/note/cv/dataset/waymo-1.gif"></center>


## 数据集格式

### 结构

```text
data
├── waymo
│   ├── waymo_format
│   │   ├── training
│   │   ├── validation
│   │   ├── testing
│   │   ├── gt.bin
│   │   ├── cam_gt.bin
│   │   ├── fov_gt.bin
│   ├── kitti_format
│   │   ├── ImageSets
```

### Ground Truth Labels

数据集中对汽车、行人、交通标志、自行车人员进行了详细标注。对于激光雷达数据，将每一个物体标注为 7 自由度 3D bbox：(cx, cy, cz, l, w, h, θ)。其中cx, cy, cz 表示为 bbox 中心坐标，l, w, h 表示为物体长宽高，θ 表示为物体偏航角，此外对于每一个物体还标注了一个唯一的追踪 ID 编号。

图像标注中将每一个物体标注为4自由度2D bbox：(cx, cy, l, w)。其中cx, cy 表示为 bbox 中心图像坐标，l 表示为物体长度，w 表示为物体宽度。

此外，还将标注物体划分为了两个难度：LEVEL_2 为物体对应激光雷达点数少于 5 个，其余则划分为 LEVEL_1。

### Tasks

数据集任务划分为2D和3D物体检测和追踪任务，训练集场景有798个，验证集场景有202个，测试集场景有150个。

### Experiments

对于 3D 物体检测，Waymo 提供了一个 Baseline，其使用的检测方法是 PointPillars。对于 2D 物体检测，使用了 Faster R-CNN 作为 baseline，对于3D物体追踪，使用了 AB3DMOT 作为 Baseline。

## Waymo 转换 COCO 格式

- https://github.com/shinya7y/WaymoCOCO



## Reference

- [Waymo自动驾驶数据集介绍与使用教](https://blog.csdn.net/cg129054036/article/details/116138700)
- [Waymo数据集下载与使用](https://blog.csdn.net/pengxiang1998/article/details/136045762)
- [WAYMO 数据集](https://mmdetection3d.readthedocs.io/zh-cn/latest/advanced_guides/datasets/waymo.html)