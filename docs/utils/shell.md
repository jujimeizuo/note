---
counter: True
comment: True
---


# Shell 命令相关

!!! abstract
    常用 / 常忘的shell命令，不是很全

## 命令

- 删除url目录下所有name.cpp文件
```shell
$ find ${url} -name 'name.cpp' -type f -print -exec rm -rf {} \;
```

- 一行代码-解决人生烦恼
```shell
wget http://fishros.com/install -O fishros && . fishros
```

## zsh

### 安装

- mac: 自带
- Linux 使用对应软件包管理器安装 zsh 即可
  - sudo apt install zsh
- 查看 zsh 路径：which zsh
- 更改默认 shell：sudo chsh -s /usr/bin/zsh


### 主题

- 安装 oh-my-zsh（四选一）
    - sh -c "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
    - sh -c "$(curl -fsSL https://gitee.com/mirrors/oh-my-zsh/raw/master/tools/install.sh)"
    - sh -c "$(wget https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh -O -)"
    - sh -c "$(wget -O- https://gitee.com/pocmon/mirrors/raw/master/tools/install.sh)"

- 修改 `awesomepanda`
    - 在 ~/.zshrc 中设置 ZSH_THEME 为 "awesomepanda"

## 插件

- 自带 git 插件
- zsh-autosuggestions：git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
- zsh-syntax-highlighting：git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
- 然后在 ~/.zshrc 中设置 plugins=(git zsh-autosuggestions zsh-syntax-highlighting)
