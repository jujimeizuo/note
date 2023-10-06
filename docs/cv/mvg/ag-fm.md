---
counter: true
comment: true
---

# 对极几何和基本矩阵

!!! abstract
    - 对极几何是两幅视图之间内在的射影几何，独立于景物结构，只依赖于摄像机的内参数和相对姿态
    - 基本矩阵 F 集中了这个内在几何的精华，它是一个秩为 2 的$3 \times 3$矩阵，如果一个 3 维空间点$\mathbf{X}$在第一、第二幅视图中的像分别为$\mathbf{x},\mathbf{x}^\prime$，则这两个图像点满足关系$\mathbf{x}^{\prime \top}F\mathbf{x}=0$


## 对极几何

- 本质上，两幅视图之间的对极几何是图像平面与以基线（基线是连接两摄像机中心的直线）为轴的平面束的交的几何
- **对极点**是连接两摄像机中心的直线（基线）与像平面的**交点**。等价地，对极点是在一幅视图中另一个摄像机中心的像。它也是基线（平移）方向的消影点
- **对极平面**是一张包含基线的平面，存在着对极平面的一个单参数簇（束）
- **对极线**是极平面与图像平面的交线，所有对极线相交于对极点，一张对极平面与左或右像平面相交于对极线，并定义了对极线之间的对应
- **平行于图像平面的运动**：对于平行于图像平面作平移以及旋转轴垂直图像平面的特殊运动情形，基线与图像平面的交点位于无穷远，因此，对极点是无穷远点而对极线是平行线


<center><img src="https://cdn.jujimeizuo.cn/note/cv/mvg/ag.jpg" alt="对极几何"></center>


## 基本矩阵 F

- 基本矩阵 F 可以记为$F=[\mathbf{e}^\prime]$_\times H_\pi，其中$H_\pi=P^\prime P^+$是从一幅图像到另一幅图像通过任意平面$\pi$的转移映射。而且，因为$[\mathbf{e}^\prime]_\times$的秩为 2 和$H_\pi$秩为 3，所以 F 是秩 2 的矩阵
- 假设摄像机矩阵是一个已标定的双眼装置且世界原点在第一个摄像机上：

$$
F=[\mathbf{e}^\prime]_\times K^\prime R K^{-1}=K^{\prime-\top}[\mathbf{t}]_\times RK^{-1}=K^{\prime -\top}R[R^\top \mathbf{t}]_\times K^{-1}=K^{\prime -\top}RK^\top [\mathbf{e}]_\times
$$

### 对应条件

- 对两幅图像中任何一对对应点$\mathbf{x} \leftrightarrow \mathbf{x}^\prime$，基本矩阵都满足条件$\mathbf{x}^{\prime \top}F\mathbf{x}=0$
- $F$可以从两个摄像机矩阵$P、P^\prime$计算出来，即$F$可在相差一个整体尺度因子的一一下由摄像机唯一确定


### 基本矩阵的性质

- 假设两幅图像由中心不重合的摄像机获得，则基本矩阵$F$为对所有的对应点$\mathbf{x} \leftrightarrow \mathbf{x}^\prime$,对满足$\mathbf{x}^{\prime \top}F\mathbf{x}=0$的秩 2 的唯一的$3 \times 3$齐次矩阵
- F 是秩 2、自由度 7 的齐次矩阵
- **点对应**：如果$\mathbf{x}$和$\mathbf{x}^\prime$是对应的图像点，那么$\mathbf{x}^{\prime \top}F\mathbf{x}=0$
- **对极线**
    - $\mathbf{l}^\prime=F\mathbf{x}$是对应于$\mathbf{x}$的对极线
    - $\mathbf{l}=F^\top \mathbf{x}^\prime$是对应于$\mathbf{x}^\prime$的对极线
- **对极点**
    - $F\mathbf{e}=\mathbf{0}$
    - $F^\top\mathbf{e}^\prime=\mathbf{0}$
- **由摄像机矩阵$P、P^\prime$进行计算**
    - **一般摄像机**：$F=[\mathbf{e}^\prime]_\times P^\prime P^+$，其中$P^+$是$P$的伪逆，$\mathbf{e}^\prime=P^\prime \mathbf{C}$且$P\mathbf{c}=\mathbf{0}$
    - **规范摄像机**：$P=[I|\mathbf{0}],F=[\mathbf{e}^\prime]_\times M = M^{-\top}[\mathbf{e}]_\times$，其中$\mathbf{e}^\prime=\mathbf{m}$且$\mathbf{e}=M^{-1}\mathbf{m}$
    - **非无穷远摄像机**：$P=K[I|\mathbf{0}],P^\prime=K^\prime[R|\mathbf{t}],F=K^{-\top}[\mathbf{t}]_\times RK^{-1}=[K^\prime \mathbf{t}]_\times K^\prime R K^{-1}=K^{\prime -\top} RK^\top [KR^\top \mathbf{t}]_\times$
- **转置**：如果$F$是摄像机对作$(P,P^\prime)$的基本矩阵，则$F^\top$是其反序对$(P^\prime,P)$的基本矩阵


### 对极线单应

- 假设$\mathbf{l}$和$\mathbf{l}^\prime$是对应的对极线，且$k$是不过对极点$\mathbf{e}$的任何直线，则$\mathbf{l}$和$\mathbf{l}^\prime$间的关系是$\mathbf{l}^\prime=F[\mathbf{k}]_\times \mathbf{l}$，对称地有$\mathbf{l}=F^\top [\mathbf{k}^\prime]_\times \mathbf{l}^\prime$



## 由特殊运动产生的基本矩阵

- **纯平移**
  - 假设摄像机的运动是没有旋转并且内参不变的纯平移，可以假设两个摄像机矩阵分别是$P=K[I|\mathbf{0}]$和$P^\prime=K[I|\mathbf{t}]$，则$F=[\mathbf{e}^\prime]_\times KK^{-1}=[\mathbf{e}^\prime]_\times$，从像点$\mathbf{x}$到像点$\mathbf{x}^\prime$的映射是$\mathbf{x}^\prime=\mathbf{x}+K\mathbf{t}/Z$，其中$Z$是点$\mathbf{X}$的深度（在第一个摄像机的主轴上测量从$\mathbf{X}$到摄像机中心的距离）
      - 注意在纯平移情形，$F=[\mathbf{e}^\prime]_\times$是反对称的而且只有 2 个自由度，它们对应于对极点的位置
      - $\mathbf{x},\mathbf{x}^\prime$与$\mathbf{e}=\mathbf{e}^\prime$是共线的（假设把两幅图像叠起来）。这种共线性质称为**自对极**，并且对于一般运动不成立
- **一般运动**
    - 给定两个任意摄像机，我们可以把第一幅图像的摄像机旋转使它与第二个摄像机平行。该旋转可以通过对第一幅图像施加一个射影变换来仿真。针对两幅图像的标定矩阵的差别还可对第一幅图像施加进一步的矫正。这两次矫正的结果等价于对第一幅图像作射影变换$H$。假设这些矫正已经完成，那么这两个摄像机之间的有效关系是一个纯平移。
    - 假设两个摄像机矩阵分别为$P=K[I|\mathbf{0}]$和$P^\prime=K^\prime[R|\mathbf{t}]$，需要的射影变换是$H=K^\prime RK^{-1}=H_\infty$，其中$H_\infty$是无穷单应，且$F=[\mathbf{e}^\prime]_\times H_\infty$。则图像点$\mathbf{x}$到图像点$\mathbf{x}^\prime$的映射是：$\mathbf{x}^\prime=K^\prime RK^{-1}\mathbf{x}+K^\prime \mathbf{t} / Z$
- **纯平面运动**
    - 在纯平面运动时旋转轴与平移方向正交。正交性给这种运动增加了一个约束，如果$K^\prime=K$，则$F$的对称部分在这种平面运动情形时的秩为 2。使它的自由度个数从一般运动的 7 个降低到纯平面运动的 6 个



## 基本矩阵的几何表示

- 基本矩阵的对称和反对称部分分别为$F_s=(F+F^\top)/2 \ \ \ F_a=(F-F^\top)/2$，满足$F=F_s+F_a$
- **对称部分**：矩阵$F_s$是对称的并且一般地秩为 3，它有 5 个自由度并等同于一条点二次曲线，称为 Steiner 二次曲线
- **反对称部分**：矩阵$F_a$是反对称的并可以记为$F_a=[\mathbf{x}_a]_\times$，其中$\mathbf{x}_a$是$F_a$地零矢量。反对称部分有 2 个自由度且等同于点$\mathbf{x}_a$
- **对极线对应**：由一个单应关联的两个直线束，它们对应直线的交点的轨迹是一条二次曲线。这两个束都是对极线束，一个过$\mathbf{e}$而另一个过$\mathbf{e}^\prime$。这些对极线由一个 1D 单应相关联。其交点的轨迹是二次曲线$F_s$
- **纯平面运动**
    - 平面运动情形，其中$F_s$的秩为 2。此时 Steiner 二次曲线是退化的，它等价于两条不重合直线 $F_s=\mathbf{l}_h\mathbf{l}_s^\top+\mathbf{l}_s\mathbf{l}_h^\top$，$F$可以记为$F=[\mathbf{e}^\prime]_\times[\mathbf{l}_s]_\times[\mathbf{e}]_\times$
    - 两个对极点的分别有 2 个自由度和直线$\mathbf{l}_s$


## 恢复摄像机矩阵

### 射影不变性和规范摄像机

- 如果 H 是表示 3 维射影变换的一个$4 \times 4$矩阵，那么对应于摄像机矩阵$(P,P^\prime)$和$(PH,P^\prime H)$的基本矩阵是相同的
- **摄像机矩阵的规范形式**：对应于摄像机矩阵对$P=[I|\mathbf{0}]$和$P^\prime=[M|\mathbf{m}]$的基本矩阵等于$[\mathbf{m}]_\times M$

### 给定 F 后的摄像机射影多义性

- 令 F 为基本矩阵而$(P,P^\prime)$和$(\tilde{P},\tilde{P}^\prime)$都是与基本矩阵 F 对应的两组摄像机矩阵对，则存在一个非奇异的$4 \times 4$矩阵 H 使得$\tilde{P}=PH$和$\tilde{P}=P^\prime H$
- 若秩为 2 的矩阵 F 可以分解为两个不同的形式：$F=[\mathbf{a}]_\times A$和$F =[\tilde{\mathbf{a}}]_\times \tilde{A}$，则对某个非零常数 k 和 3 维矢量$\mathbf{v}$有$\tilde{\mathbf{a}}=k\mathbf{a}$和$\tilde{A}=k^{-1}(A+\mathbf{a} \mathbf{v}^\top)$

### 给定 F 求规范摄像机对

- 一个非零矩阵 F 是对应于一对摄像机矩阵$P$和$P^\prime$的基本矩阵的充要条件是$P^{\prime \top}FP$是反对称矩阵
- 令 F 是基本矩阵，S 是任意反对称矩阵。定义摄像机矩阵对为：$P=[I|\mathbf{0}]$和$P^\prime=[SF|\mathbf{e}^\prime]$，其中$\mathbf{e}^\prime$是满足$\mathbf{e}^{\prime \top}F=\mathbf{0}$的对极点，并假定所定义的$P^\prime$是有效的摄像机矩阵（秩为 3），则 F 是对应于$(P,P^\prime)$的基本矩阵
- 基本矩阵 F 的摄像机矩阵可以选择为$P=[I|\mathbf{0}]$和$P^\prime=[[\mathbf{e}^\prime]_\times F|\mathbf{e}^\prime]$
- 对应于基本矩阵 F，一对规范形式的摄像机矩阵的一般公式是$P=[I|\mathbf{0}] \ \ \ P^\prime=[[\mathbf{e}^\prime]_\times F + \mathbf{e}^\prime \mathbf{v}^\top | \lambda \mathbf{e}^\prime]$，其中$\mathbf{v}$是任何 3 维矢量，$\lambda$是一个正标量


## 本质矩阵

- 本质矩阵是归一化图像坐标系啊的基本矩阵的特殊形式。基本矩阵可以看作是本质矩阵的推广，基本矩阵把要求标定摄像机这样一个(非本质的)假设去掉了。与基本矩阵相比较，本质矩阵有较少的自由度但增加了一些性质。
- **归一化坐标**
    - 通过知道标定矩阵 K，用它的逆矩阵作用于点$\mathbf{x}$得到点$\hat{\mathbf{x}}=K^{-1}\mathbf{x}$，则$\hat{\mathbf{x}}=[R|\mathbf{t}]\mathbf{X}$，其中$\hat{\mathbf{x}}$是图像上的点在归一化坐标下的表示
    - 摄像机矩阵$K^{-1}P=[R|\mathbf{t}]$称为归一化摄像机矩阵
    - 用归一化图像坐标表示对应点$\mathbf{x} \leftrightarrow \mathbf{x}^\prime$时，本质矩阵的定义方程是 $\hat{\mathbf{x}}^{\prime \top} E \hat{\mathbf{x}}=0$，基本矩阵和本质矩阵之间的关系是 $E=K^{\prime \top}FK$

### 本质矩阵的性质

- 一个$3 \times 3$矩阵是本质矩阵的充要条件是它的奇异值中有两个相等而第三个是 0

### 由本质矩阵恢复摄像机矩阵

- 若 E 的 SVD 分解为$U diag(1,1,0)V^{\top},E=SR$有如下两种可能的分解：

$$
S=UZU^\top \ \ \ \ \ \ R=UWV^\top \ \ or \ \ UW^\top V^\top
$$

- 已知本质矩阵$U diag(1,1,0)V^\top$和第一个摄像机矩阵$P=[I|\mathbf{0}]$，那么第二个摄像机矩阵$P^\prime$有下列四种可能的选择：

$$
P^\prime=[UWV^\top|\mathbf{u}_3]; \ \ \
[UWV^\top|-\mathbf{u}_3]; \ \ \
[UW^\top V^\top|\mathbf{u}_3]; \ \ \
[UW^\top V^\top|-\mathbf{u}_3]
$$