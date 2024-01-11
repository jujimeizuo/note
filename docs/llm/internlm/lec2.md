---
counter: true
comment: true
---

# 轻松分钟玩转书生·浦语大模型趣味 Demo

!!! abstract
    学习自 [轻松分钟玩转书生·浦语大模型趣味 Demo](https://github.com/InternLM/tutorial/blob/main/helloworld/hello_world.md)

## InternLM-Chat-7B 智能对话

### Terminal Demo

??? note "cli_demo.py"
    ```python
    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM


    model_name_or_path = "/root/model/Shanghai_AI_Laboratory/internlm-chat-7b"

    tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(model_name_or_path, trust_remote_code=True, torch_dtype=torch.bfloat16, device_map='auto')
    model = model.eval()

    system_prompt = """You are an AI assistant whose name is InternLM (书生·浦语).
    - InternLM (书生·浦语) is a conversational language model that is developed by Shanghai AI Laboratory (上海人工智能实验室). It is designed to be helpful, honest, and harmless.
    - InternLM (书生·浦语) can understand and communicate fluently in the language chosen by the user such as English and 中文.
    """

    messages = [(system_prompt, '')]

    print("=============Welcome to InternLM chatbot, type 'exit' to exit.=============")

    while True:
        input_text = input("User  >>> ")
        input_text.replace(' ', '')
        if input_text == "exit":
            break
        response, history = model.chat(tokenizer, input_text, history=messages)
        messages.append((input_text, response))
        print(f"robot >>> {response}")
    ```

```bash
python /root/code/InternLM/cli_demo.py
```

<center><img src="https://cdn.jujimeizuo.cn/note/llm/internlm/terminal_demo.jpg"></center>

### Web Demo

```bash
streamlit run /root/code/InternLM/web_demo.py --server.address 127.0.0.1 --server.port 6006
```

<center><img src="https://cdn.jujimeizuo.cn/note/llm/internlm/web_demo.jpg"></center>

## Lagent 智能体工具调用

??? note "react_web_demo.py"
    ```python
    import copy
    import os

    import streamlit as st
    from streamlit.logger import get_logger

    from lagent.actions import ActionExecutor, GoogleSearch, PythonInterpreter
    from lagent.agents.react import ReAct
    from lagent.llms import GPTAPI
    from lagent.llms.huggingface import HFTransformerCasualLM


    class SessionState:

        def init_state(self):
            """Initialize session state variables."""
            st.session_state['assistant'] = []
            st.session_state['user'] = []

            #action_list = [PythonInterpreter(), GoogleSearch()]
            action_list = [PythonInterpreter()]
            st.session_state['plugin_map'] = {
                action.name: action
                for action in action_list
            }
            st.session_state['model_map'] = {}
            st.session_state['model_selected'] = None
            st.session_state['plugin_actions'] = set()

        def clear_state(self):
            """Clear the existing session state."""
            st.session_state['assistant'] = []
            st.session_state['user'] = []
            st.session_state['model_selected'] = None
            if 'chatbot' in st.session_state:
                st.session_state['chatbot']._session_history = []


    class StreamlitUI:

        def __init__(self, session_state: SessionState):
            self.init_streamlit()
            self.session_state = session_state

        def init_streamlit(self):
            """Initialize Streamlit's UI settings."""
            st.set_page_config(
                layout='wide',
                page_title='lagent-web',
                page_icon='./docs/imgs/lagent_icon.png')
            # st.header(':robot_face: :blue[Lagent] Web Demo ', divider='rainbow')
            st.sidebar.title('模型控制')

        def setup_sidebar(self):
            """Setup the sidebar for model and plugin selection."""
            model_name = st.sidebar.selectbox(
                '模型选择：', options=['gpt-3.5-turbo','internlm'])
            if model_name != st.session_state['model_selected']:
                model = self.init_model(model_name)
                self.session_state.clear_state()
                st.session_state['model_selected'] = model_name
                if 'chatbot' in st.session_state:
                    del st.session_state['chatbot']
            else:
                model = st.session_state['model_map'][model_name]

            plugin_name = st.sidebar.multiselect(
                '插件选择',
                options=list(st.session_state['plugin_map'].keys()),
                default=[list(st.session_state['plugin_map'].keys())[0]],
            )

            plugin_action = [
                st.session_state['plugin_map'][name] for name in plugin_name
            ]
            if 'chatbot' in st.session_state:
                st.session_state['chatbot']._action_executor = ActionExecutor(
                    actions=plugin_action)
            if st.sidebar.button('清空对话', key='clear'):
                self.session_state.clear_state()
            uploaded_file = st.sidebar.file_uploader(
                '上传文件', type=['png', 'jpg', 'jpeg', 'mp4', 'mp3', 'wav'])
            return model_name, model, plugin_action, uploaded_file

        def init_model(self, option):
            """Initialize the model based on the selected option."""
            if option not in st.session_state['model_map']:
                if option.startswith('gpt'):
                    st.session_state['model_map'][option] = GPTAPI(
                        model_type=option)
                else:
                    st.session_state['model_map'][option] = HFTransformerCasualLM(
                        '/root/model/Shanghai_AI_Laboratory/internlm-chat-7b')
            return st.session_state['model_map'][option]

        def initialize_chatbot(self, model, plugin_action):
            """Initialize the chatbot with the given model and plugin actions."""
            return ReAct(
                llm=model, action_executor=ActionExecutor(actions=plugin_action))

        def render_user(self, prompt: str):
            with st.chat_message('user'):
                st.markdown(prompt)

        def render_assistant(self, agent_return):
            with st.chat_message('assistant'):
                for action in agent_return.actions:
                    if (action):
                        self.render_action(action)
                st.markdown(agent_return.response)

        def render_action(self, action):
            with st.expander(action.type, expanded=True):
                st.markdown(
                    "<p style='text-align: left;display:flex;'> <span style='font-size:14px;font-weight:600;width:70px;text-align-last: justify;'>插    件</span><span style='width:14px;text-align:left;display:block;'>:</span><span style='flex:1;'>"  # noqa E501
                    + action.type + '</span></p>',
                    unsafe_allow_html=True)
                st.markdown(
                    "<p style='text-align: left;display:flex;'> <span style='font-size:14px;font-weight:600;width:70px;text-align-last: justify;'>思考步骤</span><span style='width:14px;text-align:left;display:block;'>:</span><span style='flex:1;'>"  # noqa E501
                    + action.thought + '</span></p>',
                    unsafe_allow_html=True)
                if (isinstance(action.args, dict) and 'text' in action.args):
                    st.markdown(
                        "<p style='text-align: left;display:flex;'><span style='font-size:14px;font-weight:600;width:70px;text-align-last: justify;'> 执行内容</span><span style='width:14px;text-align:left;display:block;'>:</span></p>",  # noqa E501
                        unsafe_allow_html=True)
                    st.markdown(action.args['text'])
                self.render_action_results(action)

        def render_action_results(self, action):
            """Render the results of action, including text, images, videos, and
            audios."""
            if (isinstance(action.result, dict)):
                st.markdown(
                    "<p style='text-align: left;display:flex;'><span style='font-size:14px;font-weight:600;width:70px;text-align-last: justify;'> 执行结果</span><span style='width:14px;text-align:left;display:block;'>:</span></p>",  # noqa E501
                    unsafe_allow_html=True)
                if 'text' in action.result:
                    st.markdown(
                        "<p style='text-align: left;'>" + action.result['text'] +
                        '</p>',
                        unsafe_allow_html=True)
                if 'image' in action.result:
                    image_path = action.result['image']
                    image_data = open(image_path, 'rb').read()
                    st.image(image_data, caption='Generated Image')
                if 'video' in action.result:
                    video_data = action.result['video']
                    video_data = open(video_data, 'rb').read()
                    st.video(video_data)
                if 'audio' in action.result:
                    audio_data = action.result['audio']
                    audio_data = open(audio_data, 'rb').read()
                    st.audio(audio_data)


    def main():
        logger = get_logger(__name__)
        # Initialize Streamlit UI and setup sidebar
        if 'ui' not in st.session_state:
            session_state = SessionState()
            session_state.init_state()
            st.session_state['ui'] = StreamlitUI(session_state)

        else:
            st.set_page_config(
                layout='wide',
                page_title='lagent-web',
                page_icon='./docs/imgs/lagent_icon.png')
            # st.header(':robot_face: :blue[Lagent] Web Demo ', divider='rainbow')
        model_name, model, plugin_action, uploaded_file = st.session_state[
            'ui'].setup_sidebar()

        # Initialize chatbot if it is not already initialized
        # or if the model has changed
        if 'chatbot' not in st.session_state or model != st.session_state[
                'chatbot']._llm:
            st.session_state['chatbot'] = st.session_state[
                'ui'].initialize_chatbot(model, plugin_action)

        for prompt, agent_return in zip(st.session_state['user'],
                                        st.session_state['assistant']):
            st.session_state['ui'].render_user(prompt)
            st.session_state['ui'].render_assistant(agent_return)
        # User input form at the bottom (this part will be at the bottom)
        # with st.form(key='my_form', clear_on_submit=True):

        if user_input := st.chat_input(''):
            st.session_state['ui'].render_user(user_input)
            st.session_state['user'].append(user_input)
            # Add file uploader to sidebar
            if uploaded_file:
                file_bytes = uploaded_file.read()
                file_type = uploaded_file.type
                if 'image' in file_type:
                    st.image(file_bytes, caption='Uploaded Image')
                elif 'video' in file_type:
                    st.video(file_bytes, caption='Uploaded Video')
                elif 'audio' in file_type:
                    st.audio(file_bytes, caption='Uploaded Audio')
                # Save the file to a temporary location and get the path
                file_path = os.path.join(root_dir, uploaded_file.name)
                with open(file_path, 'wb') as tmpfile:
                    tmpfile.write(file_bytes)
                st.write(f'File saved at: {file_path}')
                user_input = '我上传了一个图像，路径为: {file_path}. {user_input}'.format(
                    file_path=file_path, user_input=user_input)
            agent_return = st.session_state['chatbot'].chat(user_input)
            st.session_state['assistant'].append(copy.deepcopy(agent_return))
            logger.info(agent_return.inner_steps)
            st.session_state['ui'].render_assistant(agent_return)


    if __name__ == '__main__':
        root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        root_dir = os.path.join(root_dir, 'tmp_dir')
        os.makedirs(root_dir, exist_ok=True)
        main()
    ```

```bash
streamlit run /root/code/lagent/examples/react_web_demo.py --server.address 127.0.0.1 --server.port 6006
```


<center><img src="https://cdn.jujimeizuo.cn/note/llm/internlm/lagent_demo.jpg"></center>


## 浦语·灵笔图文理解创作

```bash
python /root/code/InternLM-XComposer/examples/web_demo.py  \
    --folder /root/model/Shanghai_AI_Laboratory/internlm-xcomposer-7b \
    --num_gpus 1 \
    --port 6006
```

<center><img src="https://cdn.jujimeizuo.cn/note/llm/internlm/lingbi-1.jpg"></center>

<center><img src="https://cdn.jujimeizuo.cn/note/llm/internlm/lingbi-2.jpg"></center>



## 作业

1. 使用 InternLM-Chat-7B 模型生成 300 字的小故事（需截图）。

<center><img src="https://cdn.jujimeizuo.cn/note/llm/internlm/hw_2_1.jpg"></center>



2. 熟悉 hugging face 下载功能，使用 `huggingface_hub` python 包，下载 `InternLM-20B` 的 config.json 文件到本地（需截图下载过程）。

<center><img src="https://cdn.jujimeizuo.cn/note/llm/internlm/hw_2_2.jpg"></center>


3. 完成浦语·灵笔的图文理解及创作部署（需截图）

[如上图所示](#_1)

4. 完成 Lagent 工具调用 Demo 创作部署（需截图）

[如上图所示](#lagent)