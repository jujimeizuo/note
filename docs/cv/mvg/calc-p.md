---
counter: true
comment: true
---

# 计算摄像机矩阵 p

!!! abstract
    本章主要讨论由 3 维空间与图像平面元素间的对应来估计摄像机投影矩阵的数值方法（简称确定摄像机参数）

## 基本方程

- 对于每组对应$\mathbf{X}_i \leftrightarrow \mathbf{x}_i$，可以得出下面关系式：

$$
\begin{bmatrix}
\mathbf{0}^\top & -w_i\mathbf{X}_i^\top & y_i\mathbf{X}_i^\top \\
w_i\mathbf{X}_i^\top & \mathbf{0}^\top & -x_i\mathbf{X}_i^\top
\end{bmatrix}
\begin{bmatrix}
\mathbf{p}_1 \\
\mathbf{p}_2 \\
\mathbf{p}_3
\end{bmatrix}
=
\mathbf{0}
$$

- **最小配置解**：矩阵 P 有 12 个元素和（忽略缩放因子）11 个自由度，所以解 P 需要 11 个方程。给定这个最小数目的对应时，解时精确的，即空间的点准确地投影到它们被测量到图像上
- **超定解**：如果由于点坐标的噪声导致数据不精确并且给定$n \ge 6$组点对应，那么$A\mathbf{p}=\mathbf{0}$将不存在精确解。P 的解可以通过最小化一个代数或几何误差来获得。求$\parallel A \mathbf{p} \parallel$的最小值，可能的约束是：
    - $\parallel \mathbf{p} \parallel = 1$
    - $\parallel \hat{\mathbf{p}}^3 \parallel = 1$，其中$\hat{\mathbf{p}}^3$是由 P 最后一行的前三个元素组成的矢量$(p_{31},p_{32},p_{33})^\top$
- **退化配置**
    - 摄像机中心和点都在一条三次绕线上
    - 这些点都在一张平面和包含摄像机中心的一条直线的并集上
- **数据归一化**：当点到摄像机的深度变化相对比较小时，采用同样类型的归一化。因此，把点的形心平移到原点，并对它们的坐标进行缩放使它们到原点的 RMS（均方根）距离等于$\sqrt{3}$。适用于点紧致分布的情形
- **直线对应**：3D 中的直线可以用它通过的两点$\mathbf{X}_0$和$\mathbf{X}_1$来表示。由图像直线$\mathbf{l}$反向投影得到的平面为$P^\top\mathbf{l}$。那么点$\mathbf{X}_j$在该平面上的条件是$\mathbf{l}^\top P \mathbf{X}_j = 0$，其中$j=0,1$

## 几何误差

- **图像中的几何误差**
    - $\underset{i}{\sum}d(\mathbf{x}_i,\hat{\mathbf{x}}_i)^2$，其中$\mathbf{x}_i$是被测量的点，$\hat{\mathbf{x}}_i$是点$P\mathbf{X}_i$，即$\mathbf{X}_i$在$P$作用下的精确的图像点
    - 如果测量误差满足高斯分布，那么$\underset{P}{\min}\underset{i}{\sum}d(\mathbf{x}_i,P\mathbf{X}_i)^2$的解是$P$的最大似然估计
- **世界点有误差**
    - 3D 几何误差定义为：$\underset{i}{\sum}d(\mathbf{X}_i,\hat{\mathbf{X}}_i)^2$
    - 如果世界和图像点的误差都考虑：$\underset{i=1}{\sum}d_{Mah}(\mathbf{x}_i,P\hat{\mathbf{X}}_i)^2+d_{Mah}(\mathbf{X}+\hat{\mathbf{X}}_i)^2$，$d_{Mah}$表示误差协方差矩阵的 Mahalanobis 距离

### 代数误差的集合解释

- 假定所有的点$\mathbf{X}_i$在 DLT 算法中已经归一化，DLT 算法要最小化的量是：$\sum_{i}(\hat{w}_id(\mathbf{x}_i,\hat{\mathbf{x}}_i))^2$，其中$\hat{w}(\hat{x}_i,\hat{y}_i,1)^\top=P\mathbf{X}_i$，$\hat{w}$可以解释成点$\mathbf{X}_i$沿主轴方向到摄像机的深度，要最小化的代数误差等于$f\sum_id(\mathbf{X}_i,\hat{\mathbf{X}}_i)^2$
- **变换不变性**：在约束$\parallel \hat{\mathbf{p}}^3 \parallel = 1$下最小化$A\mathbf{p}$可以解释成最小化 3D 几何距离。这样既不受 3D 空间也不受图像空间的相似变换的影响

### 仿射摄像机的估计

- 上面有关射影摄像机推导的方法可以直接用于仿射摄像机。仿射摄像机定义为射影矩阵的最后一行是$(0,0,0,1)$的摄像机。仿射摄像机的 DLT 估计是在$P$的最后一行满足上述条件下最小化$\parallel A \mathbf{p} \parallel$


## 受限摄像机估计

- 在关于摄像机参数的限制条件下寻求一个最适配的摄像机矩阵$P$，通常的限制有
    - 扭曲$s$为 0
    - 像素是正方形:$\alpha_x=\alpha_y$
    - 主点$(x_0,y_0)^2$已知
    - 整个摄像机标定矩阵$K$已知
- **最小化几何误差**：假定我们强调约束$s=0$和$\alpha_x=\alpha_y$，用余下的 9 个参数来参数化摄像机矩阵。几何误差可以用迭代最小化方法相对于这组参数来最小化
- **最小化代数误差**：考虑把参数集$\mathbf{q}$映射到摄像机矩阵$P$的参数化映射$g$，最小化所有点匹配的代数误差等价于最小化$\parallel Ag(\mathbf{q}) \parallel$
- **简化的测量矩阵**：一般，$2n \times 12$的矩阵$A$可能有很多行。但可用一个$12 \times 12$的矩阵$\hat{A}$来代替$A$，使得对任何矢量$\mathbf{p}$有$\parallel A \mathbf{p} \parallel = \mathbf{p}^\top A^\top A \mathbf{p} = \parallel \hat{A} \mathbf{p} \parallel$
- **初始化**：求摄像机初始化参数的一种途径：
    - 用诸如 DLT 的线性算法求出一个初始的摄像机矩阵
    - 把固定参数强制到所希望的取值范围
    - 把摄像机矩阵分解所获得的初始值赋给参数变量
- **外部校准**：为了计算外部校准，需对世界坐标位置准确已知的一个配置进行影像。之后求摄像机的姿态。在机器人系统的手眼标定中求摄像机位置就是这样的情形；还有在采用配准技术的基于模型的识别中，需要知道物体相对摄像机的位置
- **协方差估计**：假定所有的无擦好仅发生在图像测量中，ML 残差期望值等于$\varepsilon_{res}=\delta(1-d/2n)^{1/2}$，其中$d$是要拟合的摄像机参数数目（对完整的针孔摄像机模型是 11）。给定一个残差，该公式也可以用来估计点测量的准确性


## 径向失真

- 用$(\tilde{x},\tilde{y})^\top$标记在理想（非失真）针孔投影下点以焦距为测量单位的坐标。对一点$\mathbf{X}$有：$(\tilde{x},\tilde{y},1)^\top=[\mathbf{I}|\mathbf{0}]\mathbf{X}_{cam}$，其中$\mathbf{X}_{cam}$是摄像机坐标下的 3D 点，实际的投影点通过一个径向位移与理想点关联。因此，径向（透镜）失真的模型是：
    
    $$\begin{bmatrix} x_d \\ y_d \end{bmatrix}=L(\tilde{r})\begin{bmatrix} \tilde{x} \\ \tilde{y} \end{bmatrix}$$

    - $(\tilde{x},\tilde{y})^\top$是理想图像位置（遵循线性投影）
    - $(x_d,y_d)^\top$是径向失真后的实际图像的位置
    - $\tilde{r}$为径向失真中心的径向距离$\sqrt{\tilde{x}^2+\tilde{y}^2}$
    - $L(\tilde{r})$是一个失真因子，它仅仅是半径$\tilde{r}$的函数

- **失真矫正**：在像素坐标中，失真矫正记为

    $$
    \hat{x}=x_c+L(r)(x-x_c) \ \ \ \ \ \ \hat{y}=y_c+L(r)(y-y_c)
    $$

    - $(x,y)^\top$是测量的坐标
    - $(\hat{x},\hat{y})^\top$是矫正后的坐标
    - $(x_c,y_c)^\top$是径向失真的中心且$r^2=(x-x_c)^2+(y-y_c)^2$，注意如果长宽比不是 1，那么在计算$r$时必须对它进行矫正

- **失真函数和中心的选择**：函数$L(r)$仅当$r$为正值时有定义并且$L(0)=1$。一个任意函数$L(r)$的逼近可以由泰勒展开式$L(r)=1+\mathcal{k}_1r+\mathcal{k}_2r^2+\mathcal{k}_3r^3+...$。$\{k_1,k_2,k_3,...,x_c,y_c\}$是径向矫正的系数。主点经常被用作径向失真的中心，虽然它们未必完全重合
- **计算失真函数**：函数$L(r)$可以通过最小化一个基于映射的线性偏差的代价函数来计算。失真函数可以作为影像过程的一部分，把参数$k_i$与$P$一起在几何误差的最小化迭代中计算
