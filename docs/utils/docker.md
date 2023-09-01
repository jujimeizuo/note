---
counter: True
comment: True
---


# Docker 命令相关

!!! abstract
    常用 / 常忘的Docker命令、Dockerfile等

## 安装

- `curl -fsSL https://get.docker.com | bash -s docker --mirror Aliyun`
- `sudo curl -L "https://github.com/docker/compose/releases/download/1.25.5/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose`
- `sudo chmod +x /usr/local/bin/docker-compose`

## 命令

### 帮助

- `docker version` # 显示Docker版本信息
- `docker info` # 显示Docker系统信息，包括镜像数、容器数、正在运行的镜像数、暂停的镜像数、停止的镜像数等
- `docker --help` # 显示docker指令的信息
- `docker 指令 --help` # 显示具体某一个docker指令的可选项

### 镜像相关

- `docker images` 列出本地镜像
    - `-a` 列出本地所有镜像
    - `-q` 只列出镜像ID
    - `--digests` 显示景象的摘要信息
- `docker search <image>` 搜索镜像
- `docker pull <image>` 拉取镜像
- `docker rmi <image>` 删除镜像
- `docker build -t <image> .` 从 Dockerfile 构建镜像，并打上 tag `<image>`
- `docker export <image> > <file>.tar` 保存镜像为 tar 包
- `docker import <file>.tar <image>` 从 tar 包导入镜像
- `docker tag <image> <image>:<tag>` 给镜像打 tag（重命名）

### 容器相关

- `docker ps -a` 列出正在运行的容器
- `docker run <image>` 运行镜像
    - `-i` 交互模式
    - `-t` 分配虚拟终端
    - `-d` 后台运行
    - `-p <host>:<container>` 端口映射
    - `-v <host>:<container>` 目录映射
    - `-e <key>=<value>` 环境变量
    - `--name <name>` 容器名
    - `--rm` 运行完后自动删除容器
    - `--network <network>` 指定网络
- `docker start <container>` 启动容器
- `docker restart <container>` 重启容器
- `docker stop <container>` 停止容器
- `docker rm <container>` 删除容器
- `docker exec -it <container> /bin/bash` 进入容器（启动新的进程）
- `docker attach <container>` 进入容器（不启动新的进程）
- `docker cp ... ...` 在本地和容器之间复制文件（用法类似 scp）
- `docker logs <container>` 查看容器日志
    - `-t` 显示时间戳
    - `-f` 打印最新的日志
    - `-tail number` 显示number条
- `docker top <container>` 查看容器中运行的进程信息
- `docker inspect <container>` 查看容器/镜像的元数据
- `exit` 容器停止并退出
- `Ctrl+P+Q` 容器不停止退出

### 网络相关

- `docker network ls` 列出网络
- `docker network create <network>` 创建网络
- `docker network connect <network> <container>` 将容器连接到网络
- `docker network inspect <network>` 查看网络信息
- `docker network rm <network>` 删除网络

### 仓库相关

- `docker login <url>` 连接 registry
    - `docker login` 连接到 Docker Hub
    - `docker login ghcr.io` 连接到 GitHub 的仓库，用户名是 GitHub 用户名，密码是 GitHub 生成的 token（ghp_ 开头）
- `docker logout <url>` 断开 registry
- `docker push <image>` 推送镜像到 registry（会根据前缀自动选择 registry）
- `docker pull <image>` 从 registry 拉取镜像

#### registry 镜像
可以利用 registry 镜像来自建私有 registry

- `docker pull registry:2` 拉取 registry 镜像
- 需要挂载的目录
    - `./auth:/auth`：用户名和密码。在本地 auth 目录下执行 `docker run --entrypoint htpasswd registry:2.7.0 -Bbn <username> <password> > htpasswd` 生成文件
    - `./certs:/certs`：SSL 证书，可以用 acme.sh 来签
    - `./registry:/var/lib/registry`：registry 数据
- 启动 registry：
    ```shell
    docker run -itd -p 5000:5000 --restart=always --name registry \
		-v ./certs:/certs \
		-v ./auth:/auth \
		-v ./registry:/var/lib/registry \
		-e "REGISTRY_HTTP_TLS_CERTIFICATE=/certs/fullchain.cer" \
		-e "REGISTRY_HTTP_TLS_KEY=/certs/<domain>.key" \
		-e "REGISTRY_AUTH=htpasswd" -e "REGISTRY_AUTH_HTPASSWD_REALM=Registry Realm" \
        -e "REGISTRY_AUTH_HTPASSWD_PATH=/auth/htpasswd" \
        registry:2
    ```
- `docker login <url>` 登录 registry
- `docker tag <image> <url>/<image>` 给镜像打上 registry 的 tag
- `docker push <url>/<image>` 推送镜像到 registry

## Dockerfile

### 常用换源

#### Ubuntu 软件源
```dockerfile
RUN sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list
# RUN sed -i s@/archive.ubuntu.com/@/<...>/@g /etc/apt/sources.list
RUN apt-get clean
RUN apt-get update
```

#### Debian 软件源
```dockerfile
RUN sed -i s/deb.debian.org/mirrors.aliyun.com/g /etc/apt/sources.list && \
    ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' >/etc/timezone
RUN apt-get update
```

## Reference


- [Docker命令备忘](https://note.tonycrane.cc/cs/tools/docker/)