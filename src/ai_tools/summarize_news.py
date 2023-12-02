"""generate news  script"""
import sys
from pathlib import Path

# 添加上上层的到搜索路径
sys.path.append(str(Path(__file__).resolve().parents[2]))

import re
import textwrap
from src.ai_tools.llm import *

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
    - 以下全部总结，不要使用符号缩写，而要使用便于阅读的形式。例如: "$1 billion" -> "1 billion dollers"
    
    step 0: 提取新闻的标题，总结成较短的标题
    step 1: 新闻总结，专业英语，400单词，不超过2段。
    step 2: 简单英语版本，面向学历较高的第二语言的学习者，400单词。
    step 3: 英语口语版本，使用 CBS 60 minutes 的语言风格，250单词。
    step 4: 对上一个版本中的长句，比如从句或者复合句，加入适当的停顿标签 <pp>，符合人类说话的停顿节奏。
    step 5: 上述所有步骤中，英语学习者可能要注意的生词、短语和用法。包括中文解释。
    
    - generate 3 summeries, strict adherence to formatting examples.

    - Formatting Example:
    [Step 0: Relatively short Title]
    Title here
    [Step 1: 400 words News Summary, professional English, no more than two paragraph]
    summary here
    [Step 2: 400 words Simplified English for Well Educated Second Language Learners]
    summary here
    [Step 3: Spoken English Version for Well Educated Second Language Learners]
    summary here
    [Step 4: Renew of Spoken English version with pause tag <pp> to make long sentences easier to read]
    summary here
    [Step 5: words and phrases should be noticed for learners]
    word or phrase /phonetic if it's a word/: meaning in Chinese.
    """)
    
    if show: print(summarize_prompt)

    summaries = gen_g35(system_msg, summarize_prompt, temp=temp, show=show)

    result = remove_inner_content(summaries).strip().split("[]")

    result = [s.strip() for s in result if s.strip() != '']

    ret = {'title': result[0],
           'pro': result[1],
           'simplified': result[2],
           'spoken': result[3].replace('\n',' '),
           'spoken_pp': result[4].replace('\n',' '),
           'vocab': result[5],
           'raw': summaries}

    return ret


if __name__ == "__main__":

    url = 'https://www.wsj.com/tech/ai/microsoft-needs-a-better-seat-at-openais-table-64bc3c3b?mod=tech_lead_pos1'
    #url = 'https://www.reuters.com/world/china/chinas-largest-bank-icbc-hit-by-ransomware-software-ft-2023-11-09/'
    print(url)
    result = generate_multi_style_summaries(url, show=True)
