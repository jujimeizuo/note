---
counter: True
---

# gitbook

## 前置要求

### nodejs

高版本可能不兼容，需要版本在v10左右。 [https://nodejs.org/download/release/v10.21.0/](https://nodejs.org/download/release/v10.21.0/)

### 更换镜像

```bash
npm config get registry
npm config set registry https://registry.npm.taobao.org
```

## 安装

```bash
npm uninstall -g gitbook-cli
```

安装完之后用`gitbook -V`查看版本，自动install gitbook。

## 使用

```bash
gitbook -V      查看版本号
gitbook init    初始化
gitbook serve   预览
gitbook build   生成
gitbook build --gitbook=2.6.7 生成时指定gitbook的版本, 本地没有会先下载
gitbook uninstall 2.6.7   卸载指定版本号的gitbook
gitbook fetch [version]      获取[版本]下载并安装<版本>
gitbook --help   显示帮助文档
gitbook ls-remote  列出NPM上的可用版本：
```
