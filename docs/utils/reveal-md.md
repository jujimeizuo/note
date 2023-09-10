---
counter: True
comment: True
---

# reveal-md

!!!abstract
    [RevealJS](https://github.com/hakimel/reveal.js/) 是一个简单且支持 markdown 的工具，然后转换成 PPT。

    这里推荐一个slide模版 [:material-github:TonyCrane/slide-template](https://github.com/TonyCrane/slide-template)。

    本人不喜欢写 PPT（也不会写）

## 什么是 reveal-md

- 可以只用写 markdown 的方式写 PPT，将 markdown 转换成 html，或导出 PDF
- 是 revealjs 的 makrdown 功能

## 安装 reveal-md

### 本地构建

- reveal.js 使用 nodejs 构建，需要提前安装好 [nodejs](https://nodejs.org/zh-cn)
- 通过 npm 安装 reveal-md
```shell
$ npm install -g reveal-md
$ reveal-md slides.md # 启动本地服务器并在默认浏览器中将任何 Markdown 文件演示文稿打开
```

### Docker 构建

- 不需要安装 node.js
- 在容器中启用实时重新加载，还应该映射端口 35729
```shell
$ docker run --rm -p 1948:1948 -p 35729:35729 -v <path-to-your-slides>:/slides webpronl/reveal-md:latest /slides --watch
```

## 相关命令

- `reveal-md -w` 实时重新加载
- `reveal-md --scripts [url/*.js]` 自定义 js
- `reveal-md --css [url/*.js]` 自定义 css 
- `reveal-md --static [--static-dirs=assets]` 导出到独立的 HTML 网站 (将包含其他静态资源的目录复制到目标目录)
- `reveal-md --print [--print-size 1024x768 / A4] name.pdf`  打印成 PDF（或者在浏览器的 url 后添加 ?print-pdf
- `reveal-md --template` 自定义模版

## 配置


### yaml 配置

可以在 markdown 文件中通过 yaml 进行配置

```yaml
---
title: Slide 模板 # 幻灯片名称
separator: <!--s--> # 幻灯片横行切割标志
verticalSeparator: <!--v--> # 幻灯片垂直切割标志
theme: simple # 幻灯片主题
highlightTheme: github # 代码高亮主题
css: custom.css # 自定义 css
revealOptions:
    transition: 'slide' # 动画效果
    transitionSpeed: fast # 动画速度
    center: false # 是否居中
    slideNumber: "c/t" # 幻灯片数量
    width: 1000 # 幻灯片宽度
---
```

### 幻灯片主题

- 默认主题

| 名称      | 效果                                 |
| --------- | ------------------------------------ |
| black     | 黑色背景，白色文本，蓝色链接（默认） |
| white     | 白色背景，黑色文本，蓝色链接         |
| league    | 灰色背景，白色文字，蓝色链接         |
| beige     | 米色背景，深色文字，棕色链接         |
| sky       | 蓝色背景，细暗文本，蓝色链接         |
| night     | 黑色背景，厚白色文字，橙色链接       |
| serif     | 卡布奇诺背景，灰色文本，棕色链接     |
| simple    | 白色背景，黑色文本，蓝色链接         |
| solarized | 高分辨率照片                         |
| blood     | 深色背景，厚白文字，红色链接         |
| moon      | 高分辨率照片                         |

- 自定义主题
    1. 下载 reveal git clone git@github.com:hakimel/reveal.js.git ；
    2. 在 /css/theme/coder.scss 中复制一个文件；
    3. 运行 npm run build -- css-themes 生成css dist/coder.css；
    4. 运行指定主题 reveal-md slides.md -w --theme theme/coder.css。

### 切换时动画

| 名称    | 效果                                         |
| ------- | -------------------------------------------- |
| none    | 瞬间切换背景                                 |
| fade    | 交叉淡入淡出 - 背景转换的默认值              |
| slide   | 在背景之间滑动 — 幻灯片过渡的默认设置        |
| convex  | 以凸角滑动                                   |
| concave | 以凹角滑动                                   |
| zoom    | 向上缩放传入的幻灯片，使其从屏幕中心向内扩展 |



## 用法

### 换页

- 横向换页：`<!--s-->`（根据 yaml 的配置
- 垂直换页：`<!--v-->`（根据 yaml 的配置

### 添加属性

- 当需要在 section 中添加属性时 `<!-- .slide: 属性=属性值 -->`
- 当需要在其它元素插入属性时 `<!-- .element: 属性=属性值 -->`
- 设置背景色或背景图 `<!-- .slide: data-background="./image1.png" -->`
- 设置动画片段 `Item1 <!-- .element: class="fragment" data-fragment-index="1" -->`

**具体可以查阅revealjs的docs**

### 指定代码高亮顺序

````markdown
```python [1|3-6]
n = 0
while n < 10:
  if n % 2 == 0:
    print(f"{n} is even")
  else:
    print(f"{n} is odd")
  n += 1
```
````


### 地址跳转

```markdown
<!-- .slide: id=0 -->
[跳转0](#/0)
```

## 部署


### Github Pages

- 在 Github 中新建一个 slides 仓库作为总幻灯片站点，并且部署 Github Pages（可自定义域名
- 在分仓库中写好项目后，通过 Action 把 site 文件夹中的内容复制到 slides

<!-- 可访问站点 [jujimeizuo' slides](http://slides.jujimeizuo.cn/) -->

具体查看 [:material-github:TonyCrane's Slide Template](https://github.com/TonyCrane/slide-template)

### Netlify

- 注册一个[netlify](https://app.netlify.com/)，然后创建一个站点关联上github仓库
- 在配置/部署里面添加构建命令
- 然后在域名管理添加一个自己的域名

## Reference
- [webpro/reveal-md](https://github.com/webpro/reveal-md)
- [revealjs 官网](https://revealjs.com/)
- [任何利用 revealjs 写出漂亮的 PPT](https://segmentfault.com/a/1190000042014461#item-3-6)
- [TonyCrane's Slide Template](https://github.com/TonyCrane/slide-template)