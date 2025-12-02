# StereoMIS

> [!abstract]
> StereoMIS是一个用于内窥镜手术中同步定位与地图构建（SLAM）的数据集。该数据集是使用达芬奇Xi手术机器人录制的，捕捉了立体视频流和相机前向运动学数据。它包含3个在体猪实验对象，以及11个包含呼吸、工具运动和组织变形的手术序列。
>
> - Paper: https://arxiv.org/abs/2304.08023
> - Github: https://github.com/aimi-lab/robust-pose-estimator
> - Home: https://zenodo.org/records/7727692

## 数据集格式

- 采集平台：da Vinci Xi 立体内窥镜，左-右目垂直拼接为单路 1920×1080 30-60 fps 视频
- 实验对象：3 只活体猪（P1、P2、P3），共 11 条序列，时长 52 s – 5 min 不等
- 挑战性元素：呼吸运动、器械遮挡、组织切割/缝合、出血与烟雾等真实术中动态
- 已公开部分：仅猪实验序列（in-vivo porcine）向学术社区开放，人类手术片段未放出

```text
sequence_name/  
├── stereo_video.avi          // 上下拼接的立体内窥镜视频  
├── left_mask/                // 自动生成的器械二值掩码（左目，PNG）  
├── kinematics.csv            // 机器人前向运动学（时间戳 → 器械关节角）  
├── start_stop.csv            // 有效帧起止编号，便于裁剪  
└── calib/                    // 内参、外参与畸变系数（YAML/txt）
```


## 应用场景

1. 内窥镜 SLAM/视觉里程计：评估在呼吸、组织变形和器械遮挡下的相机跟踪鲁棒性；多篇最新方法（如学习-几何混合 VO、自适应加权 VO）在此数据集上取得 SOTA ATE ≈ 2.2 mm。
2. 动态场景 NeRF/3D 重建：利用左目视频+掩码训练可变形 NeRF（EndoNeRF、4D-GS、FLEx 等），实现“去器械”或“时变组织”新视角合成；FLEx 在 5000 帧长序列上仍保持 29.97 PSNR。
3. 在线组织跟踪与器械分割：地标子集提供 2D-3D 对应，可用于验证特征跟踪、模板匹配或深度强化学习策略。
4. 深度估计与立体匹配：双目帧+真值轨迹为无监督/自监督深度网络提供尺度一致的监督信号，多篇内窥镜深度补全工作以 StereoMIS 为测试床。