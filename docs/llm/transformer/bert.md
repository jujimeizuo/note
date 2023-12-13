---
counter: true
comment: true
---

# BERT

!!! abstruct
    - BERT 作为 NLP 预训练模型里的经典模型之一，效果非常好。
    - BERT 的模型代码和模型参数开源，都可以基于这个强大的模型组件搭建自己的 NLP 系统，也节省开始训练语言处理模型所需要的时间、精力、知识和资源。
    - BERT的全称是 Bidirectional Encoder Representation from Transformers，即双向 Transformer 的 Encoder，因为decoder是不能获要预测的信息的。
    - 模型的主要创新点都在pre-train方法上，即用了Masked LM和Next Sentence Prediction两种方法分别捕捉词语和句子级别的representation。

## Introduction

BERT 首先在大规模无监督语料上进行预训练，然后在预训练好的参数基础上增加一个与任务相关的神经网络层，并在该任务的数据上进行微调，最终取得很好的效果。

BERT的训练过程可以简述为：预训练+微调（finetune），这是近几年 NLP 解决方案的主流范式。

<center><img src="https://cdn.jujimeizuo.cn/note/llm/transformer/bert/tf.png" alt="预训练+微调"></center>

## 模型结构

BERT模型的结构如下图最左：

<center><img src="https://cdn.jujimeizuo.cn/note/llm/transformer/bert/bert-structure.png" alt="BERT模型结构"></center>

- 对比 OpenAI GPT，BERT 是双向的 Transformer block 连接，就像单向 RNN 和双向 RNN 的区别，效果会更好。
- 对比 ELMo，虽然都是“双向”，但目标函数不同。
    - ELMo 是分别以 $P(w_i|w_1,...,w_{i-1})$ 和 $P(w_i|w_{i+1},...,w_n)$  作为目标函数，独立训练出两个 representation 然后连接
    - BERT 是以 $P(w_i | w_1,...,w_{i-1},w_{i+1},...,w_n)$ 作为目标函数训练 LM

命名表示层数为L（Transformer Blocks），隐藏层数为H，自注意力头数量为A。原始论文中的两种模型：

- BERT_base(L=12,H=768,A=12; parameters=110M)
- BERT_large(L=24,H=1024,A=16; parameters=340M)

## Embedding

这里的 Embedding 由三种 Embedding 求和组成：

<center><img src="https://cdn.jujimeizuo.cn/note/llm/transformer/bert/embedding.png"></center>

- `Token Embedding`：词向量，第一个单词是 CLS 标志，可以用于之后的分类任务
- `Segment Embedding`：句子向量，用于区分两个句子，因为预训练不光做 LM 还要做以两个句子为输入的分类任务
- `Position Embedding`：位置向量，用于区分单词在句子中的位置，和之前的 Transformer 不一样，不是三角函数而是学习出来的

## Pre-training

### Masked LM （MLM）

- 第一步预训练的目标就是做预言模型，从上文模型结构中看到了这个模型的不同，即 bidirectional。

!!! note "为什么要 bidirectional"
    如果使用预训练模型处理其他任务，那人们想要的不止某个词的左边的信息，而是左右两边的信息，而考虑到这点的模型 ELMo 只是将 left-to-right 和 right-to-left 分别训练拼接起来。直觉上来讲我们其实想要一个 deeply bidirectional 的模型，但是普通的LM又无法做到，因为在训练时可能会“穿越”，所以作者用了一个加mask的trick。

- 在训练过程中作者随机 mask 15% 的 token，而不是把像 CBOW 一样把每个词都预测一遍。**最终的损失函数只计算被 mask 掉那么 token**。
- mask 如何做也是有技巧的，如果一直用标记 [MASK] 代替（在实际预测时是碰不到这个标记的）会影响模型，所以随机 mask 的时候 10% 的单词会被替代成其他单词，10% 的单词不替换，剩下 80% 才被替换为 [MASK]。要注意的是 Masked LM 预训练阶段模型是不知道真正被 mask 的哪个词，所以模型每个词都要关注。

!!! note "为什么这么分配比例"

    <center><img src="https://pic1.zhimg.com/80/v2-f25d1b04b74ea4210c3368a2b609f63c_1440w.webp"></center>
    
    如果句子中的某个Token100%都会被mask掉，那么在fine-tuning的时候模型就会有一些没有见过的单词。加入随机Token的原因是因为Transformer要保持对每个输入token的分布式表征，否则模型就会记住这个[mask]是token ’hairy‘。至于单词带来的负面影响，因为一个单词被随机替换掉的概率只有15%*10% =1.5%，这个负面影响其实是可以忽略不计的。

- 因为序列长度太大（512）会影响训练速度，所以 90% 的 steps 都用 seq_len=128，10% 的 steps 用 seq_len=512。

### Next Sentence Prediction （NSP）

- 因为涉及到QA和NLI之类的任务，增加了第二个预训练任务，目的是让模型理解两个句子之间的联系。
- Next Sentence Prediction（NSP）的任务是判断句子B是否是句子A的下文。如果是的话输出’IsNext‘，否则输出’NotNext‘。训练数据的生成方式是从平行语料中随机抽取的连续两句话，其中50%保留抽取的两句话，它们符合IsNext关系，另外50%的第二句话是随机从预料中提取的，它们的关系是NotNext的。
- 预训练的时候可以达到 97%-98% 的准确度。
- **作者特意说了语料的选取很关键，要选用document-level的而不是sentence-level的，这样可以具备抽象连续长序列特征的能力。**

## Fine-tuning

微调是简单的，因为Transformer中的自注意力机制允许BERT通过交换适当的输入和输出来建模许多下游任务--不管它们涉及单个文本还是文本对。对于NSP任务来说，其条件概率表示为 $P=softmax(CW^T)$，其中 C 是 BERT 输出中的 [CLS] 符号，W 是可学习的权值矩阵。

微调的任务包括：

- 基于句子对的分类任务
- 基于单个句子的分类任务
- 问答任务
- 命名实体识别NER

下图展示了BERT在11个不同任务中的模型，它们只需要在BERT的基础上再添加一个输出层便可以完成对特定任务的微调。这些任务类似于我们做过的文科试卷，其中有选择题，简答题等等。图3中其中Tok表示不同的Token，E 表示嵌入向量，$T_i$ 表示第 i 个Token在经过BERT处理之后得到的特征向量。

<center><img src="https://cdn.jujimeizuo.cn/note/llm/transformer/bert/fine-tuning.png"></center>

整体 Fine-Tuning 过程：

1. 构建图结构，截取目标张量，添加新层
2. 夹在目标张量权重
3. 训练新层
4. 全局微调

## Reference

- [图解 BERT](https://github.com/datawhalechina/learn-nlp-with-transformers/blob/main/docs/%E7%AF%87%E7%AB%A02-Transformer%E7%9B%B8%E5%85%B3%E5%8E%9F%E7%90%86/2.3-%E5%9B%BE%E8%A7%A3BERT.md)
- [【深度学习】BERT 详解](https://zhuanlan.zhihu.com/p/130913995)
- [【NLP】Google BERT模型原理详解](https://zhuanlan.zhihu.com/p/46652512)
- [NLP与深度学习（五）BERT预训练模型](https://www.cnblogs.com/zackstang/p/15358061.html)