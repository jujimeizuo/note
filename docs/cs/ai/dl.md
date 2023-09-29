---
counter: True
comment: True
---

# 神经网络与深度学习

!!! abstract
    学习自 [邱锡鹏老师](https://nndl.github.io/) 的神经网络与深度学习，归档一些学习笔记。


## 概述

神经网络与深度学习是人工智能的一个子领域

- 神经网络：一种以（人工）神经元为基本单元的模型
- 深度学习：一类机器学习问题，主要解决贡献度分配问题。

<center>![总结概括](https://cdn.jujimeizuo.cn/note/cs/ai/dl/summary.jpg)</center>

## 机器学习概述

转移到 [机器学习](../ml)


## 线性模型

<center>![线性模型](https://cdn.jujimeizuo.cn/note/cs/ai/dl/linear-model.jpg)</center>

### 应用

- 图像分类
- 文本文类

### 感知器

- 模型

$$
g(x,w)=
\left\{\begin{matrix}
+1  & 当w^{\top}x>0  \\
-1  & 当w^{\top}x<0
\end{matrix}\right.
$$

- 学习准则

$$
L(w;x,y)=\max{(0,-yw^{\top}x)}
$$

- 优化：随机梯度下降

$$
\frac{\partial L(w;x,y)}{\partial w}=
\left\{\begin{matrix}
0  & 当yw^{\top}x>0  \\
-yx  & 当yw^{\top}x<0
\end{matrix}\right.
$$

### 两类感知器算法

<center>![两类感知器算法](https://cdn.jujimeizuo.cn/note/cs/ai/dl/perceptron-flow.jpg)</center>


## Reference

- [邱锡鹏,神经网络与深度学习,机械工业出版社, 2020，ISBN 9787111649687](https://nndl.github.io/)
- [阿斯顿·张等,动手学深度学习, ISBN: 9787115505835](https://d2l.ai/)