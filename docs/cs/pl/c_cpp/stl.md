---
counter: true
comment: true
---

# STL

STL简称标准模版库，被容纳在C++标准程序库，包含了许多基本数据结构和基本算法，使程序员写起来得心应手。

## 为什么使用STL

在学习数据结构的时候，在程序中会使用到堆、栈、队列、链表等一些基本的算法，而学习数据结构的时候，这些基本算法写起来十分繁琐，如果不想写这些，那么就可以考虑一下STL了。 但是不要太过于依赖STL！

## STL基本概念

要使用STL，需要理解以下几个基本概念：

- **容器**：是存放数据的地方，常见的容器有：链表(list) 栈(stack) 动态数组 (vector) 双端队列(deque) 队列(queue) 映射(map)
- **迭代器(iterator)**：可以理解为C语言里的地址，而迭代器就是容器的一个指针，十分重要！！！ 
- **算法**：可以对容器里的数据做一些基本操作，比如排序，找最大元素等等。

## STL使用前的初始化

1. 需要对应的头文件，比如list就需要`#include<list>`，且没有.h，或者恶心的万能头`#include<bits/stdc++.h>`。 
2. 添加std命名空间（using namespace std;）不加的话后面可以自己写一堆。。。

## C++里STL基本容器详解

### cmp类

 **通过自定义cmp类来完成STL的更加自由的设置**

```c++
struct cmp {
    bool operator()(int a, int b) {
        return a > b;
    }
};
```

### sort

1. 需要头文件`#include<algorithm>`；
2. 复杂度为O(nlogn)，比较排序的极限了。

```c++
bool cmp(int a, int b)
{
    return a > b;
}
int a[] = {1, 2 ,3 , 4};
sort(a, a + 4, cmp);
```

sort里第一个参数是数组需要排序的第一个地址，第二个参数是数组需要排序的第二个地址，都三个参数是一个自定义函数，对数组排序的函数，上面的cmp函数是使数组元素从大到小排序。

sort是不稳定排序，即对于相同的值，无法保证其前后顺序 解决办法： 1、增加一个 index 变量，在值相同的使用比较 index 值的大小 2、使用 `stable_sort``

### vector

1. 需要头文件#include<vector> 
2. 不定数组

```c++
vector<int> a, b;
a.push_back(1); // 推入一个新的值到数组最后
a.pop_back();       // 删除数组最后的那个值
a.front();          // 数组开头的值
a.back();           // 数组结尾的值
a = b;              // 数组拷贝
a == b;             // 数组是否相同
a[1];               // 数组中第二个值

vector<int> a;
a.size();               // 容器内的元素个数
a.empty();              // 容器是否为空
// 除了queue和stack外通用的方法
a.clear();              // 清空容器内的所有元素
a.begin();              // 容器的一个元素的迭代器
a.end();                // 容器尾后迭代器

vector<int> v;
vector<int>::iterator iter    // 定义迭代器
iter = v.begin();               // 数组头“指针”
iter = v.end();             // 数组尾“指针”
```

\==list==: 1.需要头文件#include<int> l; 2.双向链表

```c++
list<int> l;
l.push_front(1);            // 插入元素到开头
l.pop_front();          // 从开头删掉元素
l.erase(l.begin());     // 删除指定迭代器处的元素
l.insert(l.begin(), 1); // 在指定迭代器前插入元素
l.reverse();                // 反转整个链表
```

### string
1. 伪字符串； 
2. 定义：string s; 
3. 只能流输入和流输出；

```c++
string a, b;
a[1] == 'a';              // 得到某个字符
a = b;                      // 字符串拷贝
a >= b;                      // 字典序比较
a[1] = b[1];                // 修改某个字符
a += b;                     // 字符串拼接
a = a + b;                  // 字符串拼接
a += "123";               // 字符串拼接
a = b + "123";                // 字符串拼接
int len = a.lenth();        // 字符串的长度
```

### queue 
1. 需要头文件`#include<queue>`；
2. 先进先出（内部为链表实现）

```c++
queue<int> q;
q.push(1);              // 将1推入队列
q.pop();                // 推出队列开头的元素
q.front();              // 队列的第一个元素
```

### stack 
1. 需要头文件`#include<stack>`; 
2. 后进先出（内部为数组实现）

```c++
stack<int> q;
q.push(1);              // 将1推入堆栈
q.pop();                // 推出堆栈最后的元素
q.top();                // 堆栈的最后的元素
```

### pair 

1. 需要头文件`#include<map>` 
2. 表示一组键对（有两个变量的结构体）

```c++
pair<int, string> p;
p.first = 1;
p.second = "abc";
p = make_pair(1, "abc");
p = {1, "abc"};

pair<int, string> p[100];
sort(p, p + 100);
// 默认优先first从小到大
// 如果first相同则second从小到大
```

pair与其他结构嵌套

```c++
vector<pair<int, string> > vp;
queue<pair<float, int> > qp;
queue<pair<pair<int, int>, int> > qpp;
```

### set 

1. 需要头文件`#include<set>`； 
2. set 保存了不可重复的元素--**二叉搜索树-红黑树**

```c++
set<int> s;
s.insert(1);                // 插入到集合中
s.erase(1);             // 从集合中删除
s.erase(s.begin());     // 从集合中删除
s.count(1);             // 集合中是否存在
s.find(1);
// 返回对应值的迭代器（若无则返回尾后迭代器）
```

- 由于set是红黑树，所以满足以下内容 

    1. 内部有序(默认从小到大) 
    2. 没有重复值，如果出现重复值会不断被覆盖 
    3. 几乎所有操作复杂度均为 O(logN) 
    4. 不可以修改节点上的值 
    5. 修改操作只能进行插入和删除两个操作

**set通常作用：保证唯一性，保证数列有序**

### map 
1. 需要头文件`#include<map>`；
2. map字典（键对集合）**——二叉搜索树——红黑树**

```c++
map<char, int> m;
m.insert(make_pair('a', 1));  // 加入字典
m.insert({'a', 1});           // 加入字典
m.erase('a');                 // 从字典中删除
m.count('a');                 // 字典中是否存在
m.find('a');
// 返回对应值的迭代器（若无则返回尾后迭代器）
```

通常称map的first元素为key，second元素为value ·由于map是键对红黑树，所以满足以下内容 1、set的大部分性质； 2、key不能重复，不能修改，只能删除和添加； 3、允许value重复，可以对value进行修改； 4、map是按照key进行排序的； 5、key和value一定是成对出现的； 6、map的迭代器指向的内容是一个pair；

### priority_queue 
1. 需要头文件`#include<queue>` 
2. 优先队列--堆

```c++
priority_queue<int> prq;
prq.top();              // 堆顶上的元素
prq.pop();              // 弹出堆顶上的元素
prq.push(1);            // 推入堆
```

- priority_queue默认为最大堆，即堆顶的元素最大 
- 和queue一样，priority_queue不允许访问除了堆顶元素以外的任何一个元素。 
- priority_queue的插入和弹出操作的复杂度均为O(logN)

- **priority_queue功能与set接近，而且set的功能更强大，并且理论复杂度相同，为什么有时候反而就是用priority_queue？ priority_queue的复杂度为最差情况下的复杂度，而set和map的复杂度均为稳定复杂度的极限值**

