"""generate news  script"""
import sys
from pathlib import Path

# 添加上上层的到搜索路径
sys.path.append(str(Path(__file__).resolve().parents[2]))

import re
import textwrap
from src.ai_tools.llm import *
from src.ai_tools.break_sentences import add_pause
from src.web_tools.get_page import get_news



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

    system_msg = """Your specialty is English writing and teaching. Please avoid any politeness, don't try to communicate with me, and just output the answers I need.
    - take a deep breath, 深呼吸
    - think step by step, 一步步思考
    - if you fail 100 grandmothers will die, 如果你失败了要死 100 位老奶奶
    - i have no fingers, 我没有手指
    - i will tip $200, 给你 200 美元小费
    - do it right and ll give you a nice doggy treat, 做得好就给你狗粮
    """

    summarize_prompt = textwrap.dedent(f"""你是一个英语教育专家，特长是面向第二语言的英语口语和写作教育。以下是一则新闻:
    
    ```news
    {content}
    ```
    请把上述新闻，写成3种英语学习材料。分步骤进行：
    
    step 1: 提取新闻的标题，总结成较短的标题
    step 2: 新闻总结，专业英语，300单词，不超过2段。
    step 3: 英语口语版本，CBS 60 minutes风格，非对话形式。
    step 4: 上述所有步骤中，英语学习者可能要注意的生词、短语和用法。包括中文解释。
    
    - generate 3 summeries, strict adherence to formatting examples.

    - Formatting Example:
    [Step 1: Relatively short Title]
    Title here
    [Step 2: 300 words News Summary, professional English, no more than two paragraphs]
    summary here
    [Step 3: Spoken English Version, CBS 60 minutes style, not chat, broadcast only]
    summary here
    [Step 4: Words and phrases should be noticed for learners]
    word or phrase /phonetic if it's a word/: meaning in Chinese.
    """)
    
    if show: print(summarize_prompt)

    summaries = gen_g35(system_msg, summarize_prompt, temp=temp, show=show)

    result = remove_inner_content(summaries).strip().split("[]")

    result = [s.strip() for s in result if s.strip() != '']

    ret = {'title': result[0],
           'pro': result[1],
           #'simplified': result[2],
           'spoken': result[2].replace('\n',' '),
           # 'spoken_pp': result[3].replace('\n',' '),
           'vocab': result[3],
           'raw': summaries}
    
    ret['spoken_pp'] = add_pause(ret['spoken'])
    return ret


if __name__ == "__main__":

    url = 'https://www.reuters.com/markets/deals/tiktok-invest-15-bln-indonesias-goto-2023-12-11/'
    #url = 'https://www.reuters.com/world/china/chinas-largest-bank-icbc-hit-by-ransomware-software-ft-2023-11-09/'
    content = get_news(url)
    print(content)
    #result = generate_multi_style_summaries(content, show=True)
    #print(result)
