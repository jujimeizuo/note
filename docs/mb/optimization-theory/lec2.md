---
counter: True
---

# 直线搜索

!!! abstract
    本章主要讨论的问题是$\min{(\varphi (t))}，\varphi: R^1 \to R^1$，这种迭代方法称为直线/一维搜索。并且在多维问题也能用到。


## 搜索区间的确定

- 假设一元函数$\varphi (t)$是单谷函数
    - 设$\varphi \subset R^1 \to R^1$，$t^*$是$\varphi (t)$在$L$上的全局最小点。如果对于$L$上任取的两点$t_1, t_2$且$t_1 < t_2$都有

    $$
    当t_2 \le t^*时，\varphi(t_1) > \varphi(t_2) \\
    当t_1 \ge t^*时，\varphi(t_1) < \varphi(t_2)
    $$

    则称$\varphi(t)$是区间$L$上的单谷函数。

    - 设$\varphi \subset R^1 \to R^1$，$t^*$是$\varphi (t)$在$L$上的全局最小点。如果找到$t_1 \in L$和$t_2 \in L$使得 $t_1 < t^* < t_2$，则$[t_1, t_2]$为$\varphi(t)$极小点的一个搜索区间，记为$\{t_1, t_2\}$。
    - 设$\{a,b\}$是单谷函数$\varphi(t)$极小点的一个搜索区间。在$(a,b)$上任取两点$t_1$和$t_2$且$t_1<t_2$。若$\varphi(t_1) < \varphi(t_2)$，则$\{a,t_2\}$是$\varphi(t)$极小点的一个搜索空间；若$\varphi(t_1) > \varphi(t_2)$，则$\{t_1, b\}$是$\varphi(t)$极小点的一个搜索空间。

- 搜索区间的确定

    1. 选定初始点$t_0$和步长$h$
    2. 计算并比较$\varphi(t_0)$和$\varphi(t_0+h)$，有 3，4 两种情况
    3. 当$\varphi(t_0)<\varphi(t_0+h)$时，比较$\varphi(t_0)$和$\varphi(t_0-h)$，有 5，6 两种情况
    4. 当$\varphi(t_0)\ge\varphi(t_0+h)$时，比较$\varphi(t_0+(2^k-1)^h), k=1,2,...$，直到对于某个$m(m \ge 1)$使得

    $$
    \varphi(t_0+(2^{m-1}-1)^h) \ge \varphi(t_0+(2^m-1)^h) < \varphi(t_0+(2^{m+1}-1)^h) \\
    设 \ \ u=\varphi(t_0+(2^{m-1}-1)^h), v=\varphi(t_0+(2^{m}-1)^h), w=\varphi(t_0+(2^{m+1}-1)^h)
    $$

    此时得到搜索区间$\{u,v,w\}$，因为区间$[v,w]$是$[u,v]$的两倍长，所以只要比较$v$和区间$[v,w]$中点$r=\frac{v+w}{2}$的函数值，立刻可以将$[u,w]$缩短$\frac{1}{3}$
    
     - 当$\varphi(v) < \varphi(r)$时，取$\{u,v,r\}$为搜索区间
     - 当$\varphi(v) \ge \varphi(r)$时，取$\{v,r,w\}$为搜索区间

    5. 当$\varphi(t_0-h) > \varphi(t_0)$时，取$\{t_0-h,t_0,t_0+h\}$为搜索区间
    6. 当$\varphi(t_0-h)\le\varphi(t_0)$时，比较$\varphi(t_0-(2^k-1)^h), k=1,2,...$，直到对于某个$m(m \ge 1)$使得

    $$
    \varphi(t_0-(2^{m-1}-1)^h) \ge \varphi(t_0-(2^m-1)^h) < \varphi(t_0-(2^{m+1}-1)^h) \\
    设 \ \ u=\varphi(t_0-(2^{m-1}-1)^h), v=\varphi(t_0-(2^{m}-1)^h), w=\varphi(t_0-(2^{m+1}-1)^h)
    $$

    此时得到搜索区间$\{u,v,w\}$，因为区间$[v,w]$是$[u,v]$的两倍长，所以只要比较$v$和区间$[v,w]$中点$r=\frac{v+w}{2}$的函数值，立刻可以将$[u,w]$缩短$\frac{1}{3}$
    
     - 当$\varphi(v) \ge \varphi(r)$时，取$\{w,r,v\}$为搜索区间
     - 当$\varphi(v) < \varphi(r)$时，取$\{r,v,u\}$为搜索区间

- **步长的选择**


## 对分法

- 适用于$\varphi: R^1 \to R^1$在已获得的搜索区间$\{a,b\}$内具有连续的一阶导数，并且已导出它的表达式
- 算法流程（已知$\varphi(t)$和$\varphi^\prime(t)$的表达式，终止限$\varepsilon$）
    1. 确定初始搜索区间$\{a,b\}$，要求$\varphi^\prime(a)<0,\varphi^\prime(b)>0$
    2. 计算$\{a,b\}$的中点$c=0.5(a+b)$
    3. 若$\varphi^\prime(c)<0$，则$a=c$，转 4；若$\varphi^\prime(c)=0$，则$t^*=c$，转 5；若$\varphi^\prime(c)>0$，则$b=c$，转4
    4. 若$|a-b|<\varepsilon$，则$t^*=0.5(a+b)$，转 5，否则转 2
    5. 打印$t^*$，停机


## Newton 切线法

- 适用于$\varphi: R^1 \to R^1$在已获得的搜索区间$\{a,b\}$内具有连续的二阶导数，并且已导出一阶和二阶导数的表达式
- 算法流程
    1. 设在区间$[a,b]$中经过$k$次迭代已求到方程$\varphi^\prime(t)=0$的一个近根似$t_k$。过$(t_k,\varphi^\prime(t_k))$作曲线$y=\varphi^\prime(t)$的切线，其方程是

    $$
    y-\varphi^\prime(t_k)=\varphi^{\prime\prime}(t_k)(t-t_k)
    $$

    2. 然后用这条切线与横轴交点的横坐标$t_{k+1}$作为根的新的近似，令$y=0$解出

    $$
    t_{k+1}=t_k-\varphi^\prime(t_k)/\varphi^{\prime\prime}(t_k)
    $$


## 黄金分割法

- 适用于$[a,b]$区间上的任何单谷函数$\varphi(t)$求极小点问题
- 算法流程（已知$\varphi(t)$，终止限$\varepsilon$）
    1. 确定$\varphi(t)$的初始搜索区间$\{a,b\}$
    2. 计算$t_2=a+\beta(b-a), \varphi_2=\varphi(t_2)$
    3. 计算$t_1=a+b-t_2, \varphi_1=\varphi(t_1)$
    4. 若$|t_1-t_2|<\varepsilon$，则打印$t^\prime=\frac{t_1+t_2}{2}$，停机；都则，若$|t_1-t_2| \ge \varepsilon$，转 5
    5. 判别$\varphi_1 \le \varphi_2$是否满足：若满足，则置$b=t_2,t_2=t_1,\varphi_2=\varphi_1$，然后转 3；否则，若$\varphi_1>\varphi_2$，则置$a=t_1,t_1=t_2,\varphi_1=\varphi_2,t_2=a+\beta(b-a),\varphi_2=\varphi(t_2)$，然后转4