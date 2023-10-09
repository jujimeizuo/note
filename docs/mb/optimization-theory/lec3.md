---
counter: true
comment: true
---

# 无约束最优化的梯度方法

!!! abstract
    - 本章开始讨论多维最优化问题和无约束最优化问题，其一般形式为

        $$
        \min f(\mathbf{x})
        $$


## 最速下降法

- **基本想法**
    - 假定已经迭代了 k 次，获得了第 k 个迭代点 $\mathbf{x}_k$，从 $\mathbf{x}_k$ 出发，显然应该沿最俗下降方向（即负梯度方向）行进，取搜索方向

    $$
    \mathbf{p}_k = - \nabla f(\mathbf{x}_k)
    $$

    - 由此得到第 $k+1$ 迭代点 $\mathbf{x}_{k+1}$，即

    $$
    \mathbf{x}_{k+1}=\mathbf{x}_k - t_k \nabla f(\mathbf{x}_k)
    $$

    - 其步长因子 $t_k$ 满足

    $$
    f(\mathbf{x}_k - t_k \nabla f(\mathbf{x}_k)) = \min f(\mathbf{x}_k - t \nabla f(\mathbf{x}_k))
    $$

    - 总结上式，得到最速下降法的迭代公式

    $$
    \mathbf{x}_{k+1} = ls(\mathbf{x}_k, - \nabla f(\mathbf{x}_k))
    $$

- **算法**
    - 已知：目标函数 $f(\mathbf{x})$ 及其梯度 $\mathbf{g}(\mathbf{x})$，H 终止准则所需要的终止限 $\varepsilon_1, \varepsilon_2$ 和 $\varepsilon_3$

    1. 选定初始点 $\mathbf{x}_0$，计算 $f_0=f(\mathbf{x}_0), \mathbf{g}_0 = \mathbf{g}(\mathbf{x}_0)$，置 $k=0$
    2. 作直线搜索：$\mathbf{x}_{k+1}=ls \cdot (\mathbf{x}_k, -\mathbf{g}_k)$；计算 $f_{k+1}=f(\mathbf{x}_{k+1}), \mathbf{g}_{k+1}=\mathbf{g}(\mathbf{x}_{k+1})$
    3. 判别 H 终止准则是否满足；若满足，则打印最优解 $\mathbf{x}_{k+1},f_{k+1}$，停机；否则，置 $k=k+1$，转 2

- **应用于正定二次函数 $f(\mathbf{x})=\frac{1}{2} \mathbf{x}^\top \mathbf{Q} \mathbf{x} + \mathbf{b}^\top \mathbf{x} + c$**
    - 设第 $k$ 次的迭代点为 $\mathbf{x}_k$，求 $\mathbf{x}_{k+1}$ 的表达式
    
    $$
    \mathbf{x}_{k+1} = \mathbf{x}_k - \frac{\mathbf{g}_k^\top \mathbf{g}_k}{\mathbf{g}_k^\top \mathbf{Q} \mathbf{g}_k} \mathbf{g}_k
    $$

## Newton 法

- **基本想法**
    - 考虑从 $\mathbf{x}_k$ 到 $\mathbf{x}_{k+1}$ 的迭代过程。在 $\mathbf{x}_k$ 点处对 $f(\mathbf{x})$ 用与它最密切的二次函数来近似，这只须把 $f(\mathbf{x}$ 按 Taylor 展开，直到第三项，即

    $$
    f(\mathbf{x}) \approx Q(\mathbf{x}) = f(\mathbf{x}_k) + \mathbf{g}(\mathbf{x}_k)^\top (\mathbf{x} - \mathbf{x}_k)+\frac{1}{2}(\mathbf{x}-\mathbf{x}_k)^\top \mathbf{G}(\mathbf{x}_k)(\mathbf{x}-\mathbf{x}_k)
    $$

    - 令 $\nabla Q(\mathbf{x})=\mathbf{G}(\mathbf{x}_k)(\mathbf{x}-\mathbf{x}_k)+\mathbf{g}(\mathbf{x}_k)=0$，得

    $$
    \mathbf{x}_{k+1} = \mathbf{x}_k - \mathbf{G}(\mathbf{x}_k)^{-1}\mathbf{g}(\mathbf{x}_k)
    $$

- **算法**
    - 已知：目标函数 $f(\mathbf{x})$ 及其梯度 $\mathbf{g}(\mathbf{x})$，Hesse 矩阵 $\mathbf{G}(\mathbf{x})$，H 终止准则所需要的终止限 $\varepsilon_1, \varepsilon_2$ 和 $\varepsilon_3$

    1. 选定初始点 $\mathbf{x}_0$；计算 $f_0 = f(\mathbf{x}_0), \mathbf{g}_0=\mathbf{g}(\mathbf{x}_0)$；置 $k=0$
    2. 计算 $\mathbf{G}_k=\mathbf{G}(\mathbf{x}_k)$
    3. 由方程 $\mathbf{G}_k \mathbf{p}=-\mathbf{g}_k$ 解出 $\mathbf{p}_k$
    4. 计算 $\mathbf{x}_{k+1}=\mathbf{x}_k + \mathbf{p}_k$，$f_{k+1}=f(\mathbf{x}_{k+1})$，$\mathbf{g}_{k+1}=\mathbf{g}(\mathbf{x}_{k+1})$
    5. 判别 H 终止准则是否满足；若满足，则打印最优解 $\mathbf{x}_{k+1},f_{k+1}$，停机；否则，置 $k=k+1$，转 2


## 共轭方向法与共轭梯度法

- **基本想法**
    - 首先考虑二维的情况，把下降法用于二元二次函数，任选初始点 $\mathbf{x}_0$，沿某个下降方向，例如向量 $\mathbf{p}_0$ 的方向，作直线搜索得到 $\mathbf{x}_1$：$\nabla f(\mathbf{x}_1)^\top \mathbf{p}_0=0$
    - 将下一次迭代的搜索方向指向极小点 $\mathbf{x}^*$，推导得到 $\mathbf{p}_0^\top \mathbf{Q} \mathbf{p}_1 = 0$，，这里的 $\mathbf{p}_0$ 和 $\mathbf{p}_1$ 称为 $\mathbf{Q}$ 共轭向量，或称 $\mathbf{p}_0$ 和 $\mathbf{p}_1$ 的方向是共轭方向

    $$
    \mathbf{p}_1 = - \nabla f(\mathbf{x}_1) + \frac{\mathbf{p}_0^\top \mathbf{Q} \nabla f(\mathbf{x}_1)}{\mathbf{p}_0^\top \mathbf{Q} \mathbf{p}_0} \mathbf{p}_0
    $$

- **向量的共轭及其性质**
    - 若非零向量系 $\mathbf{p}_0, \mathbf{p}_1, ..., \mathbf{p}_{m+1}$ 是 $\mathbf{Q}$ 共轭的，则这 m 个向量线性无关
    - 在 n 维空间中，互相共轭的非零向量的向量个数不超过 n

- **共轭方向法**
    - 已知：具有正定矩阵 $\mathbf{Q}$ 的二次目标函数 $f(\mathbf{x})=\frac{1}{2} \mathbf{x}^\top \mathbf{Q} \mathbf{x} + \mathbf{b}^\top \mathbf{x}+c$ 和终止限 $\varepsilon$

    1. 选定初始点 $\mathbf{x}_0$ 和具有下降方向的向量 $\mathbf{p}_0$；置 $k=0$
    2. 作直线搜索 $\mathbf{x}_{k+1}=ls(\mathbf{x}_k. \mathbf{p}_k)$
    3. 判别 $\parallel \nabla f(\mathbf{x}_{k+1}) \parallel < \varepsilon$ 是否满足：若满足，则打印 $\mathbf{x}_{k+1}$，停机，否则转 4
    4. 提供共轭方向 $\mathbf{p}_{k+1}$ 使得 $\mathbf{p}_j^\top \mathbf{Q} \mathbf{p}_{k+1} = 0, \ \ \ j=0,1,...,k$
    5. $k = k + 1$，转 2

- **共轭梯度法**
    - 已知：具有二次目标函数 $f(\mathbf{x})=\frac{1}{2} \mathbf{x}^\top \mathbf{Q} \mathbf{x} + \mathbf{b}^\top \mathbf{x}+c$ 和终止限 $\varepsilon$

    1. 选定初始点 $\mathbf{x}_0$，计算 $\mathbf{p}_0 = -\nabla f(\mathbf{x}_0)$，置 $k=0$
    2. 作直线搜索 $\mathbf{x}_{k+1}=ls(\mathbf{x}_k,\mathbf{p}_k)$，或采取计算公式 $t_k=\frac{\nabla f(\mathbf{x}_k)^\top \nabla f(\mathbf{x}_k)}{\mathbf{p}_k^\top \mathbf{Q} \mathbf{p}_k}$，$\mathbf{x}_{k+1}=\mathbf{x}_k + t_k\mathbf{p}_k$
    3. 判别 $\parallel \nabla f(\mathbf{x}_{k+1}) \parallel < \varepsilon$ 是否满足：若满足，则打印 $\mathbf{x}_{k+1}$，停机，否则转 4
    4. 计算 $\alpha_k = \frac{\nabla f(\mathbf{x}_{k+1}^\top \mathbf{Q} \mathbf{p}_k)}{\mathbf{p}_k^\top \mathbf{Q} \mathbf{p}_k}$，$\mathbf{p}_{k+1}=-\nabla f(\mathbf{x}_{k+1})+\alpha_k \mathbf{p}_k$
    5. $k=k+1$，转 2


## 变尺度法

- **基本想法**：略
- **DFP 算法**
    - 已知：目标函数 $f(\mathbf{x})$ 及其梯度 $\mathbf{g}(\mathbf{x_0})$，问题的维度 n，H 终止准则中的终止限 $\varepsilon_1, \varepsilon_2$ 和 $\varepsilon_3$

    1. 选定初始点 $\mathbf{x}_0$，计算 $f_0=f(\mathbf{x}_0),\mathbf{g}_0=\mathbf{g}(\mathbf{x}_0)$
    2. 置 $\mathbf{H}_0=\mathbf{I},\mathbf{p}_0=-\mathbf{g}_0,k=0$
    3. 作直线搜索 $\mathbf{x}_{k+1}=ls(\mathbf{x}_k, \mathbf{p}_k)$，计算 $f_{k+1}=f(\mathbf{x}_{k+1}),\mathbf{g}_{k+1}=\mathbf{g}(\mathbf{x}_{k+1})$
    4. 判别 H 终止准则是否满足：若满足，则打印 $\mathbf{x}_{k+1},f_{k+1}$，停机；否则，转 5
    5. 若 $k=n$，则置 $\mathbf{x}_0 = \mathbf{x}_{k+1}, f_0=f_{k+1}, \mathbf{g}_0 = \mathbf{g}_{k+1}$，转 2；否则转 6
    6. 计算 $\mathbf{y}_k=\mathbf{g}_{k+1}-\mathbf{g}_k, \mathbf{s}_k = \mathbf{x}_{k+1}-\mathbf{x}_k, \mathbf{H}_{k+1}=\mathbf{H}_k+\frac{\mathbf{s}_k\mathbf{s}_k^\top}{\mathbf{s}_k^\top \mathbf{y}_k} - \frac{\mathbf{H}_k \mathbf{y}_k \mathbf{y}_k^\top \mathbf{H}_k}{\mathbf{y}_k^\top \mathbf{H}_k \mathbf{y}_k},\mathbf{p}_{k+1}=-\mathbf{H}_{k+1}\mathbf{g}_{k+1}$，置 $k=k+1$，转 3


## 最小二乘问题的解法

### 线性最小二乘问题

- 当 $f(\mathbf{x})$ 取线性函数形式时，即 $f(\mathbf{x})=A \mathbf{x} - \mathbf{b}$，其中 A 是 $m \times n$ 矩阵，b 是 m 维向量，此时线性最小二乘问题即

$$
\min \parallel A \mathbf{x} - \mathbf{b} \parallel^2
$$

- $\mathbf{x}^*$ 的极小点当且仅当 $\mathbf{x}^*$ 满足方程 $A^\top A \mathbf{x}=A^\top \mathbf{b}$
- 设 A 是 $m \times n$ 矩阵 $(m \ge n)$，则 $A^\top A$ 正定的充要条件是 A 的秩为 n
- 当 A 的秩为 n 时，则 $\mathbf{x}=(A^\top A)^{-1} A^\top \mathbf{b}$ 是唯一最小二乘解
- 设 A 是 $m \times n$ 矩阵 $(m \ge n)$，则 $A^\top A$ 正定的充要条件是 $A^\top A$ 为非奇异

### Gauss-Newton 法

- 讨论以 $s(\mathbf{x})=f(\mathbf{x})^\top f(\mathbf{x})=\parallel f(\mathbf{x}) \parallel^2$ 为目标函数的非线性最小二乘问题的解法
- 把 $f(\mathbf{x})$ 线性化，用线性最小二乘问题的解去逼近非线性最小二乘问题的解
- 算法流程
    - 已知：$f(\mathbf{x})=[f_1(\mathbf{x}), ..., f_m(\mathbf{x})]^\top$ 及其 Jacobi 矩阵 $A(\mathbf{x})=[\frac{\partial f_i(\mathbf{x})}{\partial x_j}]$

    1. 选定初始点 $\mathbf{x}_0$；计算 $s_0=\sum_{i=1}^m f_i^m (\mathbf{x}_0)$；置 $k=0$
    2. 对 $i=1,...,m$ 和 $j=1,...,n$ 计算 $a_{ij}^{(k)}=\frac{\partial f_i(\mathbf{x}_k)}{\partial x_j}$。由此构成矩阵 $A_k$，它的第 i 行和第 j 列分量是 $a_{ij}^{(k)}$，对 $j=1,...,n$ 计算 $g_j^{(k)}=\sum_{i=1}^m f_i(\mathbf{x}_k) \frac{\partial f_i(\mathbf{x_k})}{\partial x_j}$。由此构成向量 $\mathbf{g}_k$，它的第 j 个分量是 $g_j^{(k)}$
    3. 由方程组 $A_k^\top A_k \mathbf{p}=-\mathbf{g}_k$ 解出 $\mathbf{p}$，设为 $\mathbf{p}_k$。在求解过程中，仅当 $r(A_k^\top A_k)=n$ 时才能解得出 $\mathbf{p}_k$
    4. 若在求解过程中发现 $r(A_k^\top A_k)<n$，则取 $\mathbf{p}_k=-\mathbf{g}_k$
    5. 对 $s(\mathbf{x})$ 作直线搜索 $\mathbf{x}_{k+1}=ls(\mathbf{x}_k, \mathbf{p}_k)$，然后计算 $s_{k+1}=\sum_{i=1}^m f_i^2(\mathbf{x}_{k+1})$
    6. 若 H 终止准则满足，则 $\mathbf{x}_{k+1}$ 就是所求的最小二乘解，打印，停机
    7. 置 $k=k+1$，转 2