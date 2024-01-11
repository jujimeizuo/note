---
counter: true
comment: true
---


# 书生·浦语大模型全链路开源开放体系

!!! abstract
    学习自 [书生·浦语大模型全链路开源开放体系](https://www.bilibili.com/video/BV1Rc411b7ns/)

## 书生·浦语大模型系列

- 轻量级：InternLM-7B
- 中量级：InternLM-20B
- 重量级：InternLM-123B

<center><img src="https://cdn.jujimeizuo.cn/note/llm/internlm/20B-pf.jpg"></center>

## 从模型到应用

<center><img src="https://cdn.jujimeizuo.cn/note/llm/internlm/model2app.jpg"></center>

## 书生·浦语大模型全链路开源开放体系

<center><img src="https://cdn.jujimeizuo.cn/note/llm/internlm/structure.jpg"></center>

### 数据：书生·万卷

<center><img src="https://cdn.jujimeizuo.cn/note/llm/internlm/data.jpg"></center>

具体查看 [openDataLab](https://opendatalab.com/)。

### 预训练：InternLM-Train

<center><img src="https://cdn.jujimeizuo.cn/note/llm/internlm/internlm-train.jpg"></center>

### 微调：XTuner

> 大语言模型的下游应用中，增量续训和有监督微调是经常会用到两种方式。
>
> - **增量续训**
>       - 使用场景：让基座模型学习新知识，如某个垂类领域知识
>       - 训练数据：文章、数据、代码等
> - **有监督微调**
>       - 使用场景：让模型学会理解和遵循各种指令，或者注入少许领域知识
>       - 训练数据：高质量的对话、问答数据

<center><img src="https://cdn.jujimeizuo.cn/note/llm/internlm/xtuner.jpg"></center>

### 评测：OpenCompass


<center><img src="https://cdn.jujimeizuo.cn/note/llm/internlm/opencompass.jpg"></center>

<center><img src="https://cdn.jujimeizuo.cn/note/llm/internlm/opencompass-structure.jpg"></center>

### 部署：LMDeploy

<center><img src="https://cdn.jujimeizuo.cn/note/llm/internlm/lmdeploy.jpg"></center>


### 应用：Lagent、AgentLego

<center><img src="https://cdn.jujimeizuo.cn/note/llm/internlm/lagent.jpg"></center>

<center><img src="https://cdn.jujimeizuo.cn/note/llm/internlm/agentlego.jpg"></center>
