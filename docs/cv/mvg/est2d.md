---
counter: True
comment: True
---


# 估计——2D 射影变换

!!! abstract
    本章主要讨论估计问题，估计的含义是指在某些本质测量的基础上计算某个变换或其它数学量，常见的估计问题的类型有：

    - **2D 单应**：给定$IP^2$中的点集$\mathbf{x}_i$，和同在$IP^2$中的对应点集$\mathbf{x}_i^\prime$，计算把每一点$\mathbf{x}_i$映射到对应点$\mathbf{x}_i^\prime$的射影变换。
    - **3D 到 2D 的摄像机投影**：给定 3D 空间的点集$X_i$以及一幅图像上的对应点集$\mathbf{x}_i$，求把$X_i$映射到$\mathbf{x}_i$的 3D 到 2D 的射影映射。
    - **基本矩阵的计算**：给定一幅图像上的点集$\mathbf{x}_i$，和另一幅图像上的对应点集$\mathbf{x}_i^\prime$，计算与这些对应一直的**基本矩阵$F$**。
    - **三焦点张量计算**：给定跨三幅图像的点对应$\mathbf{x}_i \leftrightarrow \mathbf{x}_i^\prime \leftrightarrow \mathbf{x}_i^{\prime \prime}$，计算三焦点张量。

    研究两幅图像之间对应点的集合$\mathbf{x}_i \leftrightarrow \mathbf{x}_i^\prime$，计算对所有的 i 都满足$H\mathbf{x}_i=\mathbf{x}_i^\prime$的一个$3 \times 3$矩阵 H：

    - **测量数**：矩阵 H 有 9 个元素，但仅确定到相差一个尺度因子。因此，2D 射影变换的自由度的总数是 8。因为一个 2D 点有两个自由度，所以为了完全约束 H，需要指定四组点对应。
    - **近似解**：如果给定四组对应，那么可以得到矩阵 H 的精确解这种解称为**最小配置解**。如果给定多于四组的对应，那么这些对应可能不与任何射影变换完全相容，因而我们面临的任务是按给定的数据确定“最好”的变换。通常这个任务是通过寻找最小化某个代价函数的变换 H 来完成。
    - **黄金标准算法**：通常存在一种最优的代价函数，其最优的含义是在一定假设下，使代价函数取最小值的 H 是变换的最好估计。计算该代价函数最小值的算法称为“黄金标准”算法。


## 直接线性变换（DLT）算法

- 首先讨论由给定 2D 到 2D的四组点对应$\mathbf{x}_i \leftrightarrow \mathbf{x}_i^\prime$确定 H 的一种简单的线性算法，变换由$\mathbf{x}_i^\prime = H\mathbf{x}_i$给出。但因为这是一个齐次矢量方程，因此 3 维矢量$\mathbf{x}_i^\prime$和$H\mathbf{x}_i$不相等。可以用矢量叉乘：$\mathbf{x}_i^\prime \times H\mathbf{x}_i=\mathbf{0}$表示。
- 如果将矩阵 H 的第 j 行记为$h^{j\top},\mathbf{x}_i^\prime=(x_i^\prime, y_i^\prime, w_i^\prime)^\top$，则$\mathbf{x}_i^\prime \times H \mathbf{x}_i=0$可以转换成：

$$
\begin{bmatrix}
\mathbf{0}^\top & -w_i^\prime\mathbf{x}_i^\top & y_i^\prime \mathbf{x}_i^\top \\
w_i^\prime\mathbf{x}_i^\top  & \mathbf{0}^\top & -x_i^\prime\mathbf{x}_i^\top \\
-y_i^\prime \mathbf{x}_i^\top  & x_i^\prime\mathbf{x}_i^\top & \mathbf{0}^\top
\end{bmatrix}
\begin{bmatrix}
\mathbf{h}^1 \\
\mathbf{h}^2 \\
\mathbf{h}^3
\end{bmatrix}
=\mathbf{0}
$$

- h 是由矩阵 H 的元素组成的 0 维矢量：

$$
\mathbf{h}=
\begin{bmatrix}
\mathbf{h}^1 \\
\mathbf{h}^2 \\
\mathbf{h}^3
\end{bmatrix}
, \ \ \ 
H=
\begin{bmatrix}
h_1 & h_2 & h_3 \\
h_4 & h_5 & h_6 \\
h_7 & h_8 & h_9
\end{bmatrix}
$$

- $A_i\mathbf{h}=\mathbf{0}$是未知矢量$\mathbf{h}$的线性方程，矩阵$A_i$的元素是已知点的坐标的二次多项式。
- 虽然式中有三个方程，但仅有两个是线性独立的。在解 H 时常省去第三个等式。
- 该方程组对$\mathbf{x}_i^\prime$的任何齐次坐标$(x_i^\prime, y_i^\prime, w_i^\prime)^\top$成立。
- **求解 H**：每组点对应给出关于 H 元素的两个独立的方程。给定四组这样的点对应，便获得方程组$A\mathbf{h}=\mathbf{0}$。


### 超定解

- 如果给出的点对应$\mathbf{x}_i \leftrightarrow \mathbf{x}_i^\prime$多余四组，方程$A\mathbf{h}=\mathbf{0}$是超定的。
- 如果点的位置是精确的，那么$A$的秩仍然为 8 并有一维零空间，并且存在精确解$\mathbf{h}$。
- 如果图像坐标的测量时不精确的，方程组将不存在精确解。所以需要一个适当的代价函数取最小值的矢量$\mathbf{h}$，通常附加范数条件，既然不存在$A\mathbf{h}=\mathbf{0}$的精确解，很自然会在通常约束$\parallel \mathbf{h} \parallel = 1$下最小化范数$\parallel A \mathbf{h} \parallel$。这等价于求商$\parallel A \mathbf{h} \parallel / \parallel \mathbf{h} \parallel$的最小值问题。该解是$A^\top A$的最小特征值的（单位）特征矢量。由此所得到的算法称为**基本DLT算法**。


### 非齐次解

- 把等式转成非齐次线性方程组，即给矢量$\mathbf{h}$中的某个元素强加上$h_j=1$的条件：

$$
\begin{bmatrix}
 0 & 0 & 0 & -x_iw_i^\top & -y_iw_i^\top & -w_iw_i^\top & x_iy_i^\top & y_iy_i^\top \\
 x_iw_i^\top & y_iw_i^\top & w_iw_i^\top & 0 & 0 & 0 & -x_ix_i^\top & -y_ix_i^\top \\
\end{bmatrix}
\bar{\mathbf{h}}=
\begin{bmatrix}
-w_iy_i^\top \\
-w_ix_i^\top
\end{bmatrix}
$$

- 其中$\bar{\mathbf{h}}$是由$\mathbf{h}$的前八个元素组成的 8 维矢量。
- 但是，如果事实上真正的解是$h_j=0$，那么不存在一因子$k$使得$kh_j=1$，表示令$h_j=1$得不到真解。

### 退化配置

- 如果$\mathbf{x}_1, \mathbf{x}_2, \mathbf{x}_3$共线，那么$H^*=\mathbf{x}_4^\top\mathbf{I}^\top$是一个解
    - $H^*$是唯一解（相差一尺度因子），因为$H^*$是奇异矩阵，不存在把每个$\mathbf{x}_i$变到$\mathbf{x}_i^\prime$的变换。当$\mathbf{x}_1, \mathbf{x}_2, \mathbf{x}_3$共线，而$\mathbf{x}_1^\prime, \mathbf{x}_2^\prime, \mathbf{x}_3^\prime$不共线时就会产生这种情况
    - 存在另外一个解$H$：从而任何形如$\alpha H^*+\beta H$的矩阵都是解，因此有一个 2 参数的变换簇存在，进而推出给出的 8 个方程不是独立的
    - 出现某种配置不能确定唯一解的情形称为**退化**。
- 退化的定义既涉及配置也涉及变换类型，而且退化问题不仅限于最小配置解。如果多出来的（精确的，即无误差的）点对应也共线，那么退化问题仍没有解决。

<center><img src="https://cdn.jujimeizuo.cn/note/cv/mvg/dot-line-config.jpg" alt="点-线配置的几何等价性"></center>


### 由线和其他实体求解

- 前面只讨论由点对应来计算单应，然而线对应和二次曲线的对应也可以计算单应，所以就产生计算一个单应（或任何其他关系）需要多少组对应的问题。一般的原则是约束数必须等于或大于变换的自由度数。
- 采用混合类型的对应来计算 H 时必须谨慎，例如一个 2D 单应不能由两组点对应和两组线对应唯一确定，但能由三级点和一组线或一组点和三组线来唯一确定，即使每种配置都有 8 个自由度也是如此。


## 不同的代价函数

> 为确定 H 的超定解而需最小化的若干代价函数

### 代数距离

- DLT 算法最小化范数$\parallel A \mathbf{h} \parallel$。
- 矢量$\varepsilon=A\mathbf{h}$称为残差矢量，并且要最小化的正是该误差矢量的范数。
- 矢量$\varepsilon_i$被称为关联于点对应$\mathbf{x}_i \leftrightarrow \mathbf{x}_i^\prime$和单应 H 的**代数误差矢量**，该矢量的范数是一个标量，称为**代数距离**：

$$
d_{alg}(\mathbf{x}_i^\prime, H\mathbf{x}_i)^2=
\parallel \varepsilon_i \parallel=
\parallel 
\begin{bmatrix}
\mathbf{0}^\top & -w_i^\prime\mathbf{x}_i^\top & y_i^\prime \mathbf{x}_i^\top \\
w_i^\prime\mathbf{x}_i^\top & \mathbf{0}^\top & -x_i^\prime \mathbf{x}_i^\top
\end{bmatrix}
\mathbf{h} \parallel^2
$$

- 对于任何两个矢量$\mathbf{x}_1$和$\mathbf{x}_2$：

$$
\sum_{i}d_{alg}(\mathbf{x}_1, \mathbf{x}_2)^2=a_1^2+a_2^2
\ \ 其中\mathbf{a}=(a_1,a_2,a_3)^\top=\mathbf{x}_1 \times \mathbf{x}_2
$$

- 给定对应的集合，量$\varepsilon=A\mathbf{h}$是整个集合的代数误差矢量，由此可见：

$$
\sum_{i}d_{alg}(\mathbf{x}_i^\prime, H\mathbf{x}_i)^2=
\sum_{i} \parallel \varepsilon_i \parallel^2=
\parallel A\mathbf{h} \parallel^2=
\parallel \varepsilon \parallel^2
$$

- 缺点是被最小化的量没有几何或统计上的意义。

### 几何距离

#### 记号

- 矢量$\mathbf{x}$表示**测量**的图像坐标；$\hat{\mathbf{x}}$表示该点的估计值而$\bar{\mathbf{x}}$表示该点的真值。
#### 单图像误差

- 首先考虑第一幅图像的测量非常精确而误差仅出现在第二幅图像的情形。适宜最小化的量是**转移误差**。它是第二幅图像上测量点$\mathbf{x}^\prime$与点$H\bar{\mathbf{x}}$之间的**欧氏距离**。用记号$d(\mathbf{x}, \mathbf{y})$表示非齐次点$\mathbf{x}$和$\mathbf{y}$之间的欧氏距离。对应集合的转移误差是：

$$
\sum_{i} d(\mathbf{x}_i^\prime, H\bar{\mathbf{x}_i})^2
$$

#### 对称转移误差

- 更切合实际的情形是图像测量误差在两幅图像中都发生，从而应该最小化两幅而不仅是一幅图像的误差：

$$
\sum_{i} d(\mathbf{x}_i, H^{-1}\mathbf{x}_i^\prime)^2+d(\mathbf{x}_i^\prime, H\mathbf{x}_i)^2
$$

#### 重投影误差——两幅图像

- 对每幅图像误差作量化的另一种方法是估计每组对应的“校正值”。为了得到完全的匹配点集有必要在一幅图像（第二幅图像）上对测量进行校正。
- 单应$\hat{H}$和完全匹配的点对$\hat{\mathbf{x}_i}$和$\hat{\mathbf{x}_i}^\prime$以最小化总的误差函数:

$$
\sum_{i} d(\mathbf{x}_i, \hat{\mathbf{x}_i})^2+d(\mathbf{x}_i^\prime, \hat{\mathbf{x}_i}^\prime)^2 \ \ \ s.t \ \ \ \hat{\mathbf{x}_i}^\prime=\hat{H}\hat{\mathbf{x}_i} \ \ \ \forall i.
$$

- 先由$\mathbf{x}_i \leftrightarrow \mathbf{x}_i^\prime$估计世界平面的点$\hat{\mathbf{X}_i}$，然后把它重投影到估计上认为是完全匹配的对应$\hat{\mathbf{x}_i} \leftrightarrow \hat{\mathbf{x}_i}^\prime$


### 几何和代数距离的比较

- 令$\mathbf{x}_i^\prime=(x_i^\prime, y_i^\prime, w_i^\prime)^\top$并定义矢量$(\hat{x_i}^\prime, \hat{y_i}^\prime, \hat{w_i}^\prime)^\top=\hat{\mathbf{x}_i}^\prime=H\bar{\mathbf{x}}$，则

$$
d(\mathbf{x}_i^\prime, \hat{\mathbf{x}_i}^\prime)^2=
d_{alg}(\mathbf{x}_i^\prime, \hat{\mathbf{x}_i}^\prime)^2/\hat{w_i}^\prime w_i^\prime
$$

- 几何距离与代数距离相关，但不相等。只有当$\hat{w_i}^\prime=w_i^\prime=1$两个距离相等。因此在仿射变换下，几何距离和代数距离相等。对于仿射变换，最小化几何距离可以用基于代数距离的线性 DLT 算法。

### 重投影误差的几何解释

- 两平面之间的单应估计可以视为用 4D 空间$IR^4$中的“曲面”来拟合点。
- 每对图像点$\mathbf{x}, \mathbf{x}^\prime$定义测量空间$IR^4$的一个点，记作$\mathbf{X}$。
- 对给定的单应 H，满足$\mathbf{x} \times \mathbf{x}^\prime=\mathbf{0}$的图像对应$\mathbf{x} \leftrightarrow \mathbf{x}^\prime$定义来$IR^4$中的一个代数簇$\upsilon_H$，它是两个超二次曲面的交集。

$$
d(\mathbf{x}_i, \hat{\mathbf{x}_i})^2+d(\mathbf{x}_i^\prime, \hat{\mathbf{x}_i}^\prime)^2=d_\perp(\mathbf{X}_i, \upsilon_H)^2
$$

- 其中$d_\perp(\mathbf{X}_i, \upsilon_H)^2$是点$\mathbf{X}$到簇$\upsilon_H$的垂直距离。

### Sampson 误差

- Sampson 误差其复杂性介于代数和几何代价函数之间，但非常近似于几何误差。
- 对给定的单应 H，在$\upsilon_H$上的任何点$\mathbf{X}=(x,y,x^\prime, y^\prime)^\top$，代价函数用$\mathcal{C}_H(\mathbf{X})=\mathbf{0}$。用下列 Taylor 展开式来一阶逼近：

$$
\mathcal{C}_H(\mathbf{X}+\delta_x)=\mathcal{C}_H(\mathbf{X})+\frac{\partial \mathcal{C}_H}{\partial \mathbf{X}} \delta_x
$$

- 记$\delta_x = \hat{\mathbf{X}}-\mathbf{X}$希望$\hat{\mathbf{X}}$在$\upsilon_H$上，即$\mathcal{C}_H(\hat{\mathbf{X}})=\mathbf{0}$，因此$\mathcal{C}_H(\mathbf{X})+\frac{\partial \mathcal{C}_H}{\partial \mathbf{X}} \delta_x=\mathbf{0}$。记成$\mathbf{J}\delta_x=-\varepsilon$，其中$\mathbf{J}$是偏导数矩阵，$\varepsilon$与$\mathbf{X}$相关的代价函数$\mathcal{C}_H(\mathbf{X})$，**最小化问题**是求满足此方程的最小$\delta_x$。
    - 即 **求在满足$\mathbf{J}\delta_x=-\varepsilon$条件下使$\parallel \delta_x \parallel$取最小值的矢量$\delta_x$**
    - 使用 Lagrange 乘子法，求的范数$\parallel \delta \parallel^2$是 Sampson 误差：

    $$
    \parallel \delta_x \parallel^2=
    \delta_x^\top\delta_x=
    \varepsilon^\top(\mathbf{J}\mathbf{J}^\top)^{-1}\varepsilon
    $$

## 统计代价函数和最大似然估计

- 假定在没有测量误差时，真实的点准确满足一个单应变换，即$\bar{\mathbf{x}_i}^\prime=H\bar{\mathbf{x}_i}$。
- 假定每一幅图像坐标都具有零均值和统一的标准差$\sigma$的高斯噪声。这意味着$x=\bar{x}+\Delta x$，其中$\Delta x$服从方差为$\sigma^2$的高斯分布。进一步假设每次测量的噪声是相在独立的，那么，若点的真值是$\bar{\mathbf{x}}$，则每个测量点$\mathbf{x}$的概率密度函数(pdf)是：

$$
\Pr(\mathbf{x})=(\frac{1}{2\pi\sigma^2})e^{-d(\mathbf{x},\bar{\mathbf{x}})^2/(2\sigma^2)}
$$

### 单图像误差

- 假定每点的误差是独立的，点对应$\{\bar{\mathbf{x}_i} \leftrightarrow \mathbf{x}_i^\prime\}$的概率就是它们单个 pdf 的乘积：


$$
\Pr(\{\mathbf{x}_i^\prime | H\}) = \prod_{i}(\frac{1}{2\pi\sigma^2})e^{-d(\mathbf{x}_i^\prime, H \bar{\mathbf{x}}_i)^2/(2\sigma^2)}
$$

- 该对应集合的**对数似然**为：

$$
\log \Pr(\mathbf{x}_i^\prime | H)=-\frac{1}{2\sigma^2}\sum_{i}d(\mathbf{x}_i^\prime, H \bar{\mathbf{x}}_i)^2+常数
$$

- 单应的**最大似然 ML **估计$\hat{H}$最大化这个对数似然，即最小化：

$$
\sum_{i}d(\mathbf{x}_i^\prime, H \bar{\mathbf{x}}_i)^2
$$

- 因此，ML 估计等价于最小化几何误差函数

### 双图像误差

- 如果真实对应是$\{\bar{\mathbf{x}}_i \leftrightarrow H \bar{\mathbf{x}}_i=\bar{\mathbf{x}}_i^\prime\}$，受噪声干扰的数据的 pdf 是：

$$
\Pr(\{\mathbf{x}_i, \mathbf{x}_i^\prime\} | H, \{\bar{\mathbf{x}}_i\}) = \prod_{i}(\frac{1}{2\pi\sigma^2})e^{-(d(\mathbf{x}_i, \bar{\mathbf{x}}_i)^2+d(\mathbf{x}_i^\prime, H\bar{\mathbf{x}}_i)^2)/(2\sigma^2)}
$$

- ML 估计就是求最小化：

$$
\sum_{i}d(\mathbf{x}_i, \hat{\mathbf{x}}_i)^2+d(\mathbf{x}_i^\prime, \hat{\mathbf{x}}_i^\prime)^2
$$

- ML 估计等同于最小化重投影误差函数

### Mahalanobis 距离

- 一般高斯分布的情形，可以假定测量矢量$\mathbf{X}$满足一个具有协方差矩阵$\sum$的高斯分布函数。最大化对数似然则等价于最小化 Mahalanobis 距离：

$$
\parallel \mathbf{X} - \bar{\mathbf{X}} \parallel_{\sum}^2=(\mathbf{X}-\bar{\mathbf{X}})^\top\sum\nolimits^{-1}(\mathbf{X}-\bar{\mathbf{X}})
$$

- 当每幅图像都有误差并假定一幅图像中的误差与另一幅图像中的误差是独立的时，合适的代价函数是：

$$
\parallel \mathbf{X} - \bar{\mathbf{X}} \parallel_{\sum}^2+\parallel \mathbf{X}^\prime - \bar{\mathbf{X}}^\prime \parallel_{\sum^\prime}^2
$$

- 其中$\sum$和$\sum^\prime$是两幅图像的测量的协方差矩阵

## 变换不变性和归一化

### 关于图像坐标变换的不变性

- 假定一幅图像的坐标$\mathbf{x}$被$\tilde{\mathbf{x}}=T\mathbf{x}$替代，而另一幅图像的坐标$\mathbf{x}^\prime$被$\tilde{\mathbf{x}}^\prime=T^\prime\mathbf{x}^\prime$替代。因此$\mathbf{x}_i$映射到$\mathbf{x}_i^\prime$的变换的另一种方法是：

    1. 根据公式$\tilde{\mathbf{x}}_i=T\mathbf{x}_i$和$\tilde{\mathbf{x}}_i^\prime=T^\prime\mathbf{x}_i^\prime$变换图像坐标
    2. 由对应$\tilde{\mathbf{x}}_i \leftrightarrow \tilde{\mathbf{x}}_i^\prime$，求$\tilde{H}$
    3. 令$H=T^{\prime-1}\tilde{H}T$


### DLT 算法的非不变性

- 令$T^\prime$为具有缩放因子$s$的相似变换，$T$为任意的射影变换。此外，假设$H$是任何 2D 单应并定义$\tilde{H}=T^\prime HT^{-1}$，那么$\parallel \tilde{A} \tilde{\mathbf{h}} \parallel = s \parallel A \mathbf{h} \parallel$

- 虽然这样定义的$H$和$\tilde{H}$给出同样的误差$\varepsilon$，但是对解施加的约束条件$\parallel H \parallel = 1$不等价于条件$\parallel \tilde{H} \parallel = 1$，它们并不以任何简单的方式相关联。


### 几何误差的不变性

$$
d(\tilde{\mathbf{x}}^\prime, \tilde{H}\tilde{\mathbf{x}})=
d(T^\prime \mathbf{x}^\prime, T^\prime HT^{-1}T\mathbf{x})=
d(T^\prime \mathbf{x}^\prime, T^\prime H\mathbf{x})=
d(\mathbf{x}^\prime, H\mathbf{x})
$$

- 在相似变换下，几何误差被乘以变换的缩放因子，从而最小化变换的对应方式与欧氏变换相同。所以最小化几何误差在相似变换下不变。

### 归一化变换

- 数据归一化不仅提高了结果的精度，还对初始数据归一化的算法将对任何尺度缩放和坐标原点的选择不变。因而使 DLT 算法实际上关于相似变换不变。

#### 各向同性缩放

1. 对点进行平移使点集形心位于原点
2. 对点进行缩放使它们到原点的平均距离等于$\sqrt{2}$
3. 对两幅图像独立进行上述变换

- **数据归一化在 DLT 算法中是实质性的，一定不要视它为可有可无的。**

#### 归一化与条件数

- 归一化的影响与 DLT 方程组的条件数或准确地说与方程组矩阵 A 的第一个和倒数第二个奇异值的比率$d_1/d_{n-1}$有关。但是，在有噪声存在时解将偏离其正确结果。大条件数会放大这种偏向。

#### 非各向同性缩放

- 在非各同性缩放中，点的形心和前面一样平移到原点，经平移后点在原点附近形成云。然后进行坐标尺度缩放使该点集的两主矩都等于 1。这样使该点集形成以原点为中心，半径为 1 的近似的对称圆云。

#### 无穷远附近的点的缩放

- 当点位于或接近平面的无穷远时，各向同性（或非各向同性）的缩放方式来归一化坐标是既无道理又不可行的，因为形心坐标和缩放因子为无穷大或接近无穷大。一个似乎会给出好结果的方法是归一化点集$\mathbf{x}_i=(x_i,y_i,w_i)^\top$使得：

$$
\sum_i x_i=\sum_i y_i=0;\sum_ix_i^2+y_i^2=2\sum_iw_i^2;x_i^2+y_i^2+w_i^2=1,\forall i
$$

## 迭代最小化方法

!!! note "迭代最小化技术"
    1. **代价参数**：代价函数是最小化的基础
    2. **参数化**：把要计算的变换（或其他实体）表示成有限数目的参数
    3. **函数确定**：必须确定一个用参数集描述的代价函数
    4. **初始化**：计算一个适当的初始参数估计。一般将由一个线性算法（例如 DLT 算法）来实现
    5. **迭代**：由初始解开始，在迭代中逐步修正参数以达到最小化代价函数的目的

### 关于参数化

- 指导参数化的一般策略是选择能覆盖最小化的整个空间并能用一种方便的方式来计算代价函数。对于齐次目标通常设有必要或不鼓励追求消除尺度因子的多义性而采用最小参数化。选择参数化的另一个考虑是限制变换为一个具体的类型。

### 函数确定

1. 有一个协方差矩阵为$\sum$的**测量矢量$\mathbf{X} \in IR^N$**
2. 一组参数被表达成一个矢量$\mathbf{P} \in IR^M$
3. 定义一个映射$f:\ IR^M \to IR^N$，其值域（至少局部地）是$IR^N$中表示容许测量集的模型曲面 S
4. 最小化代价函数是 Mahalanobis 距离

$$\parallel \mathbf{X} - f(\mathbf{P}) \parallel_{\sum}^2=(\mathbf{X} - f(\mathbf{P}))^\top\sum\nolimits^{-1}(\mathbf{X} - f(\mathbf{P}))$$

- **单图像误差-最小化代价函数**：固定第一幅图像中点$\mathbf{x}_i$的坐标，并变换 H 以最小化代价函数：

$$
\sum_id(\mathbf{x}_i^\prime,H\tilde{\mathbf{x}}_i)^2 \\
f:\mathbf{h} \to (H\mathbf{x}_1, H\mathbf{x}_2, ..., H\mathbf{H}_n)
$$

- **对称传递误差-对称化代价函数**

$$
\sum_id(\mathbf{x}_i, H^{-1}\mathbf{x}_i^\prime)^2+d(\mathbf{x}_i^\prime, H\mathbf{x}_i)^2 \\
f: \mathbf{h} \to (H^{-1}\mathbf{x}_1^\prime, ..., H^{-1}\mathbf{x}_n^\prime, H\mathbf{x}_1, ..., H\mathbf{x}_n)
$$

- **重投影误差**：可以用$\hat{\mathbf{x}}_i$坐标和$\hat{H}$矩阵的元素——总共$2n+9$个参数来参数化。**参数矢量**：$\mathbf{P}=(\mathbf{h}, \hat{\mathbf{x}}_i, ..., \hat{\mathbf{x}}_n)$。函数$f$定义为$f:\mathbf{P}\to (\hat{\mathbf{x}}_1, \hat{\mathbf{x}}_i^\prime, ..., \hat{\mathbf{x}}_n, \hat{\mathbf{x}}_n^\prime)$

- **Sampson 近似**：重投影误差的 Sampson 近似使投影误差也能仅对 9 个参数最小化

### 初始化

- 可以用线性技术或最小配置解来求参数化的初始估计。还采用的另一种方法是在参数空间进行足够密的采样，从每一个采样初始点开始迭代并保留最好的结果。这种方法仅在参数空间的维数足够小时才可采用

### 迭代方法

- 其中最常用的有 Newton 迭代和 Levenberg-Marquardt 方法。Newton 迭代是最快的，但是它需要计算代价函数的二阶导数，而且在某些情况下可能会发散。Levenberg-Marquardt 方法是一种更稳定的方法，但是它的收敛速度比 Newton 迭代慢。

### 算法的实验比较


<center><img src="https://cdn.jujimeizuo.cn/note/cv/mvg/cpi-func-of-ptm.jpg" alt="图像对应点计算射影变换方法"></center>


## 鲁棒估计

- 之前讨论的对应集的唯一误差源来自点的位置测量，在许多实际运行中，还存在着点被错配的情况。错配点对高斯误差分布而言是**野值**。

### RANSAC

- 用**模型**去拟合数据，**随机样本**包含足以确定模型的最小数据集。如果模型是平面单应，而数据是 2D 点对应集，那么最小子集包含四组对应。

!!! note "算法流程"
    1. 随机地从数据集$S$中选择$s$个数据点组成的一个样本作为模型的一个示例
    2. 确定在模型距离阈值$t$内的数据点集 $S_i$，$S_i$称为采样的一致集并定义$S_i$的内点
    3. 如果$S_i$的大小(内点的数目)大于某个阈值$T$，用$S_i$的所有点重估计模型并结束
    4. 如果$S_i$的大小小于$T$，选择一个新的子集并重复上面的过程
    5. 经过$N$次试验选择最大一致集$S_i$，并用$S_i$的所有点重估计模型

### 鲁棒最大似然估计

- **鲁棒代价函数**：不同于仅在内点上最小化$\mathcal{C}=\sum_{i}d_{\perp}^2$，另一种改进的鲁棒方法是在所有数据上最小化。一个合适的鲁棒代价函数是

$$
\mathcal{D}=\sum_i \gamma(d_{\perp})且\gamma(e)=
\left\{\begin{matrix}
 e^2 & e^2 < t^2 & 内点 \\
 t^2 & e^2 >= t^2 & 野值
\end{matrix}\right.
$$

- $d_\perp$是点的误差，$\gamma(e)$是一个鲁棒代价函数，其中给野值赋一个固定的代价。

### 其他鲁棒算法

- **最小中值平方(LMS)估计**： 根据数据中所有点的距离中值，选择具有最小中值的模型。LMS 的优点在于它不需要阈值或误差方差的先验知识。 LMS 的缺点是如果多于一半的数据是野值那么它要失败，因为距离的中值可能是一个野值。解决的办法是用野值的比例来确定所选的距离。
- 如果野值的数量少，那么可以采用以下鲁棒方法：

    - **删点方法** 每点轮流被删除而用模型对剩下的数据拟合。
    - **加权最小二乘方迭代** 其中一个数据点对拟合的影响以它的残差来反加权。


## 单应的自动计算

- 计算两幅图像间的单应的算法。
- 算法的输入仅仅是图像，不需要其他**先验**信息；而输出的是单应的估计以及一组对应的兴趣点。该算法可以应用于诸如一张平坦表面的两幅图像或由摄像机绕其光心旋转的到的两幅图像。

!!! note "算法流程"
    1. **兴趣点**：在每一幅图像上计算兴趣点
    2. **假设对应**：根据兴趣点灰度领域的接近和相似，计算它们的匹配集。
    3. **RANSAC鲁棒估计**：重复$N$次采样：
        1. 选择由四组对应组成的一个随机样本并计算单应 H
        2. 对假设的每组单应，计算距离$d_{\perp}$
        3. 根据$d_\perp < t = \sqrt{5.99} \delta$像素确定对应数，进而计算与 H 一致的内点数
        4. 选择具有最大内点数的 H，当数目相等时选择内点的标准方差最低的 H
    4. **最优估计**：由划定的内点的所有对应重新估计 H，用 Levenberg-Marquardt 算法来最小化 ML 代价函数
    5. **引导匹配**：用估计的 H 去定义转移点位置附近的搜索区域，进一步确定兴趣点的对应。

    最后两步重复到对应的数目稳定为止