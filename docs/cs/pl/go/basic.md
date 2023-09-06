---
counter: True
comment: True
---

# Go 语法基础

!!! abstract
    归档一些学习 Go 的一些语法，和其他编程语言无太大区别，入门还是很简单的

## 为什么学习 Go

- 硬件限制：摩尔定律已然失效
- Go 为并发而生：在多核并发上拥有原生的设计优势，从底层原生并发
- Go 性能强悍：同 C/C++ 一样，Go 也是编译型语言，执行效率更高，性能更好
- Go 简单易学：语法简洁、代码风格统一、开发效率高

## 怎么装 Go

### 下载

- [Go 官网下载地址](https://golang.org/dl/)
- [Go 官方镜像站（推荐）](https://golang.google.cn/dl/)
- Windows平台和Mac平台推荐下载可执行文件版，Linux平台下载压缩文件版。


### 安装

- Windows：以64位Win10举例，将选好安装包下载到本地，双击一直next，**注意要指定一个Go 安装目录，这很重要**
- Linux：

```shell
# 在版本选择好下载文件后
wget https://dl.google.com/go/go1.14.1.linux-amd64.tar.gz
# 将下载好的文件解压到 `/usr/local` 目录中，没有权限加上 `sudo`
tar -zxvf go1.14.1.linux-amd64.tar.gz -C /usr/local
# 配置环境变量，在 `~/.profile` 中添加以下代码，并用 `source` 重新加载
export GOROOT=/usr/local/go
export PATH=$PATH:$GOROOT/bin
```
- Mac：下载可执行文件后，直接点击下一步安装即可，默认会将 go 安装到 `/usr/local/go` 目录下

### GOROOT 和 GOPATH


>&ensp;&ensp;`GOROOT`和`GOPATH`都是环境变量，其中`GOROOT`是我们安装go开发包的路径，而从`Go 1.8`版本开始，Go开发包在安装完成后会为`GOPATH`设置一个默认目录，并且在`Go1.14`及之后的版本中启用了`Go Module`模式之后，不一定非要将代码写到`GOPATH`目录下，所以也就不需要我们再自己配置`GOPATH`了，使用默认的即可。

- 查看 `GOPATH` 路径：`go env`

!!! note "GOPROXY"
    `Go1.14`版本之后，都推荐使用`go mod`模式来管理依赖环境了，也不再强制我们把代码必须写在`GOPATH`下面的src目录了，你可以在你电脑的任意位置编写go代码。（网上有些教程适用于1.11版本之前。）

    默认`GoPROXY`配置是：`GOPROXY`=[https://proxy.golang.org,direct](https://proxy.golang.org,direct)，由于国内访问不到[https://proxy.golang.org](https://proxy.golang.org)，所以我们需要换一个PROXY，这里推荐使用[https://goproxy.io](https://goproxy.io)或[https://goproxy.cn](https://goproxy.cn)。

    可以执行下面的命令修改GOPROXY：
    ```shell
    go env -w GOPROXY=https://goproxy.cn,direct
    ```

## 怎么编写、运行 Go

> &ensp;&ensp;任何编辑器都可以编写 Go（包括记事本），这里推荐用 VsCode（需安装 Go 扩展），当然也可以用Sublime，JB 的全家桶等等


### go mod init

使用`go module`模式新建项目时，我们需要通过`go mod init` 项目名命令对项目进行初始化，该命令会在项目根目录下生成`go.mod`文件。执行如下命令
```shell
go mod init ${project}
```

**记得配置好 `GOPROXY`**

### 编译、运行、安装

- `go build`： 命令表示将源代码编译成可执行文件。
- `go run`：命令本质上是先在临时目录编译程序然后再执行。
- `go install`：它先编译源代码得到可执行文件，然后将可执行文件移动到GOPATH的bin目录下。因为**把 `GOPATH` 下的 `bin` 目录添加到了环境变量中**，所以就可以在任意地方直接执行可执行文件。


## go module

> &ensp;&ensp; `go module` 是Go1.13版本之后。Go语言默认的依赖管理工具。

- 设置好 `GO111MODULE=on` 就可以使用 `go module`
- 使用 `go module`` 管理依赖后会在项目根目录下生成两个文件`go.mod`和`go.sum`
- `go mod` 命令：
    - `go mod download`    下载依赖的module到本地cache（默认为$GOPATH/pkg/mod目录）
    - `go mod edit`        编辑go.mod文件
    - `go mod graph`       打印模块依赖图
    - `go mod init`        初始化当前文件夹, 创建go.mod文件
    - `go mod tidy`        增加缺少的module，删除无用的module
    - `go mod vendor`      将依赖复制到vendor下
    - `go mod verify`      校验依赖
    - `go mod why`         解释为什么需要依赖
- go.mod文件记录了项目所有的依赖信息
- 在项目中执行 `go get` 命令可以下载依赖包，并且还可以指定下载的版本

## 变量和常量

- 变量
    - 需要显式声明，并且在函数调用等情况下，编译器会检查其类型的正确性
    - `var` 声明1个或多个变量，Go 会自动推断已经有初始值的变量类型
    - 声明后却没有给出对应的初始值时，变量将会初始化为 零值 。 例如，int 的零值是 0
    - := 语法是声明并初始化变量的简写（不能在函数外使用）， 例如 `var f string = "short"` 可以简写为`f := "short"`
    - 在使用多重赋值时，如果想要忽略某个值，可以使用匿名变量，一个下划线`_`表示
- 常量
    - 支持字符、字符串、布尔和数值常量
    - const 用于声明一个常量
    - const 语句可以出现在任何 var 语句可以出现的地方
    - iota 是常量计数器，在 const 关键字出现时会被重置为0

## 条件语句

### if/else 分支
- if-else if-else 结构
- Go 规定与 if 匹配的左括号 \{ 必须与 if 和表达式放在同行，其他位置会触发编译错误，同理else
- 在条件语句之前可以有一个声明语句；在这里声明的变量可以在这个语句所有的条件分支中使用
- 在 Go 中，条件语句的圆括号不是必需的，但是花括号是必需的
- Go 没有三目运算符， 即使是基本的条件判断，依然需要使用完整的 if 语句

??? example "if-else"
    ```go
    if num := 9; num < 0 {
        fmt.Println(num, "is negative")
    } else if num < 10 {
        fmt.Println(num, "has 1 digit")
    } else {
        fmt.Println(num, "has multiple digits")
    }
    ```

### switch 分支
- 不带表达式的 switch 是实现 if/else 逻辑的另一种方式
- 每个 switch 只能有一个 default 分支
- 一个分支可以有多个值，多个case值中间使用英文逗号分隔
- fallthrough 语法可以执行满足条件的case的下一个case，是为了兼容C语言中的case设计的

??? example "switch"
    ```go
    func switchDemo5() {
        s := "a"
        switch {
        case s == "a":
            fmt.Println("a")
            fallthrough
        case s == "b":
            fmt.Println("b")
        case s == "c":
            fmt.Println("c")
        default:
            fmt.Println("...")
        }
    }
    ```

## 循环

- 经典的初始/条件/后续 for 循环
- for循环的初始语句可以被忽略，但是初始语句后的分号必须要写
- for循环的初始语句和结束语句都可以省略
- for循环可以通过break、goto、return、panic语句强制退出循环
- Go语言中可以使用for range遍历数组、切片、字符串、map 及通道（channel）。 通过for range遍历的返回值有以下规律
    - 数组、切片、字符串返回索引和值。
    - map返回键和值。
    - 通道（channel）只返回通道内的值

??? example "for"
    ```go
    for i := 0; i < 10; i++ {
        ...
    }

    for ; i < 10; i++ {
        ...
    }
    for i < 10 {
        ...
    }
    for i, v := range ** {
        ...
    }
    ```

## 数据类型

### 数字与运算

- 整型有int8/16/32/64，包括对应的无符号整型
- 浮点型有float32/64
- 复数有complex64/128
- 运算：
    - 和C/C++无太大差别

### 布尔类型

- 通过 bool 来声明布尔型数据，只有 true 和 false
- 默认值为 false
- 不允许将整型强制转换为布尔型
- 布尔型无法参与数值运算，也无法与其他类型进行转换


### 字符串

- 字符串的内部实现使用 UTF-8 编码，字符串的值为双引号(")中的内容，可以在Go语言的源码中直接添加非ASCII码字符
- 要定义一个多行字符串时，就必须使用反引号字符，反引号间换行将被作为字符串中的换行，但是所有的转义字符均无效，文本将会原样输出
```go
s := `第一行
第二行
第三行
`
```
- 常用方法
    - `len(str)`：求长度
    - `+或fmt.Sprintf`：拼接字符串
    - `strings.Split`：分割
    - `strings.contains`：判断是否包含
    - `strings.HasPrefix,strings.HasSuffix`：前缀/后缀判断
    - `strings.Index(),strings.LastIndex()`：子串出现的位置
    - `strings.Join(a[]string, sep string)`：join操作


### byte和rune类型

- 组成每个字符串的元素叫做“字符”，可以通过遍历或者单个获取字符串元素获得字符。 字符用单引号（’）包裹起来
- Go 包括两种字符：
    - `uint8` 类型，或者叫 `byte` 型，代表一个 ASCII 码字符
    - `rune` 类型，代表一个 `UTF-8` 字符
- 当需要处理中文、日文或者其他复合字符时，则需要用到 `rune` 类型。`rune` 类型实际是一个`int32`
- Go 使用了特殊的 `rune` 类型来处理 `Unicode`，让基于 `Unicode` 的文本处理更为方便，也可以使用 `byte` 型进行默认字符串处理，性能和扩展性都有照顾
- 字符串底层是一个byte数组，所以可以和 `[]byte` 类型相互转换
- 字符串是不能修改的，字符串是由 `byte` 字节组成，所以字符串的长度是 `byte` 字节的长度
- `rune` 类型用来表示 `utf8` 字符，一个`rune` 字符由一个或多个`byte` 组成
- 要修改字符串，需要先将其转换成 `[]rune` 或 `[]byte` ，完成后再转换为`string`

??? example "byte and rune"
    ```go
    s1 := "big"
	// 强制类型转换
	byteS1 := []byte(s1)
	byteS1[0] = 'p'
	fmt.Println(string(byteS1))

	s2 := "白萝卜"
	runeS2 := []rune(s2)
	runeS2[0] = '红'
	fmt.Println(string(runeS2))
    ```


### 数组

- 定义一个长度为3元素类型为int的数组a：`var a [3]int`
- 内置函数 len 可以返回数组的长度
- 初始化
    - 可以使用初始化列表来初始化数组：`var num = [3]int{1, 2}`
    - 可以让编译器根据初始值的个数自行推断数组的长度，`var num = [...]{1, 2}`
    - 指定索引值来初始化数组，`num := [...]int{1: 1, 3: 5}`
- 遍历
    - `for i := 0; i < len(a); i ++ {}`
    - `for index, value := range a {}`
- 多维数组定义，`a := [2][3]int`
- 多维数组只有第一层可以使用 ... 来让编译器推导数组长度，不支持内层使用
- 数组是值类型，赋值和传参会复制整个数组，因此改变副本的值，不会改变本身的值
- `[n]*T` 表示指针数组，`*[n]T` 表示数组指针


### 切片

- 定义
    - 切片（Slice）是一个拥有相同类型元素的可变长度的序列。它是基于数组类型做的一层封装。它非常灵活，支持自动扩容
    - 切片声明：`var name []T`，name 表示变量名，T 表示切片中的元素类型
    - 切片拥有自己的长度和容量，我们可以通过使用内置的len()函数求长度，使用内置的cap()函数求切片的容量
    - 切片的底层就是数组，和 Python 一样，可以使用`b := a[1:3]`，表示从数组 a 中选出 索引值在$[1,3)$中的元素组成切片 b
    - 完整的切片表达式：`a[low: high: max]`，得到的结果切片的容量设置为`max - low`，low 可以省略，默认为0
    - 使用内置`make函数`构造切片，`make([]T, size, cap)`，T 表示元素类型，size 表示元素数量，cap 表示切片容量
    - 判断切片是否为空，请使用`len(s) == 0`，不要使用`s == nil`
- 切片不能直接比较
- 切片遍历和数组一样
- 可以用`append()`为切片添加元素`s = append(s, 1,2,3)`，也可以添加另一个切片的元素`s = append(s, s2...)`
- 切片的扩容策略（略）
- 可以使用`copy()`复制切片，但切片是引用类型，所以两个切片都指向同一块内存地址，对一个切片的修改会影响另一个切片的内容
- 排序，需要`import sort`，排序时可自定义排序`sort.Slice(a, func(i, j int) bool { return a[i] < a[j] })`

### Map

- 一种无序的`key-value`数据结构，在 Go 中 map 是引用类型，必须初始化才能使用
- 定义：`map[KeyType]ValueType`，KeyType 表示键的类型，ValueType 表示键对应的值的类型，`x := map[int]int{1:3, 2:4}`或`s := make([int]int, 2), s[1] = 3, s[2] = 4`
- 判断键是否存在：`value, ok := map[key]`，查看 ok 是否为 true
- 遍历：`for k, v := range map {}`，v 可省略，遍历元素的顺序与添加键值对的顺序无关，可以把 key 放入 slice 中排序，然后遍历 slice 就可以指定顺序
- `delete()`从 map 中删除一组键值对

## 函数

- 使用 `func` 来定义函数
- 通过函数名的方式调用函数
- 函数的参数中如果相邻变量的类型相同，则可以省略类型，
- 可变参数是指函数的参数数量不固定。Go语言中的可变参数通过在参数名后加 ... 来标识，可变参数通常要作为最后一个参数
- 函数如果有多个返回值，必须使用 () 将所有返回值包裹
- 函数定义时可以给返回值命名，并在函数体中直接使用这些变量，最后通过return关键字返回 
- 可以使用 type 关键字来定义一个函数类型
- 高阶函数
    - 函数作为参数
    - 函数作为返回值
- 可以定义匿名函数，`add := func(x, y int)`，多用于回调函数和闭包
- 闭包=函数+引用环境（略）
- `defer`语句，将其后面跟随的语句进行延迟处理，会被逆序处理
- 使用 panic/recover 模式来处理错误，**recover()必须搭配defer使用，defer一定要在可能引发panic的语句之前定义**

??? example "func"
    ```go
    func 函数名(参数)(返回值) {
        函数体
    }

    func add(a, b int) int {
        return x + b
    }

    func intSum2(x ...int) int {
        fmt.Println(x) //x是一个切片
        sum := 0
        for _, v := range x {
            sum = sum + v
        }
        return sum
    }

    func calc(x, y int) (int, int) {
        reurn x + y, x - y
    }

    func calc(x, y int) (sum, sub int) {
        sum = x + y
        sub = x - y
        return
    }

    func add(x, y int) int {
        return x + y
    }
    func calc(x, y int, op func(int, int) int) int {
        return op(x, y)
    }
    func main() {
        ret2 := calc(10, 20, add)
        fmt.Println(ret2) //30
    }

    func do(s string) (func(int, int) int, error) {
        switch s {
        case "+":
            return add, nil
        case "-":
            return sub, nil
        default:
            err := errors.New("无法识别的操作符")
            return nil, err
        }
    }
    ```


## 指针

- 和 C 的区别不大，都是用`*`和`&`来操作，`*`表示取值操作符，`&`表示取地址操作符
- new 和 make 分配内存
    - `a = new(int)`，make 只用于slice、map以及channel的内存创建，返回的是引用类型
    - 而new用于类型的内存分配，并且内存对应的值为类型零值，返回的是指向类型的指针

## 结构体

### 定义与初始化
- type 定义类型别名
- type + struct 定义结构体，type 类型名 struct { 字段名 字段类型 ...}
- 使用 var 实例化结构体
- 通过 . 访问结构体字段
- 初始化
    - 没有初始化的结构体，其成员变量都是对应其类型的零值
    - 使用键值对对结构体进行初始化时，键对应结构体的字段，值对应该字段的初始值
- 结构体占用一块连续的内存，空结构体是不占用空间的
- 结构题没有构造函数，但是可以自己实现
??? example "构造函数"
    ```go
    func newPerson(name, city string, age int8) *person {
        return &person{
            name: name,
            city: city,
            age:  age,
        }
    }
    ```

### 方法

- 方法（Method）是一种作用于特定类型变量的函数。这种特定类型变量叫做接收者（Receiver）。接收者的概念就类似于其他语言中的 this 或者 self，当然还可以有指针类型的接收者
```go
func (接收者变量 接收者类型) 方法名(参数列表) (返回参数) {
    函数体
}
```
- 方法与函数的区别是，函数不属于任何类型，方法属于特定的类型

### 其他

- 结构体允许其成员字段在声明时没有字段名而只有类型，这种没有名字的字段就称为匿名字段
- 一个结构体中可以嵌套包含另一个结构体或结构体指针
- 通过结构体可以实现“继承”
- 结构体中字段大写开头表示可公开访问，小写表示私有（仅在定义当前结构体的包中可访问）
- 结构体可以使用 JSON 序列化

## 接口

### 接口类型

- 接口是一种由程序员来定义的类型，一个接口类型就是一组方法的集合，它规定了需要实现的所有方法
- 每个接口类型由任意个方法签名组成
```go
type 接口类型名 interface{
    方法名1( 参数列表1 ) 返回值列表1
    方法名2( 参数列表2 ) 返回值列表2
    ...
}
```
- 接口就是规定了一个需要实现的方法列表，在 Go 语言中一个类型只要实现了接口中规定的所有方法，那么我们就称它实现了这个接口
- 可以通过值接收者或指针接收者实现借口

### 类型与接口的关系

- 一个类型实现多个接口
- 多种类型实现同一接口

### 接口组合

- 接口与接口之间可以通过互相嵌套形成新的接口类型，例如Go标准库io源码中就有很多接口之间互相组合的示例

### 空接口

- 空接口是指没有定义任何方法的接口类型。因此任何类型都可以视为实现了空接口。也正是因为空接口类型的这个特性，空接口类型的变量可以存储任意类型的值
- 通常我们在使用空接口类型时不必使用type关键字声明，可以像下面的代码一样直接使用interface{}，`var x interface{}`
- 空接口作为函数的参数，使用空接口实现可以接收任意类型的函数参数
- 空接口作为map的值，使用空接口实现可以保存任意值的字典

### Error 接口

- Go 语言中把错误当成一种特殊的值来处理，不支持其他语言中使用 try/catch 捕获异常的方式
- Go 语言中使用一个名为 error 接口来表示错误类型
- 当一个函数或方法需要返回错误时，我们通常是把错误作为最后一个返回值，例如之前查询map中是否存在键值对
- 默认零值为 nil
- 使用 fmt.Errorf 才描述错误信息
- 可以对自定义结构体类型实现 error 接口

## 标准库

### fmt

> &ensp;&ensp;fmt包实现了类似C语言printf和scanf的格式化I/O。主要分为向外输出内容和获取输入内容两大部分

#### 向外输出

- `Print()`：将内容输出到系统的标准输出
- `Fprint()`：将内容输出到一个io.Writer接口类型的变量w中，我们通常用这个函数往文件中写入内容
- `Sprint()`：把传入的数据生成并返回一个字符串
- `Errorf()`：根据format参数生成格式化字符串并返回一个包含该字符串的错误

#### 获取输入

- `Scan()`：标准输入扫描文本，读取由空白符分隔的值保存到传递给本函数的参数中，换行符视为空白符
- `Scanf()`：标准输入扫描文本，根据format参数指定的格式去读取由空白符分隔的值保存到传递给本函数的参数中
- `Scanln()`：类似Scan，它在遇到换行时才停止扫描。最后一个数据后面必须有换行或者到达结束位置
- `bufio.NewReader`：时候我们想完整获取输入的内容，而输入的内容可能包含空格，这种情况下可以使用bufio包来实现
- `Fscan()系列`：类似于`Scan()系列`，从io.Reader中读取数据
- `Sscan()系列`：类似于`Scan()系列`，从指定字符串中读取数据

### log

> Go语言内置的log包实现了简单的日志服务

??? example "log"
    ```go
    package main

    import (
        "log"
    )

    func main() {
        log.Println("这是一条很普通的日志。")
        v := "很普通的"
        log.Printf("这是一条%s日志。\n", v)
        log.Fatalln("这是一条会触发fatal的日志。")
        log.Panicln("这是一条会触发panic的日志。")
    }
    ```

除了默认提供日志的时间信息，还可以通过配置logger来设置输出信息

### 文件操作

#### 打开和关闭文件

`os.Open()`函数能够打开一个文件，返回一个`*File`和一个`err`。对得到的文件实例调用`close()`方法能够关闭文件

??? example "open and close"
    ```go
    package main

    import (
        "fmt"
        "os"
    )

    func main() {
        // 只读方式打开当前目录下的main.go文件
        file, err := os.Open("./main.go")
        if err != nil {
            fmt.Println("open file failed!, err:", err)
            return
        }
        // 关闭文件
        file.Close()
    }
    ```

**为了防止文件忘记关闭，我们通常使用defer注册文件关闭语句**


#### 读取文件

- file.Read()

    - 接收一个字节切片，返回读取的字节数和可能的具体错误，读到文件末尾时会返回0和io.EOF
    
    ```go
    func (f *File) Read(b []byte) (n int, err error)
    ```

    - 使用 for 循环读取文件中的所有数据


- bufio读取文件

`bufio`是在`file`的基础上封装了一层API，支持更多的功能

- 读取整个文件

`io/ioutil`包的`ReadFile`方法能够读取完整的文件，只需要将文件名作为参数传入


#### 文件写入操作

- `os.OpenFile()`函数能够以指定模式打开文件，从而实现文件写入相关功能
- `Write`和`WriteString`
- `bufio.NewWriter`
- `ioutil.WriteFile`
### strconv

> &ensp;&ensp;strconv包实现了基本数据类型与其字符串表示的转换

#### Atoi()

用于将字符串类型的整数转换为int类型

#### Itoa()

用于将int类型数据转换为对应的字符串表示

#### Parse系列函数

> &ensp;&ensp;Parse类函数用于转换字符串为给定类型的值：ParseBool()、ParseFloat()、ParseInt()、ParseUint()

- 返回字符串表示的bool值
```go
func ParseBool(str string) (value bool, err error)
```

- 返回字符串表示的整数值
```go
func ParseInt(s string, base int, bitSize int) (i int64, err error)
```

- 解析一个表示浮点数的字符串并返回其值
```go
func ParseFloat(s string, bitSize int) (f float64, err error)
```

#### Format系列函数

> &ensp;&ensp;Format系列函数实现了将给定类型数据格式化为string类型数据的功能

- 根据b的值返回”true”或”false”
```go
func FormatBool(b bool) string
```

- 返回i的base进制的字符串表示
```go
func FormatInt(i int64, base int) string
```

- 函数将浮点数表示为字符串并返回
```go
func FormatFloat(f float64, fmt byte, prec, bitSize int) string
```


## Referencce

- [Go 官方文档](https://go.dev/doc/effective_go)
- [Go 菜鸟教程](https://www.runoob.com/go/go-tutorial.html)
- [Go 语言学习之路](https://www.liwenzhou.com/posts/Go/golang-menu/)
- [Go by Example 中文版](https://gobyexample-cn.github.io/arrays)