---
counter: True
comment: True
---

# ffmpeg

!!! abstract
    ffmpeg 相关

## Installation

- Download Source Code

```bash
wget https://www.ffmpeg.org/releases/ffmpeg-7.0.tar.gz
tar -zxvf ffmpeg-7.0.tar.gz
```

- Compile

```bash
cd ffmpeg-7.0
./configure --prefix=/usr/local/ffmpeg --enable-openssl --disable-x86asm
make && make install
```

- Add to PATH

```bash
vim ~/.bashrc
export PATH=$PATH:/usr/local/ffmpeg/bin
source ~/.bashrc
```

- Check

```bash
ffmpeg -version
```

## Usage

- 视频转图片

```bash
ffmpeg -i ./data/data_classroom/classroom.mov -qscale:v 1 -qmin 1 -vf fps=8 /path/to/data/input/%04d.jpg
```

- ...

## Reference

- [FFmpeg教程（超级详细版）](https://juejin.cn/post/7094619578356989966)