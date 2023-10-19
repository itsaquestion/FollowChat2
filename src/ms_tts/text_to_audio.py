"""用于把字符转化语音文件
"""
import os
import shutil
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv
from datetime import datetime
import os
from pydub import AudioSegment
from tqdm import tqdm


load_dotenv()

speech_config = speechsdk.SpeechConfig(subscription=os.environ.get(
    'SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))

speech_synthesizer = speechsdk.SpeechSynthesizer(
    speech_config=speech_config, audio_config=None)


def text_to_audio(text, speaker, style='chat', style_degree='0.1', debug=False):
    """字符转为语音

    Args:
        text (str): 要说的字符，如'Hello!'
        speaker (str): 角色，如'Jenny'
        file_path (str): 保存文件的路径，如'output/001.wav'
        style (str, optional): 说话风格. Defaults to 'excited'.
        style_degree (str, optional): 风格的强度. Defaults to '0.3'.
        debug (bool, optional): 是否显示SSML字符串. Defaults to False.

    Returns:
        [AudioDataStream]: 音频流数据
    """

    current_dir = os.path.dirname(__file__)
    template_path = os.path.join(current_dir, 'ssml_template.xml')

    with open(template_path, 'r') as f:
        template = f.read()

    ssml_string = template.format(
        speaker=speaker, text=text, style=style, style_degree=style_degree)

    if debug:
        print(ssml_string)
    result = speech_synthesizer.speak_ssml_async(ssml_string).get()

    stream = speechsdk.AudioDataStream(result)
    return stream  # stream.save_to_wav_file(file_path)


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
        stream = text_to_audio(text, speaker)

        file_path = output_dir + '/'+'{:0>3}'.format(counter) + '.wav'
        stream.save_to_wav_file(file_path)


