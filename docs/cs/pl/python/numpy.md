---
counter: True
comment: True
---

# Numpy 科学计算库

!!! abstract
    在学习 Python，尤其是机器学习领域，最基础的 Numpy 十分重要，提供一个强大的科学计算环境，所以必须要熟练掌握。

    Numpy 通常与 SciPy(Scientific Python) 和 Matplotlib(绘图库) 一起食用，相当于替代了 MatLab。



## ndarray

### 属性
- Numpy 的主要对象时同构多维数组。它是一个元素表（通常是数字），所有类型都相同，由非负整数元组索引。在 Numpy 维度中称为**轴**。
- Numpy 的数组类被调用`ndarray`，别名为 `array`，但和 Python 的`array.array` 区别很大
    - `ndarray.ndim`: 数组的轴（维度）的个数，也被称 rank
    - `ndarray.shape`: 数组的维度。一个整数的元祖，表示每个维度中数组的大小，shape 的长度就是 rank 或维度的个数 ndim
    - `ndarray.size`: 数组元素的总数，等于 shape 元素的乘积
    - `ndarray.dtype`: 描述数组中元素类型的对象。可以使用标准的 Python 类型创建或指定 dtype，也可以用 Numpy 提供的例如`numpy.int32, numpy.float64`等
    - `ndarray.itemsize`: 数组中每个元素的字节大小，例如 `float64`的 itemsize 就是 64/8=8，等于 `ndarray.dtype.itemsize`
    - `ndarray.data`: 该缓冲区包含数组的实际元素，通常不使用，只需要通过索引访问

??? example "element in ndarray"
    ```Python
    >>> import numpy as np
    >>> a = np.arange(15).reshape(3, 5)
    >>> a
    array([[ 0,  1,  2,  3,  4],
        [ 5,  6,  7,  8,  9],
        [10, 11, 12, 13, 14]])
    >>> a.shape
    (3, 5)
    >>> a.ndim
    2
    >>> a.dtype.name
    'int64'
    >>> a.itemsize
    8
    >>> a.size
    15
    >>> type(a)
    <type 'numpy.ndarray'>
    >>> b = np.array([6, 7, 8])
    >>> b
    array([6, 7, 8])
    >>> type(b)
    <type 'numpy.ndarray'>
    ```

### 数组创建

- `a=np.array([2,3,4])`:从 Python 列表或元组中创建数组（类型推导）
- `b=np.array([(1,2,3),(4,5,6)])`: 可以将序列的序列转换成二维数组，甚至高维数组
- `c=np.array([[],[]], dtype=complex)`: 创建时可以显式指定数组的类型 `dtype=complex`
- 占位符数组（默认情况下的 `dtype` 都是 `float64`）
    - `np.zero()`: 创建一个由 0 组成的数组
    - `np.ones()`: 创建一个由 1 组成的数组
    - `np.empty()`: 创建一个数组，内容随机（取决于内存状态）
- `np.arange()`，创建数字组成的数组，类似于 `range` 的函数
    - 当与浮点参数一起使用时，最好使用 `linspace` 函数接受想要的元素数量的函数，而不是步长 `step`

### 打印数组

Numpy 以嵌套列表类似的方式显示，有以下布局

- 最后一个轴从左到右打印
- 倒数第二个从上到下打印
- 其余部分从上到下打印，每个切片用空行隔开

当数组太大而无法打印时，Numpy 会自动跳过数组的中心部分并仅打印角点。要禁用此行为并强制NumPy打印整个数组，可以使用更改打印选项 `set_printoptions`

??? example "print array"
    ```Python
    >>> a = np.arange(6)                         # 1d array
    >>> print(a)
    [0 1 2 3 4 5]
    >>>
    >>> b = np.arange(12).reshape(4,3)           # 2d array
    >>> print(b)
    [[ 0  1  2]
    [ 3  4  5]
    [ 6  7  8]
    [ 9 10 11]]
    >>>
    >>> c = np.arange(24).reshape(2,3,4)         # 3d array
    >>> print(c)
    [[[ 0  1  2  3]
    [ 4  5  6  7]
    [ 8  9 10 11]]
    [[12 13 14 15]
    [16 17 18 19]
    [20 21 22 23]]]
    >>>
    >>> print(np.arange(10000))                  # 10000d array
    [   0    1    2 ..., 9997 9998 9999]
    >>>
    >>> print(np.arange(10000).reshape(100,100))
    [[   0    1    2 ...,   97   98   99]
    [ 100  101  102 ...,  197  198  199]
    [ 200  201  202 ...,  297  298  299]
    ...,
    [9700 9701 9702 ..., 9797 9798 9799]
    [9800 9801 9802 ..., 9897 9898 9899]
    [9900 9901 9902 ..., 9997 9998 9999]]
    >>>
    >>> np.set_printoptions(threshold=sys.maxsize)       # sys module should be imported
    ```


### 基本操作

- 数组上的算数运算符会应用到元素级别
- 乘法 `*` 在 array 中按元素进行运算，矩阵乘法可以用 `@` 或 `dot` 函数进行运算
- 某些操作例如 `+=、*=` 会直接更改被操作的矩阵数组而不会创建新矩阵数组
- 当使用不同类型的数组进行操作时，结果数组的类型对应于更一般或更精确的数组（称为向上转换的行为）
- 许多一元操作，例如计算数组中所有元素的总和，都是作为 `ndarray` 类的方法实现的
    - `min()`
    - `max()`
    - `sum()`
- 通过指定 `axis` 参数，可以沿数组的指定轴应用操作


### 通函数

NumPy 提供熟悉的数学函数，例如 `sin`，`cos` 和 `exp`。在 NumPy 中，这些被称为“通函数”（ufunc）。在 NumPy 中，这些函数在数组上按元素进行运算，产生一个数组作为输出。


### 索引、切片和迭代

- 一维的数组可以进行索引、切片和迭代操作的，就像 列表 和其他 Python 序列类型一样
- 多维的数组每个轴可以有一个索引。这些索引以逗号​​分隔的元组给出
- 当提供的索引少于轴的数量时，缺失的索引被认为是完整的切片
- 可以使用 `...` 表示产生完整索引元组所需的冒号（剩余轴），用来替代 `:`
    - 例如 x 是 rank 为 5 的数组
    - `x[1,2,...]` = `x[1,2,:,:,:]`
    - `x[...,3]` = `x[:,:,:,:,3]`
    - `x[4,...,5,:]` = `x[4,:,:,5,:]`
- 对多维数组进行 迭代（Iterating） 是相对于第一个轴完成的
- 如果想要对数组中的每个元素执行操作，可以使用 `flat` 属性，该属性是数组的所有元素的迭代器

## 形状操纵

### 改变数组形状

- `a.shape()`: 查看数组的形状
- `ravel()`: 将数组平坦并返回修改后的数组
- `reshape(i, j, ...size)`: 将数组的轴改成 (i,j,..)，返回修改后的数组，如果 size 指定为 -1，则会自动计算其他的 size 大小
- `resize(i, j, ...)`: 将数组的轴改成 (i,j,..)，修改数组本身
- `T`: 将数组转置

### 将不同数组堆叠

- `vstack(a,b,...)`: 将数组 a，b，... 按顺序垂直堆叠
- `hstack(a,b,...)`: 将数组 a，b，... 按顺序横向堆叠
- `coulumn_stack`: 1D 数组作为列堆叠到 2D 数组中，相当于 hstack 2D 数组
- `row_stack`: 等效于 vstack 于任何输入数组
- `r_、c_`: 通过沿一个轴堆叠数组来创建数组，可以使用范围为操作符 :

### 将一个数组拆分成几个较小的数组

- `hsplit()`: 可以沿数组的水平轴拆分数组，方法是指定要返回的形状相等的数组的数量，或者指定应该在其之后进行分割的列
- `vsplit()`: 沿垂直轴分割

### 拷贝和视图

#### 完全不复制

- 简单分配不会复制数组对象或其数据
- Python将可变对象作为引用传递，因此函数调用不会复制

#### 视图或浅拷贝

- 不同的数组对象可以共享相同的数据
- `view()`: 创建一个查看相同数据的新数组对象
- 切片数组会返回一个视图

#### 深拷贝

- `copy()`: 生成数组及其数据的完整副本
- 如果不再需要原始数组，则应在切片后调用 `copy()`

### 广播

- 广播(Broadcast)是 numpy 对不同形状(shape)的数组进行数值计算的方式， 对数组的算术运算通常在相应的元素上进行
- 如果两个数组 a 和 b 形状相同，即满足 a.shape == b.shape，那么 a*b 的结果就是 a 与 b 数组对应位相乘
- 当运算中的 2 个数组的形状不同时，numpy 将自动触发广播机制
- 规则: 对两个数组，分别比较他们的每一个维度（若其中一个数组没有当前维度则忽略）
    - 数组拥有相同形状
    - 当前维度的值相等
    - 当前维度的值有一个是 1
- 若条件不满足，抛出 "ValueError: frames are not aligned" 异常


## 索引技巧

### 整数数组索引

整数数组索引是指使用一个数组来访问另一个数组的元素。这个数组中的每个元素都是目标数组中某个维度上的索引值。

```python
>>> a = np.arange(12)**2                       # the first 12 square numbers
>>> i = np.array( [ 1,1,3,8,5 ] )              # an array of indices
>>> a[i]                                       # the elements of a at the positions i
array([ 1,  1,  9, 64, 25])
>>>
>>> j = np.array( [ [ 3, 4], [ 9, 7 ] ] )      # a bidimensional array of indices
>>> a[j]                                       # the same shape as j
array([[ 9, 16],
       [81, 49]])
```

### 布尔数组索引

布尔索引通过布尔运算（如：比较运算符）来获取符合指定条件的元素的数组

```python
>>> a = np.arange(12).reshape(3,4)
>>> b = a > 4
>>> b                                          # b is a boolean with a's shape
array([[False, False, False, False],
       [False,  True,  True,  True],
       [ True,  True,  True,  True]])
>>> a[b]                                       # 1d array with the selected elements
array([ 5,  6,  7,  8,  9, 10, 11])
```

### ix_()函数

`ix_` 函数可用于组合不同的向量，以便获得每个n-uplet的结果

```python
>>> a = np.array([2,3,4,5])
>>> b = np.array([8,5,4])
>>> c = np.array([5,4,6,8,3])
>>> ax,bx,cx = np.ix_(a,b,c)
>>> ax
array([[[2]],
       [[3]],
       [[4]],
       [[5]]])
>>> bx
array([[[8],
        [5],
        [4]]])
>>> cx
array([[[5, 4, 6, 8, 3]]])
>>> ax.shape, bx.shape, cx.shape
((4, 1, 1), (1, 3, 1), (1, 1, 5))
>>> result = ax+bx*cx
>>> result
array([[[42, 34, 50, 66, 26],
        [27, 22, 32, 42, 17],
        [22, 18, 26, 34, 14]],
       [[43, 35, 51, 67, 27],
        [28, 23, 33, 43, 18],
        [23, 19, 27, 35, 15]],
       [[44, 36, 52, 68, 28],
        [29, 24, 34, 44, 19],
        [24, 20, 28, 36, 16]],
       [[45, 37, 53, 69, 29],
        [30, 25, 35, 45, 20],
        [25, 21, 29, 37, 17]]])
>>> result[3,2,4]
17
>>> a[3]+b[2]*c[4]
17
```

## 位运算

- `bitwise_and()`: 对数组元素执行位与操作
- `bitwise_or()`: 对数组元素执行位或操作
- `invert()`: 按位取反
- `left_shift()`: 向左移动二进制表示的位
- `right_shift()`: 向右移动二进制表示的位

## 函数

### 字符串函数

- `add()`: 对两个数组的逐个字符串元素进行连接
- `multiply()`: 返回按元素多重连接后的字符串
- `center()`: 居中字符串
- `capitalize()`: 将字符串第一个字母转换为大写
- `title()`: 将字符串的每个单词的第一个字母转换为大写
- `lower()`: 数组元素转换为小写
- `upper()`: 数组元素转换为大写
- `split()`: 指定分隔符对字符串进行分割，并返回数组列表
- `splitlines()`: 返回元素中的行列表，以换行符分割
- `strip()`: 移除元素开头或者结尾处的特定字符
- `join()`: 通过指定分隔符来连接数组中的元素
- `replace()`: 使用新字符串替换字符串中的所有子字符串
- `decode()`: 数组元素依次调用 str.decode
- `encode()`: 数组元素依次调用 str.encode

### 数学函数

- `sin(), cos(), tan()` 等三角函数
- `around()`: 返回指定数字的四舍五入值
- `floor()`: 返回小于或者等于指定表达式的最大整数，即向下取整
- `ceil()`: 返回大于或者等于指定表达式的最小整数，即向上取整


### 算数函数

- `add()，subtract()，multiply() 和 divide()`
- `reciprocal()`: 返回参数逐元素的倒数,如 1/4 倒数为 4/1
- `power()`: 将第一个输入数组中的元素作为底数，计算它与第二个输入数组中相应元素的幂
- `mod()`: 计算输入数组中相应元素的相除后的余数

### 统计函数

- `amin()`: 用于计算数组中的元素沿指定轴的最小值
- `amax()`: 用于计算数组中的元素沿指定轴的最大值
- `ptp()`: 计算数组中元素最大值与最小值的差（最大值 - 最小值）
- `percentile()`: 百分位数是统计中使用的度量，表示小于这个值的观察值的百分比
- `median()`: 用于计算数组 a 中元素的中位数（中值）
- `mean()`: 返回数组中元素的算术平均值，如果提供了轴，则沿其计算
- `average()`: 根据在另一个数组中给出的各自的权重计算数组中元素的加权平均值
- `sqrt(mean((x - x.mean())**2))`: 标准差公式
- `mean((x - x.mean())** 2)`: 方差

### 排序、条件筛选函数

- `sort()`: 返回输入数组的排序副本
- `lexsort()`: 用于对多个序列进行排序
- `nonzero()`: 返回输入数组中非零元素的索引
- `where()`: 返回输入数组中满足给定条件的元素的索引
- `extract()`: 根据某个条件从数组中抽取元素，返回满条件的元素

## 线性代数

- `numpy.dot()`: 两个数组的点积，即元素对应相乘
- `numpy.vdot()`: 两个向量的点积
- `numpy.inner()`: 两个数组的内积
- `numpy.matmul()`: 两个数组的矩阵积
- `numpy.determinant()`: 数组的行列式
- `numpy.solve()`: 求解线性矩阵方程
- `numpy.inv()`: 计算矩阵的乘法逆矩阵
- `numpy.matlib.empty()`: 返回一个新的矩阵，元素随机
- `numpy.matlib.zeros()`: 创建一个以 0 填充的矩阵
- `numpy.matlib.one()`: 创建一个以 1 填充的矩阵
- `numpy.matlib.eye()`: 返回一个矩阵，对角线元素为 1，其他位置为零
- `numpy.matlib.identity()`: 返回给定大小的单位矩阵
- `numpy.matlib.rand()`: 创建一个给定大小的矩阵，数据是随机填充的

## 其他

### “自动”整形

要更改数组的尺寸，您可以省略其中一个尺寸，然后自动推导出尺寸

```python
>>> a = np.arange(30)
>>> a.shape = 2,-1,3  # -1 means "whatever is needed"
>>> a.shape
(2, 5, 3)
>>> a
array([[[ 0,  1,  2],
        [ 3,  4,  5],
        [ 6,  7,  8],
        [ 9, 10, 11],
        [12, 13, 14]],
       [[15, 16, 17],
        [18, 19, 20],
        [21, 22, 23],
        [24, 25, 26],
        [27, 28, 29]]])
```

### 矢量堆叠

通过 vstack 等将数组堆叠

```python
x = np.arange(0,10,2)                     # x=([0,2,4,6,8])
y = np.arange(5)                          # y=([0,1,2,3,4])
m = np.vstack([x,y])                      # m=([[0,2,4,6,8],
                                          #     [0,1,2,3,4]])
xy = np.hstack([x,y])                     # xy =([0,2,4,6,8,0,1,2,3,4])
```

### 直方图

histogram应用于数组的NumPy 函数返回一对向量：数组的直方图和bin的向量。matplotlib还有一个构建直方图的功能（hist在Matlab中称为），与NumPy中的直方图不同。主要区别在于pylab.hist自动绘制直方图，而 numpy.histogram只生成数据

```python
>>> import numpy as np
>>> import matplotlib.pyplot as plt
>>> # Build a vector of 10000 normal deviates with variance 0.5^2 and mean 2
>>> mu, sigma = 2, 0.5
>>> v = np.random.normal(mu,sigma,10000)
>>> # Plot a normalized histogram with 50 bins
>>> plt.hist(v, bins=50, density=1)       # matplotlib version (plot)
>>> plt.show()
```

<center><img src="https://cdn.jujimeizuo.cn/note/cs/pl/python/quickstart-2_00_00.png"></center>

```python
>>> # Compute the histogram with numpy and then plot it
>>> (n, bins) = np.histogram(v, bins=50, density=True)  # NumPy version (no plot)
>>> plt.plot(.5*(bins[1:]+bins[:-1]), n)
>>> plt.show()
```

<center><img src="https://cdn.jujimeizuo.cn/note/cs/pl/python/quickstart-2_01_00.png"></center>




## Reference

- [Numpy 官网](https://numpy.org/)
- [SciPy 官网](https://www.scipy.org/)
- [Matplotlib 官网](https://matplotlib.org/)
- [菜鸟教程](https://www.runoob.com/numpy/numpy-tutorial.html)
- [Numpy 快速入门](https://www.numpy.org.cn/user/quickstart.html)
- [Numpy 数据可视化](https://jalammar.github.io/visual-numpy/)