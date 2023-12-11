# %%
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
import wave
import numpy as np
import sys

# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"

# %%
def load_StyleTTS2(package_path = 'D:\\tts\\StyleTTS2'):
    last_wd = os.getcwd()
    sys.path.append(package_path)
    os.chdir(package_path)
    from StyleTTS2 import StyleTTS2

    tts = StyleTTS2()

    os.chdir(last_wd)

    return tts


def wave_to_file(wav, file_path):
    rate = 24000  # 采样率
    nchannels = 1  # 声道数
    sampwidth = 2  # 样本宽度（以字节为单位）

    # 创建一个 wave 文件
    with wave.open(file_path, 'w') as wf:
        wf.setnchannels(nchannels)
        wf.setsampwidth(sampwidth)
        wf.setframerate(rate)

        # 确保音频数据是 int16 格式
        wav_int16 = np.int16(wav * 32767) if wav.dtype != np.int16 else wav

        # 写入数据
        wf.writeframes(wav_int16.tobytes())

# print('load xtts_v2')
# tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
xtts_v2 = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

# style_tts = load_StyleTTS2()

# def tts_to_file(text, speaker_wav, file_path, backend =  None):
#     # print(f'\n[TTS backend: {backend}]')
#     if backend == 'style_tts2':
#         ref_s = style_tts.compute_style(speaker_wav)
#         wav = style_tts.inference(text, ref_s, alpha=0.3, beta=0.7, diffusion_steps=5, embedding_scale=1)
#         wave_to_file(wav,file_path)
#     else:
#         xtts_v2.tts_to_file(text=text, speaker_wav=speaker_wav, language="en", file_path=file_path )

def tts_to_file(text, speaker_wav, file_path, backend =  None):
    xtts_v2.tts_to_file(text=text, speaker_wav=speaker_wav, language="en", file_path=file_path )


# %%
def script_to_wav_files(chat_script, output_dir='data/fragments', backend =  'style_tts2' ):
    
    """把原始对话文本，首先重新断句，然后转化音频文件，按顺序命名为001.wav,002.wav

    Args:
        chat_script (str): 处理过的脚本，每行的开头都是说话的人名。如：
            'Aria: Hey there, welcome to today\'s episode of "The English Corner"!
            Aria: Today, we're talking about Netflix and their recent news.'

        output_dir (str): 输出wav文件的目录
    """

    chat_script = chat_script.replace("-",' ')

    # 如果output文件夹存在，则删除
    if os.path.exists(output_dir):
        print(f'{output_dir}目录存在，删除')
        shutil.rmtree(output_dir)

    # 创建新的output文件夹
    os.mkdir(output_dir)

    counter = 0
    for chat in tqdm(chat_script.split('\n')):

        # 尝试去掉行末的','
        chat = chat.strip().rstrip(',')
        counter += 1
        #print(counter)
        if not ':' in chat:
            continue
        speaker, text = [x.strip() for x in chat.split(':')][:2]

        file_path = output_dir + '/'+'{:0>3}'.format(counter) + '.wav'
        # tts.tts_to_file(text=text, speaker_wav=f"voices/{speaker}.wav", language="en", file_path=file_path )
        tts_to_file(text=text,speaker_wav=f"voices/{speaker}.wav", file_path=file_path, backend = backend)

if __name__ == "__main__":
    import os

    # 获取当前文件的绝对路径
    current_file = os.path.abspath(__file__)

    # 获取当前文件所在目录的上一层的上一层目录
    parent_parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))

    # 更改当前工作目录
    # print(parent_parent_dir)

    text  = "It is a repetitive, painful and familiar feeling for Gershkovich’s vast and close-knit network of friends. It has motivated The Wall Street Journal reporter’s friends who are pushing for his release, helping him stay connected to the outside world and keeping his name and plight on others’ minds."
    
    script_to_wav_files(text)
