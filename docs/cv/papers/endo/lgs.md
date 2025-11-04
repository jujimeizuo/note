---
counter: true
comment: true
---

# LGS

> [!abstract]
> - paper：[:book: LGS: A Light-weight 4D Gaussian Splatting for Efficient Surgical Scene Reconstruction](https://arxiv.org/abs/2406.16073)
> - code：[:material-github: LGS](https://github.com/CUHK-AIM-Group/LGS)

## Introduction

> [!Question] 问题导向
> 高维度的 Gaussian 属性和高分辨率的形变场，导致严重的存储问题。

> [!Done] 解决方案
> - 为最大限度减少高斯数量的冗余，评估每个高斯对形变的影响，提出形变感知剪枝方法（DAP）；
> 为降低高斯属性的冗余，通过对高斯属性的维度进行剪枝，简化非关键区域的纹理和光照表示（GAP）；
> 通过 4D 特征场压缩，解决了用于动态场景建模的 4D 神经时空编码器因分辨率而导致的特征场冗余问题（FFC）；
> <center><img src="https://cdn.jsdelivr.net/gh/jujimeizuo/note@gh-pages/assets/images/cv/slam/lgs-1.jpg"></center>


## Method

### Deformation-Aware Pruning (DAP)

> [!Todo] DAP 目标
> **减少场景中冗余的 Gaussian 数量。**
> 
> 并非所有的 Gaussian 都对场景的形变建模有同等贡献。

- **Deformation Score**
    - 为每个 Gaussian 计算一个形变评分 $d_i$，反映了该 Gaussian 在所有时间戳上对像素的贡献以及其自身的形变程度；

    $$
    d_i = \sum_{t}^T \sum_{k}^{HW} \mathbb{1}(G(X_i), p_k, t) \cdot \Delta V(s_i),
    \Delta V(s_i) = \sum_t^T \| V(s_i) - V(s_i + \Delta s_i) \|_1
    $$

    - $\mathbb{1}(G(X_i), p_k, t)$ 表示 i-th Gaussian 在时间 t 对像素 k 的贡献度，$\Delta V(s_i)$ 表示 i-th Gaussian 的体积形变，通过缩放因子 $s_i$ 和形变 $\Delta s_i$ 计算体积的差。$V(s)=4\pi s_1s_2s_3/3$ 是 Gaussian 的体积计算公式。
    - 该分数表示，一个 Gaussian 对图像像素贡献越大，并且自身的体积形变越大，则它的形变评分越高，表明它对建模场景动态变化的重要性越高。

- **Gaussian**
    - stable Gaussian（SG）：$d_i \le h$；
    - deformed Gaussian（DG）：$d_i \gt h$；

- **Prune**
    - 分别对 SG 和 DG 分别进行剪枝，对每组 Gaussian 分别计算重要性得分：
        - SG 基于不透明度和归一化体积计算；
        - DG 基于原始体积及其形变计算；
    - $V_{norm}(s)=(V(s)/V_{max90})^\beta$ 为归一化的体积，$V_{max90}$ 为所有排序后的高斯分布中 90% 的最大体积。然后相应地修剪重要性得分较低的高斯分布。

$$
IS_i=\begin{cases}\sum_t^T\sum_k^{HW}\mathbb{1}(G(\boldsymbol{X}_i),\boldsymbol{p}_k,t)\cdot\sigma_i\cdot V_{norm}(\boldsymbol{s}_{\boldsymbol{i}}),\quad i\in SG\\\sum_t^T\sum_k^{HW}\mathbb{1}(G(\boldsymbol{X}_i),\boldsymbol{p}_k,t)\cdot\Delta V(\boldsymbol{s})\cdot V_{norm}(\boldsymbol{s}_{\boldsymbol{i}}),\quad i\in DG&&\end{cases}
$$

### Gaussian-Attribute Pruning (GAP)

> [!Todo] GAP 目标
> **减少每个 Gaussian 的属性维度，尤其是 SH 的维度。**
> 
> 内窥镜场景的纹理和光照相对简单，不需要高纬度的 SH 系数来表示，通过移除高阶的 SH 系数，从而减少每个 Gaussian 的内存占用。

- **SH Prune**
    - SH 包含 48 个浮点值，占每个高斯所有属性的 80% 以上，因此GAP 减少用于建模视角相关颜色和场景反射的高阶 SH；
    - 使用一个阈值 $h_{sh}$ 表示 SH 的剪枝程度，$\alpha_{ic} = \alpha_{ic} * \mathbb{1}(c \le (h_{sh} + 1)^2 + N_{RGB}), c \in C$；

- **Knowledge Distillation**：为弥补剪枝带来的信息损失，LGS 使用知识蒸馏技术。将为压缩的、训练良好的模型作为 teacher model，经过 DAP、GAP 和 FFC 处理后的模型作为 student model，通过最小化二者渲染图像之间的差异，将知识从 teacher 传递给 student，损失函数如下：
    - $L = L_d + L_r$
    - 蒸馏损失：$L_d = \frac{1}{T} \sum_t^T \| \hat{I}_{tch}(t) - \hat{I}_{stu}(t) \|_2$
    - 渲染损失：$L_r = \frac{1}{T} \sum_t^T \| I_{gt}(t) - \hat{I}_{stu}(t) \|_2$

### Feature Field Condensation (FFC)

> [!Todo] FFC 目标
> **减少用于建模动态场景的 4D 特征场的内存占用。**
> 
> FFC 通过对特征场进行自适应池化来减少其分辨率。

- 考虑到相邻的 Gaussian 通常共享相似的空间和时间信息，这意味着同一体素平面上的相邻值也应该相似，FCC 对 4D 特征场的各个子平面进行 3D 自适应池化：

$$
E_{\Phi}^{\prime}(i,j)=\frac{1}{r_{\Phi_1}r_{\Phi_2}}\sum_{i^{\prime}=i\cdot r_{\Phi_1}}^{(i+1)\cdot r_{\Phi_1}}\sum_{j^{\prime}=j\cdot r_{\Phi_2}}^{(j+1)\cdot r_{\Phi_2}}E_{\Phi}(i^{\prime},j^{\prime})
$$


## Experiments


## Reference

- [[论文审查] LGS: A Light-weight 4D Gaussian Splatting for Efficient Surgical Scene Reconstruction](https://www.themoonlight.io/zh/review/lgs-a-light-weight-4d-gaussian-splatting-for-efficient-surgical-scene-reconstruction)