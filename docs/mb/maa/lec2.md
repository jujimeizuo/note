---
counter: True
---

# 矩阵代数基础

!!! abstract
    元素之间存在某种特殊结构关系的矩阵，统称为特殊矩阵

## Hermitian 矩阵


- 一个正方的复值矩阵$\mathbf{A}=[a_{ij}] \in C^{n\times n}$称为 Hermitian 矩阵
- 若$\mathbf{A}=-\mathbf{A}^H$，则矩阵$\mathbf{A}$称为反 Hermitian 矩阵
- 中央 Hermitian 矩阵$\mathbf{R}$是一个元素满足对称性$r_{ij}=r_{n-j+1,n-i+1}^*$的$n \times n$正方矩阵
- 中央 Hermitian 矩阵的一个特殊子类是双重对称的矩阵，它既是关于主对角线对称的 Hermitian 矩阵，又是关于交叉对角线对称的交叉对称矩阵，如

$$
\mathbf{R}=
\begin{bmatrix}
 r_{11} & r_{21}^* & r_{31}^* & r_{41}^* \\
 r_{21} & r_{22} & r_{32}^* & r_{31}^* \\
 r_{31} & r_{32} & r_{22} & r_{21}^* \\
 r_{41} & r_{31} & r_{21} & r_{11}
\end{bmatrix}
$$

## 置换矩阵、互换矩阵与选择矩阵

### 置换矩阵与互换矩阵

- 若每一行和每一列有且只有一个非零元素 1 的正方矩阵称为置换矩阵
- $(\mathbf{P}_{m \times n})^{\top} = \mathbf{n \times m}$
- $\mathbf{P}^{\top}\mathbf{P}=\mathbf{P}\mathbf{P}^{\top}=\mathbf{I}$，说明置换矩阵是正交矩阵
- $\mathbf{P}^{\top}=\mathbf{P}^{-1}$
- $\mathbf{P}^{\top}\mathbf{A}\mathbf{P}$与$\mathbf{A}$具有相同的对角线元素，但排列顺序可能不同
- 另外三个特殊形式：交换矩阵、互换矩阵、移位矩阵

### 广义置换矩阵与选择矩阵

- 每一行和每一列有且只有一个非零元素的正方矩阵称为广义置换矩阵
- 一个正方矩阵是 $g$ 矩阵，当且仅当它可以分解为一个置换矩阵和一个非奇异的对角矩阵之积，即$\mathbf{G}=\mathbf{P}\mathbf{D}$
- 选择矩阵是一种可以对某个给定矩阵的某些行或者某些列进行选择的矩阵

## 正定矩阵与酉矩阵

- 向量$x_1, ..., x_k \in C^n$组成一正交组，若$x_i^Hx_j=0, 1 \le i < j < \le k$。若是归一化的，则为标准正交组
- 一组正交的非零向量是线性无关的
- 一实的正方矩阵$\mathbf{Q} \in R^{n \times n}$称为正交矩阵，若$\mathbf{Q}\mathbf{Q}^{\top}=\mathbf{Q}^{\top}\mathbf{Q}=\mathbf{I}$
- 一复值正方矩阵$\mathbf{U}\in C^{n \times n}$称为酉矩阵，若$\mathbf{U}\mathbf{U}^{\top}=\mathbf{U}^{\top}\mathbf{U}=\mathbf{I}$


<center><img src="https://cdn.jujimeizuo.cn/note/mb/maa/matrix-property-comparison.jpg"></center>

- 若$n \times n$矩阵$\mathbf{A}=[a_{ij}]$和$\mathbf{B}=[b_{ij}]$是酉等价的，则$\sum_{i=1}^n\sum_{j=1}^n|b_{ij}|^2=\sum_{i=1}^n\sum_{j=1}^n|a_{ij}|^2$
- 矩阵$\mathbf{A} \in C^{n \times n}$称为正规矩，若$\mathbf{A}^H\mathbf{A}=\mathbf{A}\mathbf{A}^{\top}$
- 令$\mathbf{J}$为$N \times N$符号矩阵，满足$\mathbf{Q}\mathbf{J}\mathbf{Q}^{\top}=\mathbf{J}$的$N \times N$矩阵$\mathbf{Q}$称为$J$正交矩阵，或称超正规矩阵

## 带型矩阵与三角矩阵

### 带行矩阵

- 满足$a_{ij}=0,|i-j|>k$的矩阵$\mathbf{A}\in C^{m\times n}$称为带型矩阵
- 三对角矩阵是带型矩阵的特殊形式，当$|i-j|>1$时，$a_{ij}=0$

### 三角矩阵

- 两种特殊的常用带型矩阵为上三角矩阵和下三角矩阵

## 求和向量与中心化矩阵

### 求和向量

- 所有元素等于 1 的向量称为求和向量，记为$\mathbf{I}=[1,1,...,1]^{\top}$

### 中心化矩阵

- 矩阵$\mathbf{C}_n=\mathbf{I}_n-\mathbf{J}_n=\mathbf{I}_n-\frac{1}{n}\mathbf{J}_n$称为中心化矩阵
- 中心化矩阵既是对称矩阵，又是幂等矩阵，$\mathbf{C}_n=\mathbf{C}_n^{\top}=\mathbf{C}_n^2$

## 相似矩阵与相合矩阵

### 相似矩阵

- 矩阵$\mathbf{B} \in C^{n \times n}$称为矩阵$\mathbf{A} \in C^{n \times n}$的相似矩阵，若存在一非奇异矩阵$\mathbf{S} \in C^{n \times n}$使得$\mathbf{B}=\mathbf{S}^{-1}\mathbf{A}\mathbf{S}$
- 若$\mathbf{B}$与$\mathbf{A}$相似，则$\det(\mathbf{B})=\det(\mathbf{A})$、$tr(\mathbf{B})=tr(\mathbf{A})$和相同的特征值

### 相合矩阵

- 令$\mathbf{A},\mathbf{B},\mathbf{C} \in C^{n\times n}$，并且$\mathbf{C}$非奇异，则矩阵$\mathbf{B}=\mathbf{C}^H\mathbf{A}\mathbf{C}$称为$\mathbf{A}$的相合矩阵。

## Vandermonde 矩阵和 Fourier 矩阵

在信号处理有广泛应用

## Hadamard 矩阵

在通信、信息论和信号处理中一种重要的特殊矩阵

## Toeplitz 矩阵

Toeplitz 在研究与 Laurent 级数有关的双线性函数的一篇论文中提出的。

## Hankel 矩阵

正方矩阵$\mathbf{A} \in C^{(n+1)\times (n+1)}$称为 Hankel 矩阵，若

$$
\mathbf{A}=
\begin{bmatrix}
 a_{0} & a_{1} & a_{2} & ... & a_{n} \\
 a_{1} & a_{2} & a_{3} & ... & a_{n+1} \\
 a_{2} & a_{3} & a_{4} & ... & a_{n+2} \\
 ... & ... & ... & ... & ...\\
 a_{n} & a_{n+1} & a_{n+2} & ... & a_{2n}
\end{bmatrix}
$$