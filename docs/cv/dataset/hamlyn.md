# SCARED

> [!abstract]
> Hamlyn Centre腹腔镜/内窥镜视频数据集由英国帝国理工学院Hamlyn Centre制作，包含丰富的腹腔镜和内窥镜视频数据。这些数据集记录了各种复杂的手术场景，包括猪膈肌解剖、肺叶切除、TECAB手术等，涵盖组织变形、呼吸和心跳引起的运动、烟雾模糊、工具与组织的交互等多种视觉挑战。数据集共包含38个视频和子数据集，为研究人员提供了高质量的真实手术视频资源。
> - Paper：https://arxiv.org/abs/2103.16525
> - Github：https://github.com/UZ-SLAMLab/Endo-Depth-and-Motion
> - Home:
>       - https://davidrecasens.github.io/EndoDepthAndMotion/
>       - https://hamlyn.doc.ic.ac.uk/vision/
>       - https://huggingface.co/datasets/vslamlab/Hamlyn_Rectified_Dataset


## 数据集格式

| 项目         | 说明                                                                            |
| ------------ | ------------------------------------------------------------------------------- |
| **采集平台** | 立体内窥镜（早期为 384×192，后期提供 1280×1024 的 rectified 序列）              |
| **模态**     | 双目光学 + 部分序列附带结构光/立体匹配深度                                      |
| **总量**     | 38 条视频子集，约 32 400 对双目帧（低分辨率子集）                               |
| **场景**     | 猪腹腔、膈肌解剖、肺叶切除、TECAB 等，含呼吸/心跳形变、器械遮挡、烟雾模糊等挑战 |
| **帧率**     | 25–30 fps，时长 30 s–5 min 不等                                                 |

- 原始发布（低分辨率）

```text
hamlyn_lowres/
├── left/               # 左目 png，384×192
├── right/              # 右目 png，384×192
└── calibration.txt     # 简易双目内参、基线
```

- 后期 Rectified + 深度版（高分辨率，1280x1024）

```text
sequence_name/
├── left_rect/          # 左目 rectified jpg
├── right_rect/         # 右目 rectified jpg
├── left_depth/         # 16-bit png，深度单位 mm（Libelas 立体匹配生成）[^58^]
├── camera_calib.yaml   # OpenCV 格式：K1, K2, D1, D2, R, T
└── times.txt           # 时间戳（秒）
```


## 应用场景

| 任务                     | 用法与指标                                                                                 |
| ------------------------ | ------------------------------------------------------------------------------------------ |
| **单目/自监督深度估计**  | 利用左目视频 + 相邻帧重建损失，评估 Abs-Rel、RMSE；Hamlyn 纹理弱、形变大，被当作“hard”基准 |
| **立体重建与视差估计**   | 以 Libelas 深度为 GT，训练端到端立体网络，测 D1-error、EPE                                 |
| **内窥镜 SLAM / 里程计** | 序列 20（缓慢形变腹腔）、21（双叶肝脏独立运动）最常用；报告 ATE、RPE，无需尺度对齐         |
| **组织变形跟踪**         | 利用双目深度真值验证可变形 SLAM（SD-DefSLAM、DSDT 等），Hamlyn 提供**体内大形变**真实案例  |
| **烟雾检测与去除**       | 原始图像 + Blender 合成烟雾，训练 U-Net、CBAM、GAN 等去雾网络，测 PSNR/SSIM≥31 dB/0.98     |
| **三维立体显示**         | 左目图 + 预测视差 → 生成右目图，红蓝 3D 眼镜可视化，用于术中立体导航                       |


## Reference

- [Hamlyn Endoscopic Video Datasets 数据集介绍](https://zhuanlan.zhihu.com/p/3483571403)