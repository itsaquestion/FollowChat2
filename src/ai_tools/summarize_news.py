"""generate news  script"""

import re
import textwrap
from .llm import *

def remove_inner_content(text):
    # 使用正则表达式找到所有的[[内容]]，并将其中的内容替换为空
    return re.sub(r'\[(.*?)\]', '[]', text)


def generate_multi_style_summaries(content,temp=0.2, show=True):
    """从文本中生成专业英语、简单英语和口语版本的总结。如果输入一个网页，LLM会帮你读出来，但BBC的网址会出错。

    Args:
        content: 要总结的文本，可以是文本、字典，甚至是网页。

    Returns:
        一个字典: {title, pro, simplified, spoken}
    """

    system_msg = "Your specialty is English news writing and teaching. Please avoid any politeness, don't try to communicate with me, and just output the answers I need."

    summarize_prompt = textwrap.dedent(f"""
    这是一则新闻:
    
    ```news
    {content}
    ```
     
    - 你是一个英语教育专家，特长是面向第二语言的英语口语和写作教育。请把上述新闻，写成3种英语学习材料，分步骤进行：

    step 0: 提取新闻的标题，总结成较短的标题，包含新闻来源。
    step 1: 新闻总结，专业英语，250单词
    step 2: 简单英语版本，面向第二语言的学习者，250单词
    step 3: 口语化版本，使用 TED Talks 的语音风格，作为英语学习者的口语练习材料，250单词
    
    - generate 3 summeries, strict adherence to formatting examples.
        
    - Formatting Example:
    [Step 0: Relative short Title includes the source]
    Title here.
    [Step 1: 250 words News Summary, professional English]
    summary here
    [Step 2: 250 words Simplified English for Second Language Learners]
    summary here
    [Step 3: 250 words Spoken English for Language Learners, TED Talks' style]
    summary here

    """)
    
    print(summarize_prompt)

    summaries = gen_g35(system_msg, summarize_prompt, temp=temp, show=show)

    result = remove_inner_content(summaries).strip().split("[]")

    result = [s.strip() for s in result if s.strip() != '']

    ret = {'title': result[0],
           'pro': result[1],
           'simplified': result[2],
           'spoken': result[3].replace('\n',''),
           'raw': summaries}

    return ret


if __name__ == "__main__":
    # import doctest
    # doctest.testmod()

    # print('测试完成')
    url = 'https://www.reuters.com/technology/netflix-raises-prices-it-adds-9-million-subscribers-2023-10-18/'
    result = generate_multi_style_summaries(url, show=True)
    print("\n\n")
    print(result)
