---
counter: True
comment: True
---

# gdb 命令相关

!!! abstract
    gdb相关的一些命令，插件等

## 前言

### 什么是gdb

> GNU调试器（英语：GNU Debugger，缩写：GDB），是GNU软件系统中的标准调试器，此外GDB也是个具有移携性的调试器，经过移携需求的调修与重新编译，如今许多的类UNIX操作系统上都可以使用GDB，而现有GDB所能支持调试的编程语言有C、C++、Pascal以及FORTRAN。
> <div style="text-align: right">———— 维基百科</div>

### 准备工作

通常，在为调试而编译时，我们会关掉编译器的优化选项`（-O）`， 并打开调试选项`（-g）`。另外，`-Wall`在尽量不影响程序行为的情况下选项打开所有warning，也可以发现许多问题，避免一些不必要的 BUG。

例如： `gcc -g -Wall program.c -o program`

`-g` 选项的作用是在可执行文件中加入源代码的信息，比如可执行文件中第几条机
器指令对应源代码的第几行，但并不是把整个源文件嵌入到可执行文件中，所以在调
试时必须保证`gdb`能找到源文件。

调试下列程序前要做准备工作，在shell中输入：

```shell
$ gcc -g -Wall test.c -o test
```

## gdb命令

### 过程操作

- `gdb` (可执行程序) 启动gdb调试
- `quit / q` 退出gdb调试
- `set args 10 20 `给程序设置参数
- `show args`获取设置的参数
- `help`用来查看调试帮助或具体指令的相关信息
- `list` 查看当前文件代码，可以指定文件和函数 (l)
- `set list / listsize` 设置显示的行数
- `print 变量名` 打印变量值(p)
- `ptype 变量名` 打印变量类型
- `until` 跳出循环

### 断点

- `gdb break (file:)line/function` 断在(文件:)行号或函数(b)
- `gdb break *0x....` 断在地址
- `gdb info breakpoints` 查看断点及状态 (i b)
- `gdb delete / clear` 清除所有断点 (d/cl)
- `gdb delete <breakpoint#>` 删除某一断点（从 i b 得来断点号）
- `gdb clear ...` 清除某一符号、地址处的断点
- `gdb disable <breakpoint#>` 禁用某一断点
- `gdb enable <breakpoint#>` 启用某一断点
- `gdb watch ...` 在某处增加观察点，delete、enable、disable 与断点共用
- `gdb break/watch <where> if <condition>` 如果条件满足则断
- `gdb condition <breakpoint#> <condition>` 更改条件

### 运行
- `gdb start` 程序停在第一行
- `gdb run` 直接运行，遇到端点才停止 (r)
- `gdb continue` 继续运行 (c)
- `gdb step` 运行到下一条源码 (s)
- `gdb next` 单步运行，跳过函数 (n)
- `gdb finish` 运行完当前函数 (fin)
- `gdb attach <pid>` 连接程序
- `gdb detach` 从当前程序断连
- `gdb target remote localhost:1234` 连接 qemu

### 调用栈

- `gdb backtrace` 查看调用栈 (bt)
- `gdb frame` 查看当前帧栈
- `gdb up/down` 移动当前帧栈（向 main / 远离 main）
- `gdb info locals` 查看当前帧栈变量
- `gdb info args` 查看函数参数

## gdb插件

### gdb-peda

每条指令带寄存器、汇编、内存数据回显

```shell
$ git clone https://github.com/longld/peda.git ~/peda
$ echo "source ~/peda/peda.py" >> ~/.gdbinit
```

其实就是下载完成后, 将 `source ~/peda/peda.py` 写入 `~/.gdbinit`

## Reference

- [jujimeizuo的Linux GDB调试](http://www.jujimeizuo.cn/blog/index.php/2022/12/31/linux-gdb-debug/)
- [gdb相关备忘](https://note.tonycrane.cc/cs/tools/gdb/)
- [维基百科-gdb](https://en.wikipedia.org/wiki/GNU_Debugger)
- [GDB实用插件(peda, gef, gdbinit)全解](https://blog.csdn.net/gatieme/article/details/63254211)