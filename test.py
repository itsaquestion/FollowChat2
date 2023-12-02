
# %%
from IPython.display import Audio
import sys
import os

def load_StyleTTS2(package_path = 'D:\\tts\\StyleTTS2'):
    last_wd = os.getcwd()

    sys.path.append(package_path)
    os.chdir(package_path)
    from StyleTTS2 import StyleTTS2

    tts = StyleTTS2()

    os.chdir(last_wd)

    return tts

tts = load_StyleTTS2()
# %%
text = "Wall Street futures went up a bit on Tuesday because investors are hopeful that inflation will go down. They feel this way because they think the central banks will keep helping the economy, especially since there are signs that growth is slowing down."

ref_s = tts.compute_style('voices/Talor.wav')
wav = tts.inference(text, ref_s, alpha=0.3, beta=0.7, diffusion_steps=5, embedding_scale=1)

Audio(wav, rate=24000, normalize=False)

# %%
tts.device

# %%


import wave
import numpy as np


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


wave_to_file(wav, 'test.wav')

# %%
