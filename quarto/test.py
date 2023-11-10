# %%
import re

def replace_step_with_caption(text, n, caption, new_line = False):
    # This regex will match the entire '[step n: title]' and replace it with 'caption'
    pattern = r'\[Step ' + re.escape(str(n)) + r':.*?\]'

    if new_line:
        pattern += r'\n?'
    new_text = re.sub(pattern, caption, text)
    
    return new_text

def script_to_qmd(file_path):
    with open(file_path,'r',encoding='utf-8') as f:
        text = f.read()
    
    text = replace_step_with_caption(text,'0', '# Title: ')
    text = replace_step_with_caption(text,'1', '# Professional English')
    text = replace_step_with_caption(text,'2', '# Simplified English')
    text = replace_step_with_caption(text,'3', '# Spoken English')
    text = replace_step_with_caption(text,'4', '# Spoken English with pause')
    text = replace_step_with_caption(text,'5', '# Vocabulary', False)
    
    return text
    

file_path = '..\\data\\scripts\\20231110-1142_News_Brazil Minister Angered by Israeli Statement on Foiled Hezbollah Attack - Reuters.txt'

print(script_to_qmd(file_path))


# %%
