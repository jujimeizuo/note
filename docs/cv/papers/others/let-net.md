---
counter: true
comment: true
---

# LET-NET

> [!Abstract]
> - paper：[:book: LET-NET: Breaking of brightness consistency in optical flow with a lightweight CNN network](https://arxiv.org/pdf/2310.15655)
> - code：[:material-github: LET-NET](https://github.com/linyicheng1/LET-NET?tab=readme-ov-file)


## Idea

1. 提出**轻量级 CNN** 结合 LK 光流进行**特征点提取**和**图像一致性计算**（特征图 F 和分数图 S），打破**亮度一致性假设**（亮度一致性 $\to$ 同一像素的卷积特征不变），以适应 **HDR 环境**。
2. 提取最快速的深度学习角点（证明局部信息足以提取角点）。
3. 提出了一种损失函数 mNRE 来提取图像中的局部不变量，并改进了角点提取中的峰值损失。

<center><img src="https://cdn.jujimeizuo.cn/note/cv/slam/LET-NET-1.jpg" alt="Pipeline of LET-NET"></center>


## Experiments

项目有问题，[issue](https://github.com/linyicheng1/LET-NET/issues/23)。

