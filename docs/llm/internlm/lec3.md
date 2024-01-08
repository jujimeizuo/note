---
counter: true
comment: true
---

# 基于 InternLM 和 LangChain 搭建你的知识库

!!! abstract
    学习自 [基于 InternLM 和 LangChain 搭建你的知识库](https://github.com/InternLM/tutorial/blob/main/langchain/readme.md)

## 搭建流程

1. 环境配置
2. 知识库搭建
      1. 数据收集
      2. 加载数据
      3. 构建向量数据库
3. 接入 LangChain
4. 构建检索问答链
      1. 加载向量数据库
      2. 实例化自定义 LLM 与 Prompt Template
      3. 构建检索问答链
5. 部署 Web Demo

## 作业

1. 复现课程知识库助手搭建过程 (截图)

<center><img src="https://cdn.jujimeizuo.cn/note/llm/internlm/hw_3_1.jpg"></center>

2. 选择一个垂直领域，收集该领域的专业资料构建专业知识库，并搭建专业问答助手，并在 OpenXLab 上成功部署（截图，并提供应用地址）