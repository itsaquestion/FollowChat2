"""
这个模块提供了一些实用的工具函数，包括替换字符串中的占位符。

函数列表：
- replace_placeholders：读取文件内容，并将文件中的占位符替换为指定的文本。
"""
import os
import openai
from dotenv import load_dotenv
from functools import partial

load_dotenv()

openai.api_key = os.environ["OR_KEY"]
openai.api_base = "https://openrouter.ai/api/v1"


def gen(system_msg, user_msg, temp=0.2,  show=True, model='openai/gpt-3.5-turbo'):
    """
    用openrouter的api和LLM对话。
    """
    response = openai.ChatCompletion.create(model=model,
                                            messages=[{"role": "system", "content": system_msg},
                                                      {"role": "user", "content": user_msg}],
                                            headers={"HTTP-Referer": 'https://py4ss.net',  # To identify your app
                                                     "X-Title": 'FollowChat2'},
                                            max_tokens=2048,
                                            stream=True, temperature=temp)
    collected_messages = []
    for chunk in response:
        content = chunk["choices"][0].get(  # type: ignore
            "delta", {}).get("content")  # type: ignore
        if content is not None:
            collected_messages.append(content)
            if show:
                print(content, end='', flush=True)

    full_message = ''.join(collected_messages)

    return full_message


gen_g4 = partial(gen, model='openai/gpt-4')
gen_g35i = partial(gen, model='openai/gpt-3.5-turbo-instruct')
gen_g35 = partial(gen, model='openai/gpt-3.5-turbo')
gen_c2 = partial(gen, model='anthropic/claude-2')
gen_c1 = partial(gen, model='anthropic/claude-instant-v1')
gen_p2 = partial(gen, model='google/palm-2-chat-bison')
gen_l70 = partial(gen, model='meta-llama/llama-2-70b-chat')
gen_m7 = partial(gen, model='mistralai/mistral-7b-instruct')
gen_s70 = partial(gen, model='migtissera/synthia-70b')
