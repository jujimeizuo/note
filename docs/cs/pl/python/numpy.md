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



## Reference

- [Numpy 官网](https://numpy.org/)
- [SciPy 官网](https://www.scipy.org/)
- [Matplotlib 官网](https://matplotlib.org/)
- [菜鸟教程](https://www.runoob.com/numpy/numpy-tutorial.html)
- [Numpy 快速入门](https://www.numpy.org.cn/user/quickstart.html)
- [Numpy 数据可视化](https://jalammar.github.io/visual-numpy/)