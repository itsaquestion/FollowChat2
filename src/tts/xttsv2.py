"""用于把字符转化语音文件
"""
import os
import shutil
from dotenv import load_dotenv
from datetime import datetime
import os
from pydub import AudioSegment
from tqdm import tqdm

import torch
from TTS.api import TTS

# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"

tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

# %%
def script_to_wav_files(chat_script, output_dir='data/fragments'):
    
    """把原始对话文本，首先重新断句，然后转化音频文件，按顺序命名为001.wav,002.wav

    Args:
        chat_script (str): 处理过的脚本，每行的开头都是说话的人名。如：
            'Aria: Hey there, welcome to today\'s episode of "The English Corner"!
            Aria: Today, we're talking about Netflix and their recent news.'

        output_dir (str): 输出wav文件的目录
    """

    # 如果output文件夹存在，则删除
    if os.path.exists(output_dir):
        print(f'{output_dir}目录存在，删除')
        shutil.rmtree(output_dir)

    # 创建新的output文件夹
    os.mkdir(output_dir)

    counter = 0
    for chat in tqdm(chat_script.split('\n')):
        counter += 1
        #print(counter)
        if not ':' in chat:
            continue
        speaker, text = [x.strip() for x in chat.split(':')][:2]

        file_path = output_dir + '/'+'{:0>3}'.format(counter) + '.wav'
        tts.tts_to_file(text=text, speaker_wav=f"voices/{speaker}.wav", language="en", file_path=file_path )

if __name__ == "__main__":
    import os

    # 获取当前文件的绝对路径
    current_file = os.path.abspath(__file__)

    # 获取当前文件所在目录的上一层的上一层目录
    parent_parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))

    # 更改当前工作目录
    # print(parent_parent_dir)

    text  = "Major indexes were little changed at open. Fast-fashion giant Shein filed for what could be one of the biggest market debuts in years. Treasury yields edged up and oil prices rose."
    script_to_wav_files(text)
