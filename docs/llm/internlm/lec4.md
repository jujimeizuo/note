---
counter: true
comment: true
---

# XTuner 大模型单卡低成本微调实战

!!! abstract
    学习自 [XTuner 大模型单卡低成本微调实战](https://www.bilibili.com/video/BV1yK4y1B75J)


## Finetune

> LLM 的下游应用中，**增量预训练**和**指令跟随**是经常会用到两种的微调模式

### 增量预训练微调

- 使用场景：让基座模型学习到一些新知识，如某个垂类领域的常识
- 训练数据：文章、书籍、代码等

- 为了让 LLM 知道什么时候开始一段话，什么时候结束一段话，实际训练时需要对数据添加起始符（BOS）和结束符（EOS），大多数的模型都是使用 `<s>` 作为起始符，`</s>` 作为结束符


### 指令跟随微调

- 使用场景：让模型学会对话模版，根据人类指令进行对话
- 训练数据：高质量的对话，问答数据

!!! example ""
    在实际对话中，通常会有三种角色

    - `System` 给定一些上下文，比如“你是一个安全的 AI 助手”
    - `User` 实际用户，会提出一些问题，比如 “世界第一高峰是”
    - `Assistant` 根据 User 的输入，结合 System 的上下文信息，做出回答，比如 “珠穆朗玛峰”

    **在使用对话模型时，通常是不会感知到这三种角色**

- 对话模版

<center><img src="https://cdn.jujimeizuo.cn/note/llm/internlm/ft-1-chat-template.jpg"></center>

- 不同于增量预训练微调，数据中会有 Input 和 Output 希望模型学会的是答案（Output），而不是问题（Input），训练时只会对答案（Output）部分计算 Loss
- 训练时，会和推理时保持一致，对数据添加相对应的对话模版


## LoRA & QLoRA

<center><img src="https://cdn.jujimeizuo.cn/note/llm/internlm/LoRA-QLoRA.jpg"></center>

## Xtuner

- **傻瓜化**：以 配置文件 的形式封装了大部分微调场景
- **轻量级**：对于 7B 参数量的 LLM，微调所需的最小显存仅为 8GB

### 快速上手

#### 使用流程

1. 安装

```bash
pip install xtuner
```

2. 挑选配置模版

```bash
xtuner list-cfg -p internlm_20b
```

3. 一键训练

```bash
xtuner train internlm_20b_qlora_oasst1_512_e3
```

| Config   | Description                           |
| -------- | ------------------------------------- |
| 模型名   | internlm_20b (无 chat 代表是基座模型) |
| 使用算法 | qlora                                 |
| 数据集   | oasst1                                |
| 数据长度 | 512                                   |
| Epoch    | e3, epoch 3                           |

#### 自定义训练

1. 拷贝配置模版
2. 修改配置模版
3. 启动训练

| 常用超参            | Description                                            |
| ------------------- | ------------------------------------------------------ |
| data_path           | 数据路径或 HuggingFace 仓库名                          |
| max_length          | 单条数据最大 Token 数，超过则截断                      |
| pack_to_max_length  | 是否将多条短数据拼接到 max_length，提高 GPU 利用率     |
| accumulative_counts | 梯度累积，每多少次 backward 更新一次参数               |
| evaluation_inputs   | 训练过程中，会根据给定的问题进行推理，便于观测训练状态 |
| evaluation_freq     | Evaluation 的测评间隔 iter 数                          |

#### 对话

为了便于开发者查看训练效果，Xtuner 提供了一键对话借口

1. Float16 模型对话

```bash
xtuner chat internlm/internlm-chat-20b
```

2. 4bits 模型对话

```bash
xtuner chat internlm/internlm-chat-20b --bits 4
```

3. 加载 Adapter 模型对话

```bash
xtuner chat internlm/internlm-chat-20b --adapter $ADAPTER_DIR
```

同时，Xtuner 还支持工具类模型的对话

### XTuner 数据引擎

#### 数据处理流程

<center><img src="https://cdn.jujimeizuo.cn/note/llm/internlm/xunter-pipe-1.jpg"></center>

#### 多数据样本拼接（Pack Dataset）

增强并行性，充分利用 GPU 资源！

## 8 GB 显卡玩转 LLM

### XTuner 加速方式

- `Flash Attention`：`Flash Attention` 将 `Attention` 计算并行化，避免了计算过程中 `Attention Score NxN` 的显存占用（训练过程中的 N 都比较大）

- `DeepSpeed ZeRO`
    - `ZeRO` 优化，通过将训练过程中的参数、梯度和优化器状态切片保存，能够在多 GPU 训练时显著节省显存
    - 除了将训练中间状态切片外，`DeepSpeed` 训练时使用 FP16 的权重，相较于 `Pytorch` 的 `AMP` 训练，在单 GPU 上也能大幅节省显存

<center><img src="https://cdn.jujimeizuo.cn/note/llm/internlm/fa-dz.jpg"></center>

`DeepSpeed` 与 `Flash Attention` 虽然能够大幅降低训练成本，但使用门槛相对较高，需要复杂的配置，甚至修改代码，为了让开发者专注于数据，XTuner 会自动 `dispatch Flash Attention`，并一键启动 `DeepSpeed ZeRO`

```bash
xtuner train internlm_20b_qlora_oasst1_512_e3 \
    --deepspeed deepspeed_zero3
```

## 实战训练

### 环境 & 安装

- 环境：Ubuntu + Anaconda + CUDA/CUDNN + 8GB Nvidia GPU
- 安装：

```bash
conda create --name xtuner0.1.9 python=3.10 -y
conda activate xtuner0.1.9
cd ~ && mkdir xtuner019 && cd xtuner019
git clone -b v0.1.9  https://github.com/InternLM/xtuner
cd xtuner
pip install -e '.[all]'
```

- 创建数据集工作路径：

```bash
mkdir ~/ft-oasst1 && cd ~/ft-oasst1
```

### 微调

#### 准备配置文件

```bash
cd ~/ft-oasst1
xtuner copy-cfg internlm_chat_7b_qlora_oasst1_e3 .
```

#### 模型下载

- InternStudio 平台上

```bash
cp -r /root/share/temp/model_repos/internlm-chat-7b ~/ft-oasst1/
```
- 不用 xtuner 默认的从 huggingface 拉取模型，而是提前从 ModelScope 下载模型到本地

```bash
# 创建一个目录，放模型文件，防止散落一地
mkdir ~/ft-oasst1/internlm-chat-7b

# 装一下拉取模型文件要用的库
pip install modelscope

# 从 modelscope 下载下载模型文件
cd ~/ft-oasst1
apt install git git-lfs -y
git lfs install
git lfs clone https://modelscope.cn/Shanghai_AI_Laboratory/internlm-chat-7b.git -b v1.0.3
```
#### 数据集下载

> https://huggingface.co/datasets/timdettmers/openassistant-guanaco/tree/main


#### 修改配置文件

修改其中的模型和数据集为 本地路径

```bash
cd ~/ft-oasst1
vim internlm_chat_7b_qlora_oasst1_e3_copy.py
```

```diff
# 修改模型为本地路径
- pretrained_model_name_or_path = 'internlm/internlm-chat-7b'
+ pretrained_model_name_or_path = './internlm-chat-7b'

# 修改训练数据集为本地路径
- data_path = 'timdettmers/openassistant-guanaco'
+ data_path = './openassistant-guanaco'
```

#### 开始微调

```bash
# 单卡
## 用刚才改好的config文件训练
xtuner train ./internlm_chat_7b_qlora_oasst1_e3_copy.py

# 多卡
NPROC_PER_NODE=${GPU_NUM} xtuner train ./internlm_chat_7b_qlora_oasst1_e3_copy.py

# 若要开启 deepspeed 加速，增加 --deepspeed deepspeed_zero2 即可
```

> 微调得到的 PTH 模型文件和其他杂七杂八的文件都默认在当前的 `./work_dirs` 中。

#### 生成 Adapter 文件

> 将得到的 PTH 模型转换为 HuggingFace 模型，即：生成 Adapter 文件夹
> 可以简单理解：LoRA 模型文件 = Adapter

```bash
mkdir hf
export MKL_SERVICE_FORCE_INTEL=1

xtuner convert pth_to_hf ./internlm_chat_7b_qlora_oasst1_e3_copy.py ./work_dirs/internlm_chat_7b_qlora_oasst1_e3_copy/epoch_1.pth ./hf
```


### 部署与测试

#### 将 HuggingFace adapter 合并到大语言模型

```bash
xtuner convert merge ./internlm-chat-7b ./hf ./merged --max-shard-size 2GB
# xtuner convert merge \
#     ${NAME_OR_PATH_TO_LLM} \
#     ${NAME_OR_PATH_TO_ADAPTER} \
#     ${SAVE_PATH} \
#     --max-shard-size 2GB
```

####  与合并后的模型对话

```bash
# 加载 Adapter 模型对话（Float 16）
xtuner chat ./merged --prompt-template internlm_chat

# 4 bit 量化加载
# xtuner chat ./merged --bits 4 --prompt-template internlm_chat
```


| 微调前                                                                                 | 微调后                                                                                |
| -------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| <center><img src="https://cdn.jujimeizuo.cn/note/llm/internlm/ft-before.png"></center> | <center><img src="https://cdn.jujimeizuo.cn/note/llm/internlm/ft-after.png"></center> |

## 自定义微调

> 以 **[Medication QA](https://github.com/abachaa/Medication_QA_MedInfo2019)** **数据集**为例

### 概述

#### **场景需求**

   基于 InternLM-chat-7B 模型，用 MedQA 数据集进行微调，将其往`医学问答`领域对齐。

#### **真实数据预览**

| 问题                                                       | 答案                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| ---------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| What are ketorolac eye drops?（什么是酮咯酸滴眼液？）      | Ophthalmic   ketorolac is used to treat itchy eyes caused by allergies. It also is used to   treat swelling and redness (inflammation) that can occur after cataract   surgery. Ketorolac is in a class of medications called nonsteroidal   anti-inflammatory drugs (NSAIDs). It works by stopping the release of   substances that cause allergy symptoms and inflammation.                                                                                                                                                                                                                                                                                                                                                           |
| What medicines raise blood sugar? （什么药物会升高血糖？） | Some   medicines for conditions other than diabetes can raise your blood sugar   level. This is a concern when you have diabetes. Make sure every doctor you   see knows about all of the medicines, vitamins, or herbal supplements you   take. This means anything you take with or without a prescription. Examples include:     Barbiturates.     Thiazide diuretics.     Corticosteroids.     Birth control pills (oral contraceptives) and progesterone.     Catecholamines.     Decongestants that contain beta-adrenergic agents, such as pseudoephedrine.     The B vitamin niacin. The risk of high blood sugar from niacin lowers after you have taken it for a few months. The antipsychotic medicine olanzapine (Zyprexa). |

### 数据准备 

> **以** **[Medication QA](https://github.com/abachaa/Medication_QA_MedInfo2019)** **数据集为例**

**原格式：(.xlsx)**

| **问题** | 药物类型 | 问题类型 | **回答** | 主题 | URL |
| -------- | -------- | -------- | -------- | ---- | --- |
| aaa      | bbb      | ccc      | ddd      | eee  | fff |

#### 将数据转为 XTuner 的数据格式

**目标格式：(.jsonL)**

```JSON
[{
    "conversation":[
        {
            "system": "xxx",
            "input": "xxx",
            "output": "xxx"
        }
    ]
},
{
    "conversation":[
        {
            "system": "xxx",
            "input": "xxx",
            "output": "xxx"
        }
    ]
}]
```

🧠通过 python脚本：将 `.xlsx` 中的 问题 和 回答 两列 提取出来，再放入 `.jsonL` 文件的每个 conversation 的 input 和 output 中。

> 这一步的 python 脚本可以请 ChatGPT 来完成。

```text
Write a python file for me. using openpyxl. input file name is MedQA2019.xlsx
Step1: The input file is .xlsx. Exact the column A and column D in the sheet named "DrugQA" .
Step2: Put each value in column A into each "input" of each "conversation". Put each value in column D into each "output" of each "conversation".
Step3: The output file is .jsonL. It looks like:
[{
    "conversation":[
        {
            "system": "xxx",
            "input": "xxx",
            "output": "xxx"
        }
    ]
},
{
    "conversation":[
        {
            "system": "xxx",
            "input": "xxx",
            "output": "xxx"
        }
    ]
}]
Step4: All "system" value changes to "You are a professional, highly experienced doctor professor. You always provide accurate, comprehensive, and detailed answers based on the patients' questions."
```

> ChatGPT 生成的 python 代码如下：

??? note "xlsx2jsonl.py"
    ```python
    import openpyxl
    import json

    def process_excel_to_json(input_file, output_file):
        # Load the workbook
        wb = openpyxl.load_workbook(input_file)

        # Select the "DrugQA" sheet
        sheet = wb["DrugQA"]

        # Initialize the output data structure
        output_data = []

        # Iterate through each row in column A and D
        for row in sheet.iter_rows(min_row=2, max_col=4, values_only=True):
            system_value = "You are a professional, highly experienced doctor professor. You always provide accurate, comprehensive, and detailed answers based on the patients' questions."

            # Create the conversation dictionary
            conversation = {
                "system": system_value,
                "input": row[0],
                "output": row[3]
            }

            # Append the conversation to the output data
            output_data.append({"conversation": [conversation]})

        # Write the output data to a JSON file
        with open(output_file, 'w', encoding='utf-8') as json_file:
            json.dump(output_data, json_file, indent=4)

        print(f"Conversion complete. Output written to {output_file}")

    # Replace 'MedQA2019.xlsx' and 'output.jsonl' with your actual input and output file names
    process_excel_to_json('MedQA2019.xlsx', 'output.jsonl')
    ```

执行 python 脚本，获得格式化后的数据集：
```bash
python xlsx2jsonl.py
```

**格式化后的数据集长这样：**

<center><img src="https://cdn.jujimeizuo.cn/note/llm/internlm/data-processed.png"></center>

此时，当然也可以对数据进行训练集和测试集的分割，同样可以让 ChatGPT 写 python 代码。当然如果你没有严格的科研需求、不在乎“训练集泄露”的问题，也可以不做训练集与测试集的分割。

#### 划分训练集和测试集

```text
my .jsonL file looks like:
[{
    "conversation":[
        {
            "system": "xxx",
            "input": "xxx",
            "output": "xxx"
        }
    ]
},
{
    "conversation":[
        {
            "system": "xxx",
            "input": "xxx",
            "output": "xxx"
        }
    ]
}]
Step1, read the .jsonL file.
Step2, count the amount of the "conversation" elements.
Step3, randomly split all "conversation" elements by 7:3. Targeted structure is same as the input.
Step4, save the 7/10 part as train.jsonl. save the 3/10 part as test.jsonl
```

> 生成的 python 代码如下：

??? note "split2train_and_test.py"
    ```python
    import json
    import random

    def split_conversations(input_file, train_output_file, test_output_file):
        # Read the input JSONL file
        with open(input_file, 'r', encoding='utf-8') as jsonl_file:
            data = json.load(jsonl_file)

        # Count the number of conversation elements
        num_conversations = len(data)
        
        # Shuffle the data randomly
        random.shuffle(data)
        random.shuffle(data)
        random.shuffle(data)

        # Calculate the split points for train and test
        split_point = int(num_conversations * 0.7)

        # Split the data into train and test
        train_data = data[:split_point]
        test_data = data[split_point:]

        # Write the train data to a new JSONL file
        with open(train_output_file, 'w', encoding='utf-8') as train_jsonl_file:
            json.dump(train_data, train_jsonl_file, indent=4)

        # Write the test data to a new JSONL file
        with open(test_output_file, 'w', encoding='utf-8') as test_jsonl_file:
            json.dump(test_data, test_jsonl_file, indent=4)

        print(f"Split complete. Train data written to {train_output_file}, Test data written to {test_output_file}")

    # Replace 'input.jsonl', 'train.jsonl', and 'test.jsonl' with your actual file names
    split_conversations('MedQA2019-structured.jsonl', 'MedQA2019-structured-train.jsonl', 'MedQA2019-structured-test.jsonl')
    ```


### 开始自定义微调

此时，我们重新建一个文件夹来玩“微调自定义数据集”
```bash
mkdir ~/ft-medqa && cd ~/ft-medqa
```

把前面下载好的internlm-chat-7b模型文件夹拷贝过来。

```bash
cp -r ~/ft-oasst1/internlm-chat-7b .
```
别忘了把自定义数据集，即几个 `.jsonL`，也传到服务器上。

```bash
git clone https://github.com/InternLM/tutorial
```

```bash
cp ~/tutorial/xtuner/MedQA2019-structured-train.jsonl .
```



#### 准备配置文件
```bash
# 复制配置文件到当前目录
xtuner copy-cfg internlm_chat_7b_qlora_oasst1_e3 .
# 改个文件名
mv internlm_chat_7b_qlora_oasst1_e3_copy.py internlm_chat_7b_qlora_medqa2019_e3.py

# 修改配置文件内容
vim internlm_chat_7b_qlora_medqa2019_e3.py
```

减号代表要删除的行，加号代表要增加的行。
```diff
# 修改import部分
- from xtuner.dataset.map_fns import oasst1_map_fn, template_map_fn_factory
+ from xtuner.dataset.map_fns import template_map_fn_factory

# 修改模型为本地路径
- pretrained_model_name_or_path = 'internlm/internlm-chat-7b'
+ pretrained_model_name_or_path = './internlm-chat-7b'

# 修改训练数据为 MedQA2019-structured-train.jsonl 路径
- data_path = 'timdettmers/openassistant-guanaco'
+ data_path = 'MedQA2019-structured-train.jsonl'

# 修改 train_dataset 对象
train_dataset = dict(
    type=process_hf_dataset,
-   dataset=dict(type=load_dataset, path=data_path),
+   dataset=dict(type=load_dataset, path='json', data_files=dict(train=data_path)),
    tokenizer=tokenizer,
    max_length=max_length,
-   dataset_map_fn=alpaca_map_fn,
+   dataset_map_fn=None,
    template_map_fn=dict(
        type=template_map_fn_factory, template=prompt_template),
    remove_unused_columns=True,
    shuffle_before_pack=True,
    pack_to_max_length=pack_to_max_length)
```
#### XTuner！启动！

```bash
xtuner train internlm_chat_7b_qlora_medqa2019_e3.py --deepspeed deepspeed_zero2
```

#### 生成 Adapter 文件

#### 部署与测试


## 用 MS-Agent 数据集赋予 LLM 以 Agent 能力

### 概述

MSAgent 数据集每条样本包含一个对话列表（conversations），其里面包含了 system、user、assistant 三种字段。其中：

- system: 表示给模型前置的人设输入，其中有告诉模型如何调用插件以及生成请求

- user: 表示用户的输入 prompt，分为两种，通用生成的prompt和调用插件需求的 prompt

- assistant: 为模型的回复。其中会包括插件调用代码和执行代码，调用代码是要 LLM 生成的，而执行代码是调用服务来生成结果的

一条调用网页搜索插件查询“上海明天天气”的数据样本示例如下图所示：

<center><img src="https://cdn.jujimeizuo.cn/note/llm/internlm/msagent_data.png"></center>


### 微调步骤

#### 准备工作
> xtuner 是从国内的 ModelScope 平台下载 MS-Agent 数据集，因此不用提前手动下载数据集文件。

```bash
# 准备工作
mkdir ~/ft-msagent && cd ~/ft-msagent
cp -r ~/ft-oasst1/internlm-chat-7b .

# 查看配置文件
xtuner list-cfg | grep msagent

# 复制配置文件到当前目录
xtuner copy-cfg internlm_7b_qlora_msagent_react_e3_gpu8 .

# 修改配置文件中的模型为本地路径
vim ./internlm_7b_qlora_msagent_react_e3_gpu8_copy.py 
```

```diff
- pretrained_model_name_or_path = 'internlm/internlm-chat-7b'
+ pretrained_model_name_or_path = './internlm-chat-7b'
```

#### 开始微调
```Bash
xtuner train ./internlm_7b_qlora_msagent_react_e3_gpu8_copy.py --deepspeed deepspeed_zero2
```

### 直接使用

> 由于 msagent 的训练非常费时，大家如果想尽快把这个教程跟完，可以直接从 modelScope 拉取咱们已经微调好了的 Adapter。如下演示。

#### 下载 Adapter
```Bash
cd ~/ft-msagent
apt install git git-lfs
git lfs install
git lfs clone https://www.modelscope.cn/xtuner/internlm-7b-qlora-msagent-react.git
```

有了这个在 msagent 上训练得到的Adapter，模型现在已经有 agent 能力了！就可以加 --lagent 以调用来自 lagent 的代理功能了！

#### 添加 serper 环境变量

> **开始 chat 之前，还要加个 serper 的环境变量：**
> 
> 去 serper.dev 免费注册一个账号，生成自己的 api key。这个东西是用来给 lagent 去获取 google 搜索的结果的。等于是 serper.dev 帮你去访问 google，而不是从你自己本地去访问 google 了。

添加 serper api key 到环境变量：

```bash
export SERPER_API_KEY=abcdefg
```

#### xtuner + agent，启动！

```bash
xtuner chat ./internlm-chat-7b --adapter internlm-7b-qlora-msagent-react --lagent --prompt-template internlm_chat
```


## 作业：XTuner InternLM-Chat 个人小助手认知微调实践

### 环境准备

```bash
# InternStudio 平台中，从本地 clone 一个已有 pytorch 2.0.1 的环境（后续均在该环境执行，若为其他环境可作为参考）
# 进入环境后首先 bash
# 进入环境后首先 bash
# 进入环境后首先 bash
bash
conda create --name personal_assistant --clone=/root/share/conda_envs/internlm-base
# 如果在其他平台：
# conda create --name personal_assistant python=3.10 -y

# 激活环境
conda activate personal_assistant
# 进入家目录 （~的意思是 “当前用户的home路径”）
cd ~
# 创建版本文件夹并进入，以跟随本教程
# personal_assistant用于存放本教程所使用的东西
mkdir /root/personal_assistant && cd /root/personal_assistant
mkdir /root/personal_assistant/xtuner019 && cd /root/personal_assistant/xtuner019

# 拉取 0.1.9 的版本源码
git clone -b v0.1.9  https://github.com/InternLM/xtuner
# 无法访问github的用户请从 gitee 拉取:
# git clone -b v0.1.9 https://gitee.com/Internlm/xtuner

# 进入源码目录
cd xtuner

# 从源码安装 XTuner
pip install -e '.[all]'
```

### 数据准备

```bash
mkdir -p /root/personal_assistant/data && cd /root/personal_assistant/data
```

在 `data` 目录下创建一个json文件 `personal_assistant.json` 作为本次微调所使用的数据集。

其中 `conversation` 表示一次对话的内容，`input` 为输入，即用户会问的问题，`output` 为输出，即想要模型回答的答案。

以下是一个python脚本，用于生成数据集。

??? note "generate_data.py"
    ```python
    import json

    # 输入你的名字
    name = '狙击美佐'
    # 重复次数
    n = 10000

    data = [
        {
            "conversation": [
                {
                    "input": "请做一下自我介绍",
                    "output": "我是{}的小助手，内在是上海AI实验室书生·浦语的7B大模型哦".format(name)
                }
            ]
        }
    ]

    for i in range(n):
        data.append(data[0])

    with open('personal_assistant.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    ```

### 配置准备

```bash
mkdir -p /root/personal_assistant/model/Shanghai_AI_Laboratory
cp -r /root/share/temp/model_repos/internlm-chat-7b /root/personal_assistant/model/Shanghai_AI_Laboratory
```

```bash
# 创建用于存放配置的文件夹config并进入
mkdir /root/personal_assistant/config && cd /root/personal_assistant/config
# 拷贝一个配置文件到当前目录
xtuner copy-cfg internlm_chat_7b_qlora_oasst1_e3 .
```
修改拷贝后的文件：

??? note "internlm_chat_7b_qlora_oasst1_e3_copy.py"
    ```python
    # Copyright (c) OpenMMLab. All rights reserved.
    import torch
    from bitsandbytes.optim import PagedAdamW32bit
    from datasets import load_dataset
    from mmengine.dataset import DefaultSampler
    from mmengine.hooks import (CheckpointHook, DistSamplerSeedHook, IterTimerHook,
                                LoggerHook, ParamSchedulerHook)
    from mmengine.optim import AmpOptimWrapper, CosineAnnealingLR
    from peft import LoraConfig
    from transformers import (AutoModelForCausalLM, AutoTokenizer,
                            BitsAndBytesConfig)

    from xtuner.dataset import process_hf_dataset
    from xtuner.dataset.collate_fns import default_collate_fn
    from xtuner.dataset.map_fns import oasst1_map_fn, template_map_fn_factory
    from xtuner.engine import DatasetInfoHook, EvaluateChatHook
    from xtuner.model import SupervisedFinetune
    from xtuner.utils import PROMPT_TEMPLATE

    #######################################################################
    #                          PART 1  Settings                           #
    #######################################################################
    # Model
    pretrained_model_name_or_path = '/root/personal_assistant/model/Shanghai_AI_Laboratory/internlm-chat-7b'

    # Data
    data_path = '/root/personal_assistant/data/personal_assistant.json'
    prompt_template = PROMPT_TEMPLATE.internlm_chat
    max_length = 512
    pack_to_max_length = True

    # Scheduler & Optimizer
    batch_size = 2  # per_device
    accumulative_counts = 16
    dataloader_num_workers = 0
    max_epochs = 3
    optim_type = PagedAdamW32bit
    lr = 2e-4
    betas = (0.9, 0.999)
    weight_decay = 0
    max_norm = 1  # grad clip

    # Evaluate the generation performance during the training
    evaluation_freq = 90
    SYSTEM = ''
    evaluation_inputs = [ '请介绍一下你自己', '请做一下自我介绍' ]

    #######################################################################
    #                      PART 2  Model & Tokenizer                      #
    #######################################################################
    tokenizer = dict(
        type=AutoTokenizer.from_pretrained,
        pretrained_model_name_or_path=pretrained_model_name_or_path,
        trust_remote_code=True,
        padding_side='right')

    model = dict(
        type=SupervisedFinetune,
        llm=dict(
            type=AutoModelForCausalLM.from_pretrained,
            pretrained_model_name_or_path=pretrained_model_name_or_path,
            trust_remote_code=True,
            torch_dtype=torch.float16,
            quantization_config=dict(
                type=BitsAndBytesConfig,
                load_in_4bit=True,
                load_in_8bit=False,
                llm_int8_threshold=6.0,
                llm_int8_has_fp16_weight=False,
                bnb_4bit_compute_dtype=torch.float16,
                bnb_4bit_use_double_quant=True,
                bnb_4bit_quant_type='nf4')),
        lora=dict(
            type=LoraConfig,
            r=64,
            lora_alpha=16,
            lora_dropout=0.1,
            bias='none',
            task_type='CAUSAL_LM'))

    #######################################################################
    #                      PART 3  Dataset & Dataloader                   #
    #######################################################################
    train_dataset = dict(
        type=process_hf_dataset,
        dataset=dict(type=load_dataset, path='json', data_files=dict(train=data_path)),
        tokenizer=tokenizer,
        max_length=max_length,
        dataset_map_fn=None,
        template_map_fn=dict(
            type=template_map_fn_factory, template=prompt_template),
        remove_unused_columns=True,
        shuffle_before_pack=True,
        pack_to_max_length=pack_to_max_length)

    train_dataloader = dict(
        batch_size=batch_size,
        num_workers=dataloader_num_workers,
        dataset=train_dataset,
        sampler=dict(type=DefaultSampler, shuffle=True),
        collate_fn=dict(type=default_collate_fn))

    #######################################################################
    #                    PART 4  Scheduler & Optimizer                    #
    #######################################################################
    # optimizer
    optim_wrapper = dict(
        type=AmpOptimWrapper,
        optimizer=dict(
            type=optim_type, lr=lr, betas=betas, weight_decay=weight_decay),
        clip_grad=dict(max_norm=max_norm, error_if_nonfinite=False),
        accumulative_counts=accumulative_counts,
        loss_scale='dynamic',
        dtype='float16')

    # learning policy
    # More information: https://github.com/open-mmlab/mmengine/blob/main/docs/en/tutorials/param_scheduler.md  # noqa: E501
    param_scheduler = dict(
        type=CosineAnnealingLR,
        eta_min=0.0,
        by_epoch=True,
        T_max=max_epochs,
        convert_to_iter_based=True)

    # train, val, test setting
    train_cfg = dict(by_epoch=True, max_epochs=max_epochs, val_interval=1)

    #######################################################################
    #                           PART 5  Runtime                           #
    #######################################################################
    # Log the dialogue periodically during the training process, optional
    custom_hooks = [
        dict(type=DatasetInfoHook, tokenizer=tokenizer),
        dict(
            type=EvaluateChatHook,
            tokenizer=tokenizer,
            every_n_iters=evaluation_freq,
            evaluation_inputs=evaluation_inputs,
            system=SYSTEM,
            prompt_template=prompt_template)
    ]

    # configure default hooks
    default_hooks = dict(
        # record the time of every iteration.
        timer=dict(type=IterTimerHook),
        # print log every 100 iterations.
        logger=dict(type=LoggerHook, interval=10),
        # enable the parameter scheduler.
        param_scheduler=dict(type=ParamSchedulerHook),
        # save checkpoint per epoch.
        checkpoint=dict(type=CheckpointHook, interval=1),
        # set sampler seed in distributed evrionment.
        sampler_seed=dict(type=DistSamplerSeedHook),
    )

    # configure environment
    env_cfg = dict(
        # whether to enable cudnn benchmark
        cudnn_benchmark=False,
        # set multi process parameters
        mp_cfg=dict(mp_start_method='fork', opencv_num_threads=0),
        # set distributed parameters
        dist_cfg=dict(backend='nccl'),
    )

    # set visualizer
    visualizer = None

    # set log level
    log_level = 'INFO'

    # load from which checkpoint
    load_from = None

    # whether to resume training from the loaded checkpoint
    resume = False

    # Defaults to use random seed and disable `deterministic`
    randomness = dict(seed=None, deterministic=False)
    ```

### 微调

```bash
xtuner train /root/personal_assistant/config/internlm_chat_7b_qlora_oasst1_e3_copy.py
```

### 参数转换/合并

- 训练后的pth格式参数转Hugging Face格式

```bash
# 创建用于存放Hugging Face格式参数的hf文件夹
mkdir /root/personal_assistant/config/work_dirs/hf

export MKL_SERVICE_FORCE_INTEL=1

# 配置文件存放的位置
export CONFIG_NAME_OR_PATH=/root/personal_assistant/config/internlm_chat_7b_qlora_oasst1_e3_copy.py

# 模型训练后得到的pth格式参数存放的位置
export PTH=/root/personal_assistant/config/work_dirs/internlm_chat_7b_qlora_oasst1_e3_copy/epoch_3.pth

# pth文件转换为Hugging Face格式后参数存放的位置
export SAVE_PATH=/root/personal_assistant/config/work_dirs/hf

# 执行参数转换
xtuner convert pth_to_hf $CONFIG_NAME_OR_PATH $PTH $SAVE_PATH
```

- Merge模型参数

```bash
export MKL_SERVICE_FORCE_INTEL=1
export MKL_THREADING_LAYER='GNU'

# 原始模型参数存放的位置
export NAME_OR_PATH_TO_LLM=/root/personal_assistant/model/Shanghai_AI_Laboratory/internlm-chat-7b

# Hugging Face格式参数存放的位置
export NAME_OR_PATH_TO_ADAPTER=/root/personal_assistant/config/work_dirs/hf

# 最终Merge后的参数存放的位置
mkdir /root/personal_assistant/config/work_dirs/hf_merge
export SAVE_PATH=/root/personal_assistant/config/work_dirs/hf_merge

# 执行参数Merge
xtuner convert merge \
    $NAME_OR_PATH_TO_LLM \
    $NAME_OR_PATH_TO_ADAPTER \
    $SAVE_PATH \
    --max-shard-size 2GB
```

### Demo

- 安装依赖

```bash
pip install streamlit==1.24.0
```

- 下载InternLM项目代码

```bash
# 创建code文件夹用于存放InternLM项目代码
mkdir /root/personal_assistant/code && cd /root/personal_assistant/code
git clone https://github.com/InternLM/InternLM.git
```

- 将 `/root/code/InternLM/web_demo.py` 中 29 行 和 33 行的模型路径更换为Merge后存放参数的路径 `/root/personal_assistant/config/work_dirs/hf_merge`

- 运行 `/root/personal_assistant/code/InternLM` 目录下的 `web_demo.py` 文件，将端口映射到本地

```bash
streamlit run /root/personal_assistant/code/InternLM/web_demo.py --server.address 127.0.0.1 --server.port 6006
```

### 效果

- **微调前**（回答比较官方）

<center><img src="https://cdn.jujimeizuo.cn/note/llm/internlm/hw_4_1.jpg"></center>

- **微调后**（对自己的身份有了清晰的认知）

<center><img src="https://cdn.jujimeizuo.cn/note/llm/internlm/hw_4_2.jpg"></center>

## 进阶作业

- 将训练好的Adapter模型权重上传到 OpenXLab、Hugging Face 或者 MoelScope 任一一平台。

    1. 通过 scp 将 hf 文件夹下载到本地，进入 HuggingFace 新建 model，上传模型文件。Adapter 权重地址：https://huggingface.co/jujimeizuo/assistant-jujimeizuo/tree/main

    <center><img src="https://cdn.jujimeizuo.cn/note/llm/internlm/hw_4_3.jpg"></center>


- 将训练好后的模型应用部署到 OpenXLab 平台，参考部署文档请访问：https://aicarrier.feishu.cn/docx/MQH6dygcKolG37x0ekcc4oZhnCe

    1. 通过 openxlab 库上传模型文件

    <center><img src="https://cdn.jujimeizuo.cn/note/llm/internlm/hw_4_4.jpg"></center>

    2. 新建 github 的 repo([assistant_jujimeizuo](https://github.com/jujimeizuo/assistant_jujimeizuo))，从 OpenXLab 上拉取上传的模型，构建 streamlit 的 app，同步到 OpenXLab 上。

    3. 应用服务地址：https://openxlab.org.cn/apps/detail/jujimeizuo/assistant_jujimeizuo

    <center><img src="https://cdn.jujimeizuo.cn/note/llm/internlm/hw_4_5.jpg"></center>
