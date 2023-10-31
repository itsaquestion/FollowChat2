# %%
from src.ms_tts.audio_tools import merge_mp3_files_in_directory, combine_wav
from src.web_tools import get_news_content
from src.ai_tools.summarize_news import generate_multi_style_summaries
from src.dialogue_script_processor import process_chat
from src.ms_tts.text_to_audio import script_to_wav_files
from src.utils import *
from datetime import datetime

import os


def gen_audio_from_page(url, show=False):
    """
    从新闻连接中生成音频文件
    """

    print('\n生成总结 =======')

    content = url
    if "bbc.com" in url:
        get_news_content(url)

    multi_summaries = generate_multi_style_summaries(
        content, temp=0.2, show=show)

    if not os.path.exists('data/scripts'):
        os.mkdir('data/scripts')

    today = datetime.today()
    base_name = sanitize_filename(today.strftime(
        "%Y%m%d-%H%M") + "_" + "News_" + multi_summaries['title']).replace('__','_').replace('_-','-')

    file_name = (base_name + '.txt').replace('..', '.')
    with open('data/scripts/' + file_name, 'w', encoding='utf-8') as f:
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

            
def gen_album(urls):
    """合并新闻，添加一个tag，并移动到album"""
    setup_dirs()

    # 对每一条新闻都生成脚本和音频
    for url in urls:
        gen_audio_from_page(url, show=False)


    # output下的音频拷贝到album
    # 注意output也只是临时文件夹，每次生成的时候会清空
    source_folder = 'data/output/'
    destination_folder = 'data/album/'
    
    # 遍历源文件夹中的所有文件
    for filename in os.listdir(source_folder):
        source = os.path.join(source_folder, filename)
        destination = os.path.join(destination_folder, filename)

        # 拷贝文件
        shutil.copy(source, destination)
    
    # 非今天的文件转移到Archive
    move_dated_files_to_archive('data/album','data/album_archive')
    move_dated_files_to_archive('data/scripts','data/scripts_archive')
    
    #print('\n合并音频 ====')
    #merged_file = merge_mp3_files_in_directory('data/output')

    #move_and_tag(merged_file, 'data/album', tag)
