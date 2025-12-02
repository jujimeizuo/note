# SCARED

> [!abstract]
> SCARED（Stereo Correspondence and Reconstruction of Endoscopic Data）是 2019 年 MICCAI EndoVis Sub-Challenge 发布的立体内窥镜数据集，主打“高精度结构光深度 + 双目帧”组合，用于在体内微创手术环境下评估深度估计、立体匹配与三维重建算法。
>
> - Paper: https://arxiv.org/abs/2101.01133
> - Github：https://github.com/EikoLoki/MICCAI_challenge_preprocess
> - Home: https://endovissub2019-scared.grand-challenge.org/Home/


## 数据集格式

- 采集平台：da Vinci Xi 立体内窥镜（1280×1024，30 fps）
- 实验对象：3 只活体猪，腹部腔内 5 段连续视频（keyframe_1~5）
- 标注方式：
    - 结构光投影仪瞬时投射编码图案，每段视频仅 1 帧被照射作为 key-frame；
    - 利用三角测量生成 key-frame 的亚毫米级稠密深度图（≈ 0.3 mm RMS）；
    - 其余帧通过“帧间相机位姿 + 深度 Warp”扩充，最终得到 822 对双目图 + 稠密视差真值（训练 7 组，测试 2 组）。
- 数据量：≈ 280 GB，TIFF/PNG/MP4 混合存储

```text
SCARED/
├── dataset_1/
│   ├── keyframe_1/
│   │   ├── data/
│   │   │   ├── scene_points.tar.gz # 逐帧 Warp 后的稠密顶点图（tiff，无效像素=0,0,0）
│   │   │   ├── rgb.mp4 # 上下拼接立体内窥镜视频（左目在上，右目在下）
│   │   │   └── frame_data.tar.gz # 每帧相机 4×4 外参（json，命名 frame_data%06d.json）
│   │   ├── right_depth_map.tiff # 右目稠密深度（32FC3，单位 mm；第三通道为有效深度)
│   │   ├── left_depth_map.tiff # 左目稠密深度（32FC3，单位 mm；第三通道为有效深度）
│   │   ├── point_cloud.obj # key-frame 点云（可直接 MeshLab 查看）
│   │   ├── Left_Image.png # 左目 key-frame 彩色图
│   │   ├── Right_Image.png # 右目 key-frame 彩色图
│   │   └── endoscope_calibration.yaml # 双目内参、外参（OpenCV FileStorage 格式）
│   ├── keyframe_2/
│   │   └── [similar structure as keyframe_1]
│   ├── keyframe_3/
│   │   └── [similar structure as keyframe_1]
│   ├── keyframe_4/
│   │   └── [similar structure as keyframe_1]
│   └── keyframe_5/
│       └── [similar structure as keyframe_1]
```

## 应用场景

| 任务                 | 常用设置                                                   | 指标                |
| -------------------- | ---------------------------------------------------------- | ------------------- |
| 立体匹配/深度估计    | 以左图为输入，预测视差或深度                               | D1-error、RMSE、MAE |
| 自监督深度补全       | 利用 rgb.mp4 序列 + key-frame 深度做时空一致性损失         | Abs-Rel、Sq-Rel     |
| 内窥镜 SLAM/位姿跟踪 | 用 frame\_data 真值评估轨迹                                | ATE、RPE            |
| 三维重建与可视化     | 将 point\_cloud.obj 或稠密 tiff 导入 MeshLab、CloudCompare | 完整度/精度         |



## Reference

- [SCARED数据集介绍](https://zhuanlan.zhihu.com/p/2167155586)