---
counter: true
comment: true
---

# MASt3R

> [!abstract]
> - paper：[:book: Grounding Image Matching in 3D with MASt3R](https://arxiv.org/abs/2406.09756)
> - code：[:material-github: mast3r](https://github.com/naver/mast3r)

## Introduction

> [!Question] 问题导向
> 图像匹配是所有 3D 视觉领域中性能最佳算法和流程核心组成部分。尽管匹配本质上是一个 3D 问题，与相机位姿和场景几何形状息息相关，但它通常被当做 2D 问题处理。因为匹配的目标是在 2D 像素场之间建立对应关系。

> [!Done] 解决方案
> MASt3R 在 DUSt3R 的基础上，提高匹配能力。在 DUSt3R 前额外加一个 network 输出稠密的 local features，并添加 matching loss 来训练。最后引入一种快速相互匹配方案，能够将匹配速度提高几个数量级。

## Method

### MASt3R Matching

<center><img src="https://cdn.jsdelivr.net/gh/jujimeizuo/note@gh-pages/assets/images/cv/slam/mast3r-1.png"></center>

- matching 的网络结构和 DUSt3R 基本一致，蓝色的部分是新增的模块。比较明显的是新增了一个 head 用来提取 local features。然后多了两个最近邻匹配模块用来构建匹配。
- 对于 loss，对 DUSt3R 的 $\mathcal{l}_{\mathrm{regr~}}$ 做了修改，然后新增了匹配 loss。
    - MASt3R matching 取消了不同的深度正则化项，直接用 gt 的平均深度。

    $$
    \mathcal{l}_{\mathrm{regr~}}(j, i) = \frac{\bar{X}_i^j - X_i^j}{\bar{z}} \\
    \mathcal{L}_{\mathrm{conf~}} = \sum_{v \in \{1, 2\}} \sum_{i \in D^v} C_i^v \mathcal{l}_{\mathrm{regr~}}(v, i) - \alpha \log C_i^v
    $$

    - 因为新增了一个用于匹配的 head 输出，希望每个像素点最多和另一张图的一个像素点匹配，这部分称为 infoNCE loss，假设 gt 的匹配点为 $\hat{\mathcal{M}} = \{ (i, j) | \hat{X}_i^{1,1} = \hat{X}_j^{2, 1} \}$，并记 $D_i^v$ 为 $HEAD_{desc}^v$ 的输出为

    $$
    \mathcal{L}_{\mathrm{match~}}=-\sum_{(i,j)\in\hat{\mathcal{M}}}(\log\frac{s_\tau(i,j)}{\sum_{k\in\mathcal{P}_1}s_\tau(k,j)}+\log\frac{s_\tau(i,j)}{\sum_{k\in\mathcal{P}_2}s_\tau(i,k)}) \\
    s_\tau(i,j)=exp[-\tau {D_i^1}^\top D_j^2],\mathcal{P}^1=\{i|(i,j)\in\hat{\mathcal{M}}\},\mathcal{P}^2=\{j|(i,j)\in\hat{\mathcal{M}}\}
    $$

    - 这里的 s 是一个相似性度量，表示图像 1 中第 i 个描述符和图像 2 中第 j 个描述符的相似性。D 是描述符的特征向量，$\tau$ 是温度超参数，控制相似性分布的平滑程度。
    - 最终的 loss 为 $\mathcal{L}_{total} = \mathcal{L}_{\mathrm{conf~}} + \beta \mathcal{L}_{\mathrm{match~}}$
- 有了 Model 和 Loss 就可以训练，但是网络只输出 PointMap 和每个像素的 LocalFeature，而期望得到两个图像之间的像素点级别的匹配，匹配的部分就是新增的 NN 模块。
- 匹配：
    - 先对两个图像对应的特征点进行降采样，先得到图像 1 的特征点对于图像 2 的正向 NN 匹配，在从已经匹配上的图像 2 特征点反向 NN 匹配到图像 1，能够形成闭环的 NN 匹配关系便成为最终的匹配。**一次迭代同时包含正向和反向 NN 匹配，这样可以快速收敛。**
    - 优化：降采样之后的最近邻不一定是真的最近邻，所以要回到原分辨率的图像上，重新分块再来一遍匹配（无论是分块还是降采样肯定都比直接全局NN快得多）。

<center><img src="https://cdn.jsdelivr.net/gh/jujimeizuo/note@gh-pages/assets/images/cv/slam/mast3r-2.png"></center>

### MASt3R SfM

<center><img src="https://cdn.jsdelivr.net/gh/jujimeizuo/note@gh-pages/assets/images/cv/slam/mast3r-3.png"></center>

- MASt3R SfM 在 pipeline 里集成了多帧输入，但是一次只能处理两张图片，MASt3R SfM 基于 MASt3R matching，只用到了 encoder 的输出作为 tokenFeature（不是 head 输出的 LocalFeature），而不需要像素级别的匹配关系。
- 类似于 DUSt3R，先基于重叠视角构建一个 Graph：
    - 根据 encoder 输出的 tokenFeature，使用 FPS 来选出 N 个关键帧，然后两两相连，构成 $N^2$ 条边。
    - 剩余的普通帧连接到最近的关键帧上，还会通过 NN 连接到最近的 k 个普通帧上。
- 计算特征的距离完全基于 tokenFeature，对于 tokenFeature 白化后计算二进制距离来实现，而一个图像不止一个特征，所以采用 ASMK 算法计算相似度来描述两张图像重叠视野。
- 使用 encoder 输出而不是 head 输出作为 feature，是因为 encoder 的输入只要一张图像，每个图像都过一遍 encoder，且不可缺少，所以提取特征没有开销。
- 构建 pair 时用 encoder 输出作为 tokenFeature，后续的匹配和优化使用 head 输出的 LocalFeature。
- **匹配与标准点图、BA 优化**

## Experiments

<center><img src="https://cdn.jsdelivr.net/gh/jujimeizuo/note@gh-pages/assets/images/cv/slam/mast3r-3.png"></center>

## Reference

- [MASt3R 落地 3D 的图像匹配](https://blog.csdn.net/yorkhunter/article/details/141274989)
- [论文阅读笔记之《MASt3R-SLAM: Real-Time Dense SLAM with 3D Reconstruction Priors》](https://kwanwaipang.github.io/File/Blogs/Poster/MASt3R-SLAM.html#dust3r:-geometric-3d-vision-made-easy)
- [DUSt3R和MASt3R论文解析](https://zhuanlan.zhihu.com/p/28169401009)
- [Mast3R代码解读](https://blog.csdn.net/xxxrc5/article/details/144712597)