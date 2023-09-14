---
counter: True
comment: True
---

# 算法设计与分析

!!! abstract
    本科和研都选过这门课，特此来归档一下笔记
    
    （虽然都是打acm的时候学的 😂


## 算法引论

- 算法是满足下述性质的指令序列：
    1. 输入：有零个或多个外部量作为算法的输入。
    2. 输出：算法产生至少一个量作为输出。
    3. 确定性：组成算法的我条指令足清晰的，无歧义的。
    4. 有限性：算法中每条指令的执行次数有限，披行每条指令的时间世存限。
- 算法分析内容：
    - 运行时间：与机器和编译器有关
    - 时间复杂度、空间复杂度：与机器和编译器无关
- 复杂度分析假设：
    - 指令按顺序执行
    - 所有指令（运算）都消耗同一时间单元
    - 数据规模是给定的，且有无限空间
- 一般需要分析 $T_{\mathrm{avg}}(N)$（平均情况）和 $T_{\mathrm{worst}}(N)$（最差情况），$N$ 是输入的数据规模（也可以有多个输入规模）


## 复杂度渐进记号

### 定义
- 大 $O$ 表示法 $T(N) = O(f(N))$，如果存在常数 $c$ 和 $n_0$ 使得当 $N\geq n_0$ 时 $T(N)\leq c\cdot f(N)$
    - 渐进上界，即 $T(N)$ 的阶不会高于 $f(N)$（增长比 $f(N)$ 慢或相同，<=）
- 大 $\Omega$ 表示法 $T(N) = \Omega(g(N))$，如果存在常数 $c$ 和 $n_0$ 使得当 $N\geq n_0$ 时 $T(N)\geq c\cdot g(N)$
    - 渐进下界，即 $T(N)$ 的阶不会低于 $f(N)$（增长比 $f(N)$ 快或相同，>=） 
- 大 $\Theta$ 表示法 $T(N) = \Theta(h(N))$，当且仅当 $T(N) = O(h(N))$ 且 $T(N) = \Omega(h(N))$
    - 渐进紧确界，即 $T(N)$ 需要与 $h(N)$ 同阶（增长速度相同 =）
- 小 $o$ 表示法 $T(N) = o(p(N))$，当 $T(N) = O(p(N))$ 且 $T(N)\ne \Theta(p(N))$ 时
    - 非渐进紧确上界（$T(N)$ 增长比 $p(N)$ 慢，<）
- 小 $\omega$ 表示法 $T(N) = \omega(p(N))$，当 $T(N) = \Omega(q(N))$ 且 $T(N)\ne \Theta(q(N))$ 时
    - 非渐进紧确下界（$T(N)$ 增长比 $q(N)$ 快，>）

### 规则
- 如果 $T_1(N) = O(f(N))$ 且 $T_2(N) = O(g(N))$，则：
    - $T_1(N) + T_2(N) = \mathrm{max}(O(f(N)), O(g(N)))$
    - $T_1(N)\cdot T_2(N) = O(f(N)\cdot g(N))$
- 如果 $T(N)$ 是 $N$ 的 $k$ 次多项式，则 $T(N) = \Theta(N^k)$
- 对于任意常数 $k$ 均有 $\log^kN = O(N)$
- 大 O 记号比较：[Big O Cheat Sheet](https://www.bigocheatsheet.com/)
- 分析规则：
    - for 循环的运行时间是循环内部语句的最长时间（含 for 判断）乘循环次数
    - 嵌套 for 循环要逐次相乘
    - if else 语句的运行时间不超过判断时间+耗时最长的语句块的运行时间
- 补充：主定理。假设有 $T(n) = aT(n/b)+f(n)$（$a\geq 1, b>1$），则：
    - 如果存在常数 $\epsilon > 0$ 有 $f(n) = O(n^{\log_ba-\epsilon})$，则 $T(n) = \Theta(n^{\log_ba})$
    - 如果 $f(n) = \Theta(n^{\log_ba})$ 则 $T(n) = \Theta(n^{\log_ba}\log n)$
    - 如果存在常数 $\epsilon > 0$ 有 $f(n) = \Omega(n^{\log_ba+\epsilon})$，同时存在常数 $c<1$ 使得对于充分大 $n$ 有 $af(n/b)\leq cf(n)$ 则 $T(N) = \Theta(f(n))$


## 递归与分治

### 递归的概念

直接成间接地调用自身的算法称为递归算法。用函数自身给出定义的函数称为递归函数。

例如阶乘函数、斐波那契函数等等

$$
eg \ \ \ F(n) =
\left\{\begin{matrix}
1 & n = 0, 1 \\
F(n-1)+F(n-2) & n >= 1
\end{matrix}\right.
$$

```c++
int fibonacci(int n) {
    if (n <= 1) return 1;
    return fibonacci(n - 1) + fibonacci(n - 2);
}
```

- 对于小范围可以用记忆化$O(n)$的复杂度求解
- 对于大范围可以用矩阵快速幂$O(\log n)$的复杂度求解。

### 分治法思想

分治法的基本思想是将一个規模为$n$的问题分解为$k$个规模较小的子问题，这些子问题互相独立且与原问题相同。递门地解这些子问题，然后將各子问题的解合井得到原向题的解。

eg：快速幂、二分、归并排序、线段树、cdq分治、FFT等

### 大整数的乘法

有两个超过 long long 类型的大整数$X$和$Y$，用较低的复杂度求解$X*Y$。

解决这个问题至少有 6 种方法，可以看之前写过的文章：[大整数相乘 – 模拟/分治/FFT/CRT/网络流/Furer](http://www.jujimeizuo.cn/blog/index.php/2022/12/06/bigintegermultiply/)


## Reference

- [算法设计与分析(王晓东).pdf](https://github.com/jujimeizuo/cdn/blob/master/book/%E7%AE%97%E6%B3%95%E8%AE%BE%E8%AE%A1%E4%B8%8E%E5%88%86%E6%9E%90(%E7%8E%8B%E6%99%93%E4%B8%9C).pdf)