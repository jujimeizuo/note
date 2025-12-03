---
counter: true
comment: true
---

# Reconstruction-Evaluation

> [!abstract]
> <center>**Reconstruction 常用评价指标**</center>
> ![](/assets/images/cv/slam/nerf-evaluation-1.jpg)

## PSNR

> [!info]
> - Peak Signal-to-Noise Ratio 峰值信噪比
> - 衡量了一张噪声图像和一张干净图像的差异
> - PSNR通过计算原始图像与重建图像之间的均方误差（Mean Squared Error，MSE）来量化它们之间的差异。
> - 两张图象的差异越小，MSE越小, **PSNR就越大，图像质量越好**。

$$
MSE = \frac{1}{mn}\sum_{i=0}^{m-1} \sum_{j=0}^{n-1}[I(i, j) - K(i, j)]^2
\\
PSNR = 10 * \log_{10}(\frac{MAX_I^2}{MSE})
$$

其中 $MAX$ 是动态范围的最大值，即某点 $(i, j)$ 像素范围的最大值，如果图像是 $8$ 位的，则 $MAX = 2^8 - 1 = 255$

```py
from PIL import Image
import numpy as np
 
img1 = np.array(Image.open('original.jpg')).astype(np.float64)
img2 = np.array(Image.open('compress.jpg')).astype(np.float64)
 
 
def psnr(img1, img2):
    mse = np.mean((img1-img2)**2)
    if mse == 0:
        return float('inf')
    else:
        return 20*np.log10(255/np.sqrt(mse))
 
 
if __name__ == "__main__":
    print(psnr(img1, img2))

# -------- #

from skimage.metrics import peak_signal_noise_ratio as psnr
from PIL import Image
import numpy as np
 
 
img1 = np.array(Image.open('original.jpg'))
img2 = np.array(Image.open('compress.jpg'))
 
 
if __name__ == "__main__":
    print(psnr(img1, img2))
```

>[!tip]
> - PSNR接近 50dB ，代表压缩后的图像仅有些许非常小的误差。
> - PSNR大于 30dB ，人眼很难查觉压缩后和原始影像的差异。
> - PSNR介于 20dB 到 30dB 之间，人眼就可以察觉出图像的差异。
> - PSNR介于 10dB 到 20dB 之间，人眼还是可以用肉眼看出这个图像原始的结构，且直观上会判断两张图像不存在很大的差异。
> - PSNR低于 10dB，人类很难用肉眼去判断两个图像是否为相同，一个图像是否为另一个图像的压缩结果。
## MS-SSIM

>[!info]
> - Structural Similarity Index Measure 结构相似性
> - 量了两张图片之间的相似程度/衡量图片的失真程度，考虑了图像的亮度、对比度和结构等方面，而 MS-SSIM。在 SSIM 的基础上引入多个尺度
> - MS-SSIM的值范围在 0 到 1 之间，数值越接近 1 表示重建图像与原始图像的相似度越高，图像质量越好



```py
import cv2
import numpy as np
 
def ms_ssim(img1, img2):
    # 转换为灰度图像
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    
    # 计算MS-SSIM
    weights = np.array([0.0448, 0.2856, 0.3001, 0.2363, 0.1333])  # 不同尺度的权重
    levels = weights.size
    
    mssim = np.zeros(levels)
    mcs = np.zeros(levels)
    
    for i in range(levels):
        ssim_map, cs_map = ssim(img1, img2)
        mssim[i] = np.mean(ssim_map)
        mcs[i] = np.mean(cs_map)
        
        img1 = cv2.resize(img1, (img1.shape[1] // 2, img1.shape[0] // 2), interpolation=cv2.INTER_LINEAR)
        img2 = cv2.resize(img2, (img2.shape[1] // 2, img2.shape[0] // 2), interpolation=cv2.INTER_LINEAR)
    
    # 整体MS-SSIM计算
    overall_mssim = np.prod(mcs[:-1] ** weights[:-1]) * (mssim[-1] ** weights[-1])
    
    return overall_mssim
 
def ssim(img1, img2, k1=0.01, k2=0.03, win_size=11, L=255):
    C1 = (k1 * L) ** 2
    C2 = (k2 * L) ** 2
    
    # 计算均值和方差
    mu1 = cv2.GaussianBlur(img1, (win_size, win_size), 1.5)
    mu2 = cv2.GaussianBlur(img2, (win_size, win_size), 1.5)
    
    mu1_sq = mu1 ** 2
    mu2_sq = mu2 ** 2
    mu1_mu2 = mu1 * mu2
    
    sigma1_sq = cv2.GaussianBlur(img1 * img1, (win_size, win_size), 1.5) - mu1_sq
    sigma2_sq = cv2.GaussianBlur(img2 * img2, (win_size, win_size), 1.5) - mu2_sq
    sigma12 = cv2.GaussianBlur(img1 * img2, (win_size, win_size), 1.5) - mu1_mu2
    
    # 计算相似性度量
    ssim_map = ((2 * mu1_mu2 + C1) * (2 * sigma12 + C2)) / ((mu1_sq + mu2_sq + C1) * (sigma1_sq + sigma2_sq + C2))
    cs_map = (2 * sigma12 + C2) / (sigma1_sq + sigma2_sq + C2)
    
    return ssim_map, cs_map
 
# 读取图像
img1 = cv2.imread('image1.jpg')
img2 = cv2.imread('image2.jpg')
 
# 计算MS-SSIM
ms_ssim_score = ms_ssim(img1, img2)
print("MS-SSIM score:", ms_ssim_score)
```

## LPIPS

>[!info]
> - Learned Perceptual Image Patch Similarity 学习感知图像块相似度
> - 基于学习的感知图像补丁相似性指标，用于评估图像的感知质量
> - LPIPS的得分范围通常是 0 到 1 之间，数值越小表示图像的感知质量越高
> - 与传统的图像质量评估指标（如PSNR和SSIM）相比，LPIPS更加注重于人眼感知的因素，能够更好地捕捉到图像之间的感知差异
> - LPIPS是一种基于学习的指标，它的性能受到所使用的CNN模型和训练数据的影响。因此，在使用LPIPS进行图像质量评估时，需要使用与训练模型相似的数据集和预训练模型，以保证评估结果的准确性和可靠性



```py
import torch
import torchvision.transforms as transforms
from PIL import Image
from models import dist_model
 
# 加载预训练的LPIPS模型
model = dist_model.DistModel()
model.initialize(model='net-lin', net='alex', use_gpu=True)
 
# 图像预处理
preprocess = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.ToTensor()
])
 
# 加载图像并进行预处理
image1 = Image.open('image1.jpg').convert('RGB')
image2 = Image.open('image2.jpg').convert('RGB')
image1 = preprocess(image1).unsqueeze(0)
image2 = preprocess(image2).unsqueeze(0)
 
# 将图像转换为PyTorch张量并计算LPIPS
with torch.no_grad():
    lpips_score = model.forward(image1, image2).item()
 
print("LPIPS score:", lpips_score)
```

## Comparison

>[!quote]
>- PSNR（Peak Signal-to-Noise Ratio）：PSNR是一种常用的图像质量评估指标，用于衡量原始图像与重建图像之间的差异。它通过计算均方误差（MSE）来量化两个图像之间的差异，数值越高表示图像质量越好。
>- MS-SSIM（Multi-Scale Structural Similarity Index）：MS-SSIM是一种结构相似性指标，它在计算图像相似性时考虑了多个尺度的信息。与传统的结构相似性指标（SSIM）相比，MS-SSIM将图像分解成多个尺度，并在每个尺度上计算结构相似性指标，最后取平均值作为最终的相似性评估。MS-SSIM相较于PSNR更能反映人眼对于图像感知的差异。
> - LPIPS（Learned Perceptual Image Patch Similarity）：LPIPS是一种学习的感知图像补丁相似性指标，它通过训练神经网络来学习图像补丁之间的感知相似性。LPIPS考虑了人眼对于图像感知的敏感性，通过计算图像补丁之间的感知距离来评估图像质量。与传统的结构相似性指标（如SSIM）相比，LPIPS在学习感知距离时更加准确和全面。
> - 这些指标在图像质量评估中都有广泛的应用。PSNR主要用于衡量图像的重建误差，而MS-SSIM和LPIPS更加关注人眼对图像感知的差异。在实际应用中，不同的指标可以结合使用，以综合评估图像质量。

## Reference

- [NeRF常用评价指标都是什么意思？PSNR、SSIM、LPIPS详解](https://www.bilibili.com/video/BV1eG4y1D73A/?vd_source=5e048b202705330980eefcc9a56cc5d0)
- [NeRF 模型评价指标PSNR,MS-SSIM, LPIPS 详解和python实现](https://blog.csdn.net/qq_35831906/article/details/131185949)