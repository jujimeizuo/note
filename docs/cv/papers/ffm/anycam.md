---
counter: true
comment: true
---

# AnyCam

> [!abstract]
> - paper：[:book: AnyCam: Learning to Recover Camera Poses and Intrinsics from Casual Videos](https://arxiv.org/abs/2503.23282)
> - code：[:material-github: AnyCam](https://github.com/Brummi/anycam)

## Introduction

> [!Question] 问题导向
> 传统 SfM 和 SLAM 在处理任意动态视频数据时困难，通常需要已知的相机内参或 test-time 优化。如何解决在处理动态场景和无标签视频时的局限性。

> [!Done] 解决方案
> 1. 采用 Transformer 架构提取深度和光流等特征，端到端地学习视频帧序列的相对相机位姿和内参；
> 2. 采用不确定性建模，可以处理原始视频且无标签，自动过滤动态物体；
> 3. 提出一个轻量级的测试时轨迹优化方法，以避免长期漂移。
> <center><img src="/assets/images/cv/slam/AnyCam-1.jpg"></center>
> <center><img src="/assets/images/cv/slam/AnyCam-2.jpg"></center>


## Method

### Transformer for Camera Prediction

- **Backbone**：使用一个预训练的 Backbone，输入为视频帧、预训练的深度信息和光流信息；
- **Transformer Encoder**：提取到的特征被送入 Encoder，利用 Self-Attention 学习视频帧之间的关系；
- **Pose Prediction Head（HP）**：预测每一帧相对位姿；
- **Uncertainty Prediction Head（Hσ）**：预测不确定性图，表示每个像素的动态可能性；
- **Intrinsics Prediction Head（Hseq）**：预测相机内参，首先采用多个候选焦距值，然后训练多个 HP 和 Hσ，输出最大似然度对应的值。


### Dynamics-aware Pose Training

- **Uncertainty-aware flow loss**
    - 利用预测的位姿和深度图，得到投影的“induced optical flow”；
    - 比较“induced optical flow”和真实光流，且使用不确定性图 $\sigma$ 对损失加权；

    $$
    \mathcal{L}_f^{\sigma\mathbf{F}^{i\to j}}=-\frac{1}{|\Omega|}\sum_{uv\in\Omega}\ln\frac{1}{\sqrt{2}\sigma_{f,uv}^i}\exp-\frac{\sqrt{2}\ell_{f,uv}^{\mathbf{F}^{i\to j}}}{\sigma_{f,uv}^i}
    $$

- **Pose Consistency Loss**
    - 为保证时间上的一致性，预测相机位姿时考虑整个序列的上下文（某些帧的光流预测不准确，或动态物体会遮挡相关的静态部分），所以引入一个额外的损失项和 dropout 训练策略。
    - 序列反转，要求正向预测的位姿和反向预测的位姿互为逆变换，强制位姿一致性；

$$
\mathcal{L}_f^{\uparrow\downarrow}=\sum_{i=1}^{n-1}\left\|\left(\mathbf{P}_f^{i\to i+1}\right)^{-1}\mathbf{P}_f^{i+1\to i}-\mathbf{I}_4\right\|_{1,1}
$$

- **Intrinsics Loss（Lintr）**
    - 为了选择最佳焦距值，训练 Hseq 来预测哪些焦距候选值会产生最低的光流损失；
    - 使用 KL 散度衡量预测的可能性和基于 flow loss 计算目标概率的差距；

$$
\mathcal{L}^{Intr}=\mathbf{KL}_{\mathrm{div}}\left(\mathcal{P},\mathrm{softmax}(-\mathcal{L}_{f_1}^{\sigma\mathbf{F}},\ldots,-\mathcal{L}_{f_m}^{\sigma\mathbf{F}})\right)
$$

- **Final Loss**

$$
\mathcal{L}=\sum_{k=1}^m\left(\lambda_{\sigma\mathbf{F}}\mathcal{L}_{f_k}^{\sigma\mathbf{F}}+\lambda_{\uparrow\downarrow}\mathcal{L}_{f_k}^{\uparrow\downarrow}\right)+\lambda_\mathrm{Intr}{\mathcal{L}}^{Intr}
$$

### Test-time Refinement

- 为了减少长时间运动中积累的漂移：
    - 特征跟踪：在视频帧中提取一些特征点，并使用光流跟踪这些点在后续帧中的位置；
    - BA：优化相机位姿和特征点的位置（需要用不确定性图作为权重）；
    - 滑动窗口优化：每次只优化一个窗口内的帧，然后滑动到下一个位置。

## Experiments


## Reference

- [[论文审查] AnyCam: Learning to Recover Camera Poses and Intrinsics from Casual Videos](https://www.themoonlight.io/zh/review/anycam-learning-to-recover-camera-poses-and-intrinsics-from-casual-videos)
- [https://fwmb.github.io/anycam/](https://fwmb.github.io/anycam/)