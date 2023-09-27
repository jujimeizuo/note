---
counter: true
comment: true
---

# 虚拟环境


## virtualenv

- `pip install virtualenv`: 安装
- `virtualenv 'name'`: 创建虚拟环境
- `cd venv && source ./vin/activate`: 激活虚拟环境
- `deactivate`: 退出虚拟环境
- `rm -rf venv`: 删除虚拟环境

## conda

- 下载 anaconda 安装的 python 直接可以使用 conda 工具
- `conda create --name 'name' python=3.9 -y`: 创建虚拟环境
- `source activate venv`: 激活虚拟环境
- `source deactivate`: 退出虚拟环境
- `conda remove --name 'name' --all`: 删除虚拟环境
- `conda info -e` / `conda env list`: 列出系统存在的虚拟环境
- `conda list`: 查看当前环境下已安装的包
- `conda list --name 'name'`: 查看某个指定环境的已安装包
- `conda search numpy`: 查看 package 信息
- `conda install --name 'name' numpy`: 安装package，如果不用-n指定环境名称，则被安装在当前激活环境
- `conda update --name 'name' numpy`: 更新 package
- `conda remove --name 'name'numpy`: 删除 package