# EndoNeRF

> [!abstract]
> EndoNeRF 数据集是专为“机器人柔性手术场景”设计的一套立体、单视角、动态 NeRF 训练/测试数据，由香港中文大学 Med-AIR 实验室在 MICCAI 2022 论文《Neural Rendering for Stereo 3D Reconstruction of Deformable Tissues in Robotic Surgery》中提出并开源 。数据集已广泛用于评估柔性组织 NeRF、4D 重建、手术导航等任务。
> - Paper: https://arxiv.org/abs/2206.15255
> - Github: https://github.com/med-air/EndoNeRF
> - Home: https://med-air.github.io/EndoNeRF/

## 数据集格式

| 项目 | 内容                                                                                        |
| ---- | ------------------------------------------------------------------------------------------- |
| 来源 | DaVinci 机器人前列腺切除术实录，术中截取 2 段典型操作片段                                   |
| 片段 | ① **pulling\_soft\_tissues**（拉扯软组织）<br>② **cutting\_tissues\_twice**（两次剪切组织） |
| 时长 | 4–8 s，15 fps                                                                               |
| 图像 | 640×512 立体 PNG（左、右目均提供，但默认仅使用左目做单视角 NeRF）                           |
| 附加 | ① 立体深度图（STTR-Light 估计）<br>② 手术器械二元掩码（人工标注）                           |
| 真值 | 无 3D mesh，以“图像+深度+掩码”作为监督，用 PSNR/SSIM/LPIPS 评估重建质量                     |

```text
pulling_soft_tissues/          # 或 cutting_tissues_twice
├── images/                    # RGB 图，000.png, 001.png …
├── depth/                     # 16-bit 深度 png，与图像同名
├── masks/                     # 器械掩码，0=器械/1=组织
└── pose_bounds.npy            # [N, 17] array，LLFF 格式
```

> [!Info] pose_bounds.npy
> 每行 17 维：
> [c2w(0:12), intrinsics(12:16), bound(16)]
> - `c2w`：3×4 相机到世界坐标系（这里全部设为单位阵，模拟固定内窥镜）
> - `intrinsics`：fx, fy, cx, cy（像素单位）
> - `bound`：场景边界（单位 m）

## 应用场景

1. 柔性动态 NeRF 训练：单视角 + 深度 + 掩码，训练可变形 NeRF（EndoNeRF、EndoSurf、LerPlane、4D-GS 等）。
2. 手术场景新视角合成：给定任意时刻 t，渲染无器械或器械被移除的“干净”视图，用于手术导航或教学。
3. 组织变形与深度补全：利用掩码排除器械干扰，仅对组织做深度监督，提升立体匹配精度。
4. 算法基准测试：文献中常用 PSNR、SSIM、LPIPS 以及训练/推理时间、GPU 占用作为量化指标，横向对比不同表示（NeRF、3D-GS、Plane 等）在手术动态场景下的表现 。