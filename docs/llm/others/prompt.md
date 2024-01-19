---
counter: true
comment: true
---

# Prompt

!!! abstract
    Learn from [**ChatGPT Prompt Engineering for Developers**](https://www.deeplearning.ai/short-courses/chatgpt-prompt-engineering-for-developers/) in  [**DeepLearning.AI**](https://learn.deeplearning.ai/)


## Guidelines for Prompting

- **Principle 1: Write clear and specific instructions**
    - **Tactic 1: Use delimiters to clearly indicate disinct parts of the input**
        - Delimiters can be anything like: \`\`\`,""",<>,`<tag>`,`</tag>`,`:`
    - **Tactic 2: Ask for a structureed output**
        - JSON, HTML
    - **Tactic 3: Ask the modell to check whether conditions are satisfied**
    - **Tactic 4: "Few-shot" prompting**
- **Principle 2: Give the model time to "think"**
    - **Tactic 1: Specify the steps required to complete a task, Ask for output in a specified format**
    - **Tactic 2: Instruct the model to work out its own solution before rushing to a conclusion**


## Setup

Load the API key and relevant Python libaries.

```python
import openai
import os

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

openai.api_key  = os.getenv('OPENAI_API_KEY')
```

using `helper function`, model is `gpt-3.5-turbo`.

```python
def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]
```

## Example

- simple

```python
text = f"""
You should express what you want a model to do by \ 
providing instructions that are as clear and \ 
specific as you can possibly make them. \ 
This will guide the model towards the desired output, \ 
and reduce the chances of receiving irrelevant \ 
or incorrect responses. Don't confuse writing a \ 
clear prompt with writing a short prompt. \ 
In many cases, longer prompts provide more clarity \ 
and context for the model, which can lead to \ 
more detailed and relevant outputs.
"""

prompt = f"""
Summarize the text delimited by triple backticks \ 
into a single sentence.
```{text}```
"""

response = get_completion(prompt)
print(response)
```

- chatbot

```python
def get_completion(prompt, model="gpt-3.5-turbo"): # Andrew mentioned that the prompt/ completion paradigm is preferable for this class
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]
```

```python
prod_review = """
Got this panda plush toy for my daughter's birthday, \
who loves it and takes it everywhere. It's soft and \ 
super cute, and its face has a friendly look. It's \ 
a bit small for what I paid though. I think there \ 
might be other options that are bigger for the \ 
same price. It arrived a day earlier than expected, \ 
so I got to play with it myself before I gave it \ 
to her.
"""

prompt = f"""
Your task is to generate a short summary of a product \
review from an ecommerce site. 

Summarize the review below, delimited by triple 
backticks, in at most 30 words. 

Review: ```{prod_review}```
"""

response = get_completion(prompt)
print(response)
```


## Prompting for Tasks

- [Iterative](https://learn.deeplearning.ai/chatgpt-prompt-eng/lesson/3/iterative)
- [Summarizing](https://learn.deeplearning.ai/chatgpt-prompt-eng/lesson/4/summarizing)
- [Inferring](https://learn.deeplearning.ai/chatgpt-prompt-eng/lesson/5/inferring)
- [Transforming](https://learn.deeplearning.ai/chatgpt-prompt-eng/lesson/6/transforming)
- [Expanding](https://learn.deeplearning.ai/chatgpt-prompt-eng/lesson/7/expanding)
- [Chatbot](https://learn.deeplearning.ai/chatgpt-prompt-eng/lesson/8/chatbot)