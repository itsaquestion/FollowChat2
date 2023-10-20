# %%
from src.ms_tts.audio_tools import merge_mp3_files_in_directory
from src.web_tools import get_news_content
from src.ai_tools.summarize_news import generate_multi_style_summaries
from src.dialogue_script_processor import process_chat
from src.ms_tts.text_to_audio import script_to_wav_files
from src.ms_tts.audio_tools import combine_wav
from src.utils import sanitize_filename
from datetime import datetime
from src.web_tools import google_news
import os


def gen_audio_from_page(url):
    """
    从新闻连接中生成音频文件
    """

    print('\n生成总结 =======')

    content = url
    if "bbc.com" in url:
        get_news_content(url)

    multi_summaries = generate_multi_style_summaries(
        content, temp=0.2, show=False)

    if not os.path.exists('data/scripts'):
        os.mkdir('data/scripts')

    today = datetime.today()
    base_name = sanitize_filename(today.strftime(
        "%Y%m%d") + "_" + "News_" + multi_summaries['title'])

    file_name = (base_name + '.txt').replace('..', '.')
    with open('data/script/' + file_name, 'w') as f:
        f.write(multi_summaries['raw'])

    print('')
    print('\n处理对话 =======')

    new_script = process_chat('Aria: ' + multi_summaries['spoken'])
    new_script = 'Jenny: ' + multi_summaries['title'] + '\n' + new_script
    print(new_script)

    print('\n生成音频 =======')
    script_to_wav_files(new_script)

    print('\n合并音频 =======')

    file_name = (base_name + '.mp3').replace('..', '.')
    combine_wav(file_name)
    print('完成')

# %%


news_info = google_news.get_news_scmp('').head()[['title', 'link']]

urls = news_info['link']

# %%
# 如果output文件夹存在，则删除
if not os.path.exists('data'):
    os.mkdir('data')

for url in urls:
    gen_audio_from_page(url)
# %%

merge_mp3_files_in_directory('data/output')

# %%
