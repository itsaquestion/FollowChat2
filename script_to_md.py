# %%
import re
from pathlib import Path


def replace_step_with_caption(text, n, caption, new_line = True):
    # This regex will match the entire '[step n: title]' and replace it with 'caption'
    pattern = r'\[Step ' + re.escape(str(n)) + r':.*?\]'
    
    if not new_line:
        pattern += '\n?'
    new_text = re.sub(pattern, caption, text)
    return new_text


def script_to_md(script_path):
    with open(script_path,'r',encoding='utf-8') as f:
        text = f.read()
        
    text = replace_step_with_caption(text,0,'# ', False)
    text = replace_step_with_caption(text,1,'## Professional English')
    text = replace_step_with_caption(text,2,'## Simplified English')
    text = replace_step_with_caption(text,3,'## Spoken English')
    text = replace_step_with_caption(text,4,'## Spoken English with pause tag')

    text = replace_step_with_caption(text,5,'## Vocabulary')
    
    return text

def change_file_extension_to_filename_only(path, new_extension):
    """
    修改给定路径的文件扩展名，并仅返回新的文件名（不包括路径）。

    :param path: 文件的路径。
    :param new_extension: 新的扩展名，不需要以点开头。
    :return: 修改扩展名后的文件名，不包括路径。
    """
    file_path = Path(path)
    # 修改扩展名并提取新的文件名
    new_file_name = file_path.with_suffix('.' + new_extension).name
    return new_file_name

# 示例使用


script_path = 'data/scripts/20231110-1445_News_Gaza Hospitals Under Attack by Israeli Forces - Reuters.txt'


#print(text)

md_content = script_to_md(script_path)

md_filename = change_file_extension_to_filename_only(script_path, 'md')

quarto_dir = 'web'

full_path = Path(quarto_dir, md_filename)

with open(full_path,'w',encoding = 'utf-8') as f:
    f.write(md_content)

# %%
import os

[f for f in os.listdir(quarto_dir) if f.endswith(('.qmd','md','.ipynb'))]



