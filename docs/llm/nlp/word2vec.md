---
counter: true
comment: true
---

# Word2Vec

!!! abstract

    <center><img src="https://cdn.jsdelivr.net/gh/jujimeizuo/note@gh-pages/assets/images/llm/nlp/word2vec/summary.png"></center>


    Word2Vec 的特点是能够将单词转化为向量来表示，这样词与词之间就可以定量地去度量它们之间的关系，挖掘词之间的联系。

    最早的词向量采用 One-Hot 编码，又称一位有效编码，每个词向量维度大小为整个词汇表的大小，对于每个具体的词汇表中的词，将对应的位置置为 1.


## Word2Vec 基本思想


采用One-Hot编码方式来表示词向量非常简单，但缺点也是显而易见的，一方面我们实际使用的词汇表很大，经常是百万级以上，这么高维的数据处理起来会消耗大量的计算资源与时间。另一方面，One-Hot编码中所有词向量之间彼此正交，没有体现词与词之间的相似关系。

　　Distributed representation可以解决One-Hot编码存在的问题，它的思路是通过训练，将原来One-Hot编码的每个词都映射到一个较短的词向量上来，而这个较短的词向量的维度可以由我们自己在训练时根据任务需要来自己指定。

　　下图是采用Distributed representation的一个例子，我们将词汇表里的词用"Royalty","Masculinity", "Femininity"和"Age"4个维度来表示，King这个词对应的词向量可能是(0.99,0.99,0.05,0.7)。当然在实际情况中，我们并不能对词向量的每个维度做一个很好的解释。

<center><img src="https://cdn.jsdelivr.net/gh/jujimeizuo/note@gh-pages/assets/images/llm/nlp/word2vec/dr.png"></center>

有了用Distributed Representation表示的较短的词向量，我们就可以较容易的分析词之间的关系了，比如我们将词的维度降维到2维，有一个有趣的研究表明，用下图的词向量表示我们的词时，我们可以发现：

$$
\vec{King} - \vec{Man} + \vec{Woman} \approx \vec{Queen}
$$

<center><img src="https://cdn.jsdelivr.net/gh/jujimeizuo/note@gh-pages/assets/images/llm/nlp/word2vec/kmwq.png"></center>

可见我们只要得到了词汇表里所有词对应的词向量，那么我们就可以做很多有趣的事情了。不过，怎么训练才能得到合适的词向量呢？针对这个问题，Google的Tomas Mikolov在他的论文中提出了CBOW和Skip-gram两种神经网络模型。

## Word2Vec 原理

Word2Vec 的训练模型本质上是只具有一个隐含层的神经元网络。

它的输入采用 One-Hot 编码的词汇表向量，它的输出也是 One-Hot 编码的词汇表向量。使用所有的样本，训练这个神经网络，等到收敛之后，从输入层到隐含层的那些权重，便是每一个词的采用Distributed Representation的词向量。比如，上图中单词的Word embedding后的向量便是矩阵 $W_{V \times N}$ 的第i行的转置。这样我们就把原本维数为V的词向量变成了维数为N的词向量（N远小于V），并且词向量间保留了一定的相关关系。

Google的Mikolov在关于Word2Vec的论文中提出了CBOW和Skip-gram两种模型，CBOW适合于数据集较小的情况，而Skip-Gram在大型语料中表现更好。其中CBOW如下图左部分所示，使用围绕目标单词的其他单词（语境）作为输入，在映射层做加权处理后输出目标单词。与CBOW根据语境预测目标单词不同，Skip-gram根据当前单词预测语境，如下图右部分所示。假如我们有一个句子“There is an apple on the table”作为训练数据，CBOW的输入为（is,an,on,the），输出为apple。而Skip-gram的输入为apple，输出为（is,an,on,the）。

<center><img src="https://cdn.jsdelivr.net/gh/jujimeizuo/note@gh-pages/assets/images/llm/nlp/word2vec/cbow-skipgram.png"></center>

## CBOW

<center><img src="https://cdn.jsdelivr.net/gh/jujimeizuo/note@gh-pages/assets/images/llm/nlp/word2vec/cbow-net.png"></center>

1. 输入层：上下文单词的 One-Hot 编码词向量，V 为词汇表单词个数，C 为上下文单词个数。以 “There is an apple on the table” 为例，C=4，所以模型输入是（is,an,on,the）4 个单词的 One-Hot 编码词向量。
2. 初始化一个权重矩阵 $W_{V \times N}$，然后用所有输入的 One-Hot 编码词向量左乘该矩阵，得到维数为 N 的向量 $w_1,w_2,...,w_c$，这里的 N 由自己根据任务需要设置。
3. 将所得的向量 $w_1,w_2,...,w_c$ 求和取平均作为隐藏层向量 h。
4. 初始化另一个权重矩阵 $W_{N \times V}^\prime$，用隐藏层向量 h 左乘 $W_{N \times V}^\prime$，在经激活函数处理得到 V 维的向量 y，y 的每一个元素代表相对应的每个单词的概率分布。
5. y 中概率最大的元素所指示的单词为预测出的中间词（target word）与 true label 的 One-Hot 编码词向量做比较，误差越小越好（根据误差更新两个权重矩阵）。

在训练前需要定义好损失函数（一般为交叉熵代价函数），采用梯度下降算法更新 $W$ 和 $W^\prime$。训练完毕后，输入层的每个单词与矩阵 W 相乘得到的向量就是我们想要的 Distributed Representation 表示的词向量，也叫 word embedding。因为 One-Hot 编码词向量中只有一个元素为 1，其他都为 0，所以第 i 个词向量乘以矩阵 W 后，得到的就是矩阵的第 i 行，所以这个矩阵也叫做 look up table，有了 look up table 就可以免去训练过程，直接查表得到单词的词向量。

## Skip-gram

<center><img src="https://cdn.jsdelivr.net/gh/jujimeizuo/note@gh-pages/assets/images/llm/nlp/word2vec/skip-gram-net.png"></center>

Skip-Gram 是给定 input word 来预测上下文，其模型结构如上图所示。它的做法是，将一个词所在的上下文中的词作为输出，而那个词本身作为输入，也就是说，给出一个词，希望预测可能出现的上下文的词。通过在一个大的语料库训练，得到一个从输入层到隐含层的权重模型。“apple”的上下文词是（’there’，’is’，’an’，’on’,’the’,’table’）.那么以apple的One-Hot词向量作为输入，输出则是（’there’，’is’，’an’，’on’,’the’,’table’）的One-Hot词向量。训练完成后，就得到了每个词到隐含层的每个维度的权重，就是每个词的向量（和CBOW中一样）。

假如我们有一个句子“There is an apple on the table”。

1. 首先选句子中间的一个词作为输入词，比如选取“apple”作为 input word。
2. 有了 input word 以后，再定义一个叫做 skip_window 的参数，它代表着从当前 input word 的一侧（左边或右边）选取词的数量。如果设置 skip_window=2，那么最终获得窗口中的词（包括 input word 在内）就是[‘is’,’an’,’apple’,’on’,’the’ ]。skip_window=2代表着选取左input word左侧2个词和右侧2个词进入我们的窗口，所以整个窗口大小span=2x2=4。另一个参数叫num_skips，它代表着我们从整个窗口中选取多少个不同的词作为我们的output word，当skip_window=2，num_skips=2时，我们将会得到两组 (input word, output word) 形式的训练数据，即 ('apple', 'an')，('apple', 'one')。
3. 神经网络基于这些训练数据中每对单词出现的次数习得统计结果，并输出一个概率分布，这个概率分布代表着到我们词典中每个词有多大可能性跟input word同时出现。举个例子，如果我们向神经网络模型中输入一个单词“中国“，那么最终模型的输出概率中，像“英国”， ”俄罗斯“这种相关词的概率将远高于像”苹果“，”蝈蝈“非相关词的概率。因为”英国“，”俄罗斯“在文本中更大可能在”中国“的窗口中出现。我们将通过给神经网络输入文本中成对的单词来训练它完成上面所说的概率计算。
4. 通过梯度下降和反向传播更新矩阵 W
5. W 中的行向量即为每个单词的 Word embedding 表示

!!! note "总结"
    CBOW 和 Skip-gram 最理想情况下的实现，即训练迭代两个矩阵 $W$ 和 $W^\prime$，之后再输出层采用 softmax 函数来计算输出各个词的概率。但在实际应用中这种方法的训练开销很大，不具有很强的实用性，为了使得模型便于训练，有学者提出了 Hierarchical Softmax 和 Negative Sampling 两种改进方法。

## Hierarchical Softmax

Hierarchical Softmax 对原模型的改进主要有两点

- 第一点是从输入层到隐藏层的映射，没有采用原先的与矩阵 W 相乘然后相加求平均的方法，而是直接对所有输入的词向量求和。假设输入的词向量为（0，1，0，0）和（0，0，0，1），那么隐藏层的向量为（0，1，0，1）。
- Hierarchical Softmax 的第二点改进是采用哈夫曼树来替换了原先的从隐藏层到输出层的矩阵 $W^\prime$。哈夫曼树的叶节点个数为词汇表的单词个数 V，一个叶节点代表一个单词，而从根结点到叶节点的路径确定了这个单词最终输出的词向量。

<center><img src="https://cdn.jsdelivr.net/gh/jujimeizuo/note@gh-pages/assets/images/llm/nlp/word2vec/hs-huffman.png"></center>

具体来说，这棵哈夫曼树除了根节点以外的所有非叶节点中都含有一个由参数 $\theta$ 确定的 sigmoid 函数，不同节点的 $\theta$ 不一样。训练时隐藏层的向量与这个 sigmoid 函数进行运算，根据结果进行分类，若分类为负类则沿左子树向下传递，编码为 0；若分类为正类则沿右子树向下传递，编码为 1。最终到达叶节点，叶节点的向量即为输出的词向量。

## Negative Sampling

尽管哈夫曼树的引入为模型的训练缩短了许多开销，但对于一些不常见、较生僻的词汇，哈夫曼树在计算它们的词向量时仍然需要做大量的运算。

负采样是另一种提高 Word2Vec 效率的方法，它是基于这样的观察：训练一个神经网络意味着使用一个训练样本就要稍微调整一下神经网络中所有的权重，这样才能确保预测训练样本更加精确，如果能设计一种方法每次只更新一部分权重，那么计算复杂度将大大降低。

将以上观察引入 Word2Vec 就是：当通过（”fox”, “quick”）词对来训练神经网络时，我们回想起这个神经网络的“标签”或者是“正确的输出”是一个one-hot向量。也就是说，对于神经网络中对应于”quick”这个单词的神经元对应为1，而其他上千个的输出神经元则对应为0。使用负采样，我们通过随机选择一个较少数目（比如说5个）的“负”样本来更新对应的权重。（在这个条件下，“负”单词就是我们希望神经网络输出为0的神经元对应的单词）。并且我们仍然为我们的“正”单词更新对应的权重（也就是当前样本下”quick”对应的神经元仍然输出为1）。

## Reference

- [Word2Vec详解](https://zhuanlan.zhihu.com/p/61635013)
- [深入浅出Word2Vec原理解析](https://zhuanlan.zhihu.com/p/114538417)
- [NLP之——Word2Vec详解](https://www.cnblogs.com/guoyaohua/p/9240336.html)