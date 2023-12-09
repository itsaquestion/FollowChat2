"""
add_pause: 输入text，添加停顿并返回处理好的text。 对于长句，在适合停顿的位置添加一个逗号。
"""
# %%

import sys
from pathlib import Path

# 添加上上层的到搜索路径
sys.path.append(str(Path(__file__).resolve().parents[2]))
from src.ai_tools.llm import *

from nltk.tokenize import sent_tokenize


system_msg = """- take a deep breath, 深呼吸
- think step by step, 一步步思考
- if you fail 100 grandmothers will die, 如果你失败了要死 100 位老奶奶
- i have no fingers, 我没有手指
- i will tip $200, 给你 200 美元小费
- do it right and ll give you a nice doggy treat, 做得好就给你狗粮
"""

def align_multiline_text(text, indent=0):
    """
    Aligns the text of a multi-line string with a specified indentation.

    :param text: A string containing multiple lines of text.
    :param indent: The number of spaces to add at the beginning of each line.
    :return: A string with aligned text.
    """
    # Split the text into lines
    lines = text.strip().split('\n')

    # Remove leading whitespace from each line and add specified indentation
    aligned_lines = [(' ' * indent) + line.lstrip() for line in lines]

    # Combine the lines back into a single string
    return '\n'.join(aligned_lines)


def create_prompt(sentences):

    summarize_prompt = align_multiline_text(f"""
        你是一名英语教育专家，特长是英语口语和写作的教育。请你帮我处理英语长句，在恰当的地方插入停顿符号，便于初学者阅读。

        - 以下一篇文章的句子，采用Python的List格式。

        ```
        {sentences}
        ```
        - 请判断每一个句子，如果句子有比较长或者复杂的复合结构，你就在其中加入停顿符'<pp>'，使之符合口语表达的停顿，便于英语初学者学习口语长句的说法。
        - 你的输出结果是添加了停顿符的句子。每行一句话，不要输出其他。

        - 3 examples:
        - Input: The central bank has been gradually reducing its bond-buying program, and investors want to know if there will be any changes in the pace of this reduction or when interest rates might start going up.
        - Output: The central bank has been gradually reducing its bond-buying program<pp> and investors want to know if there will be any changes in the pace of this reduction<pp> or when interest rates might start going up.
        
        - Input: Additionally, investors are also keeping a close eye on any indications from the Federal Reserve regarding its plans for tapering its bond-buying program and raising interest rates.
        - Output: Additionally<pp> investors are also keeping a close eye on any indications from the Federal Reserve<pp> regarding its plans for tapering its bond-buying program and raising interest rates.
        
        - Input: The emergence of this new COVID-19 variant has raised concerns about the possibility of renewed restrictions and disruptions to economic activity.
        - Output: The emergence of this new COVID-19 variant<pp> has raised concerns about the possibility of renewed restrictions and disruptions<pp> to economic activity.
        """
    )
    return summarize_prompt

def add_pause(text):

    sentences = sent_tokenize(text)
    prompt = create_prompt(sentences)

    print(prompt)

    return gen_g35(system_msg, prompt, temp=0.2, show=True).replace('\n',' ').replace('<pp>',',')


if __name__ == "__main__":
    
    text = """In China, consumer prices have dropped at the fastest rate in three years, and factory gate deflation has gotten worse, according to recent data. The Consumer Price Index, which measures the average change in prices of goods and services purchased by households, fell by 0.3% in November. This is the biggest drop since October 2020. The main reason for this decline is the decrease in food prices, especially pork, which went down by 12.5%. Prices of non-food items also went down a bit. On the other hand, the Producer Price Index, which measures the average change in prices received by domestic producers for their output, fell by 2.2% in November. This is the 17th consecutive month of decline. This drop in factory gate prices shows that there is weak demand and too much production capacity in China's industrial sector.

    The decrease in consumer prices is worrying because it might lead to deflation, which is a general decrease in prices. While lower prices can be good for consumers in the short term, they can also lead to less spending and investment, which can slow down economic growth. The Chinese government has been taking steps to encourage people to spend more and to help businesses that have been affected by the pandemic. However, if prices keep going down, it will be difficult for these efforts to work. The government will need to keep a close eye on the situation and think about what they can do to keep prices stable and to help the economy grow in a sustainable way.
    """

    result = add_pause(text)
    print('')
    print(result)

