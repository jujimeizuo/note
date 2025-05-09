---
counter: true
comment: true
---

# COLMAP

> [!abstract]
> - COLMAP 是一种通用的运动结构(SfM) 和多视图立体(MVS) 管道，具有图形和命令行界面。
> - 以下的实验环境：Ubuntu 20.04（宿主机 ）、Docker 11.8.0-cudnn8-devel-ubuntu22.04（镜像）、CUDA 11.8


## Installation

### Dependencies

```bash
sudo apt-get install \
    git \
    cmake \
    ninja-build \
    build-essential \
    libboost-program-options-dev \
    libboost-filesystem-dev \
    libboost-graph-dev \
    libboost-system-dev \
    libeigen3-dev \
    libflann-dev \
    libfreeimage-dev \
    libmetis-dev \
    libgoogle-glog-dev \
    libgtest-dev \
    libgmock-dev \
    libsqlite3-dev \
    libglew-dev \
    qtbase5-dev \
    libqt5opengl5-dev \
    libcgal-dev \
    libceres-dev
```

> [!tip] 支持 CUDA（宿主机里），docker run 的参数添加 --gpus
>
> ```bash
> sudo apt-get install -y \
>    nvidia-cuda-toolkit \
>   nvidia-cuda-toolkit-gcc
> ```


### Configure and Compile

```bash
git clone https://github.com/colmap/colmap.git
cd colmap
mkdir build
cd build
cmake .. -GNinja
ninja
sudo ninja install
```

> [!error] nvcc fatal : unsupported gpu architecture ‘compute_native’
> ```text
> # 在 colmap/cmake/FindDependencies.cmake 中添加一句 `set(CMAKE_CUDA_ARCHITECTURES "80")`，如下所示：
> set(CMAKE_CUDA_ARCHITECTURES "80")
> if(CUDA_ENABLED AND CUDA_FOUND)
>     if(NOT DEFINED CMAKE_CUDA_ARCHITECTURES)
>         set(CMAKE_CUDA_ARCHITECTURES "native")
>     endif()
> ```

## Experiment

- 启动 `COLMAP`

```bash
colmap gui
```

<center><img src="https://note.jujimeizuo.cn/assets/images/cv/utils/colmap-1.jpg"></center>

- 点击 `Reconstruction > Automatic Reconstruction` 进行一系列基本设置后，输出的结果会写在 `workspace folder` 中（如果图像在 `path/to/project/images` 中，那么就应该选择 `path/to/project` 作为`workspace`）

<center><img src="https://note.jujimeizuo.cn/assets/images/cv/utils/colmap-2.jpg"></center>

- 运行 `Automatic Reconstruction` 后，文件夹生成为

```text
+── images
│   +── image1.jpg
│   +── image2.jpg
│   +── ...
+── sparse
│   +── 0
│   │   +── cameras.bin
│   │   +── images.bin
│   │   +── points3D.bin
│   +── ...
+── dense
│   +── 0
│   │   +── images
│   │   +── sparse
│   │   +── stereo
│   │   +── fused.ply
│   │   +── meshed-poisson.ply
│   │   +── meshed-delaunay.ply
│   +── ...
+── database.db
```

> [!info] 文件夹作用
> - `path/to/project/sparse`：重建得到的稀疏模型
> - `path/to/project/dense`：重建得到的稠密模型
> - `fused.ply`：可以加载到 COLMAP 图形界面，从 `File > Import model from ...`
> - 稠密的网格只能用外部查看器（`MeshLab`）可视化


> [!question] 生成的文件夹不能直接用于 `NGP` 或 `3DGS`
> > [!success]- 3DGS
> > 在 `3DGS` 中，有脚本转换
> > ```bash
> > python convert.py -s location [--resize] #If not resizing, ImageMagick is not needed
> > ```
> >
> > 将图片打包成如下再执行脚本
> > ```text
> > location
> > |---input
> >    |---<image 0>
> >    |---<image 1>
> >    |---...
> > ```
> >
> > 如果是视频，先用 `ffmpeg` 抽帧
> > ```bash
> > ffmpeg -i ./data/data_classroom/classroom.mov -qscale:v 1 -qmin 1 -vf fps=8 /path/to/data/input/%04d.jpg
> > ```
> ---
> > [!success]- instant-NGP
> > 在 `instant-NGP` 中，有脚本转换
> > ```bash
> > python scripts\colmap2nerf.py --video_in [mp4]  --run_colmap --colmap_db data\data_classroom\colmap.db --text data\data_classroom\text_colmap   --aabb_scale 16 --out data\data_classroom\transforms.json  --colmap_matcher exhaustive  --video_fps 8
> > ```

## Picture Capture Process

- 拍摄的图片应具有丰富的纹理。最好避免纹理特别少的图片如一张白墙或空桌图片。通过加入一些物品来丰富纹理
- 具备相似的光照情况。避免 `high dynamic range scenes`（如有太阳有影子，穿过门或窗拍摄）。避免镜面反射
- 具有高度视觉重叠的图片。确保一个物体至少有三张图片，尽量多一点
- 多视图拍摄。不要通过平移旋转相机来从同一个方向拍摄。但确保相似视角有少且精的图片，并不是越多越好。如果是视频，请减少帧率。



## Reference

- [Installation — COLMAP 3.11.0.dev0 documentation](https://colmap.github.io/install.html)
- [实验笔记之——Linux实现COLMAP\_linux colmap-CSDN博客](https://blog.csdn.net/gwplovekimi/article/details/135389922)
- [ColMap使用 | 悠闲の小屋](https://keepjolly.com/archives/colmap-use/)
- [三维重建instant-ngp环境部署与colmap、ffmpeg的脚本参数使用 - lefree - 博客园](https://www.cnblogs.com/lefree/articles/17055075.html)