---
counter: true
---

# 矩阵微分

!!! abstract
    - 矩阵微分是多变量函数微分的推广，包括矩阵偏导和梯度。

    - 概念巨多且繁琐（还是建议看书吧

## Jacobian 矩阵与梯度矩阵

### Jacobian 矩阵

- $pq \times mn$维 Jacobian 矩阵

$$
D_{X}F(\mathbf{X}) \overset{def}{=}
\frac{\partial vec(F(\mathbf{X}))}{\partial (vec \mathbf{X})^\top} \in R^{pq \times mn}
$$

- 具体表达式为

$$
D_{X}F(\mathbf{X})=
\begin{bmatrix}
\frac{\partial f_{11}}{\partial (vec \mathbf{X})^\top} \\
... \\
\frac{\partial f_{p1}}{\partial (vec \mathbf{X})^\top} \\
...\\
\frac{\partial f_{1q}}{\partial (vec \mathbf{X})^\top} \\
...\\
\frac{\partial f_{pq}}{\partial (vec \mathbf{X})^\top} \\
\end{bmatrix}
=
\begin{bmatrix}
\frac{\partial f_{11}}{\partial x_{11}} & .. & \frac{\partial f_{11}}{\partial x_{m1}} & .. & \frac{\partial f_{11}}{\partial x_{1n}} & .. & \frac{\partial f_{11}}{\partial x_{mn}} \\
... & .. & ... & .. & ... & .. & ... \\
\frac{\partial f_{p1}}{\partial x_{11}} & .. & \frac{\partial f_{p1}}{\partial x_{m1}} & .. & \frac{\partial f_{p1}}{\partial x_{1n}} & .. & \frac{\partial f_{p1}}{\partial x_{mn}} \\
... & .. & ... & .. & ... & .. & ... \\
\frac{\partial f_{1q}}{\partial x_{11}} & .. & \frac{\partial f_{1q}}{\partial x_{m1}} & .. & \frac{\partial f_{1q}}{\partial x_{1n}} & .. & \frac{\partial f_{1q}}{\partial x_{mn}} \\
... & .. & ... & .. & ... & .. & ... \\
\frac{\partial f_{pq}}{\partial x_{11}} & .. & \frac{\partial f_{pq}}{\partial x_{m1}} & .. & \frac{\partial f_{pq}}{\partial x_{1n}} & .. & \frac{\partial f_{pq}}{\partial x_{mn}} \\
\end{bmatrix}
$$

### 梯度矩阵

- 定义梯度矩阵

$$
\nabla_\mathbf{X} f(\mathbf{X})=
\begin{bmatrix}
\frac{\partial f(\mathbf{X})}{\partial x_{11}} & ... & \frac{\partial f(\mathbf{X})}{\partial x_{1n}} \\
... & ... & ... \\
\frac{\partial f(\mathbf{X})}{\partial x_{m1}} & ... & \frac{\partial f(\mathbf{X})}{\partial x_{mn}} \\
\end{bmatrix}
=
\frac{\partial f(\mathbf{X})}{\partial \mathbf{X}}
$$

- 矩阵函数的梯度矩阵是其 Jacobian 矩阵的转置：$\nabla_\mathbf{X} F(\mathbf{X})=(D_\mathbf{X} F(\mathbf{X}))^\top$

### 偏导和梯度计算

- 矩阵变元的梯度计算和标量变元的梯度计算类似，只是矩阵变元的梯度是矩阵，而标量变元的梯度是向量，都满足线性、乘积、商、链式法则

## 一阶实矩阵微分与 Jacobian 矩阵辨识

### 一阶实矩阵微分

- 矩阵微分用符号$d\mathbf{X}$表示，定义为$d\mathbf{X}=[dX_{ij}]_{i=1,j=1}^{m,n}$

- 标量函数的 Jacobian 矩阵辨识
- 实值矩阵函数的 Jacobian 矩阵辨识

## 二阶实矩阵微分与 Hessian 矩阵辨识

### Hessian 矩阵

- 实值函数$f(x)$相对于$m \times 1$实向量$x$的二阶偏导称为 Hessian 矩阵，记作$H[f(x)]$，定义为

$$
H[f(x)]=\frac{\partial^2 f(x)}{\partial x \partial x^\top}=\frac{\partial}{\partial x}[\frac{\partial f(x)}{\partial x^\top}] \in R^{m \times m} \\
或 \\
H[f(x)]=\frac{\partial^2 f(x)}{\partial x \partial x^\top}=
\begin{bmatrix}
\frac{\partial^2 f}{\partial x_1 \partial x_1} & ... & \frac{\partial^2 f}{\partial x_1 \partial x_m} \\
... & ... & ... \\
\frac{\partial^2 f}{\partial x_m \partial x_1} & ... & \frac{\partial^2 f}{\partial x_m \partial x_m} \\
\end{bmatrix}
\in R^{m \times m}
$$

### Hessian 矩阵的辨识原理

- 标量函数 $f(x)$ 的 Hessian 矩阵辨识
- 标量函数 $f(\mathbf{X})$ 的 Hessian 矩阵辨识

### Hessian 矩阵的辨识方法

## 共轭梯度与复 Hessian 矩阵


