from src.web_tools import get_news_content
from src.ai_tools.summarize_news import generate_multi_style_summaries
from src.dialogue_script_processor import process_chat
from src.ms_tts.text_to_audio import script_to_wav_files
from src.ms_tts.audio_tools import combine_wav
from src.utils import sanitize_filename
from datetime import datetime


urls = ['https://www.reuters.com/technology/google-pushes-deeper-into-ai-publishers-see-fresh-challenges-2023-10-19/',
        ]


url = 'https://www.wsj.com/economy/housing/china-stabilizes-in-the-shadow-of-country-garden-and-evergrande-7574010a' #urls[0]

print('\n生成总结 =======')

content = get_news_content(url)
if "www.scmp.com" in url or "www.reuters.com" in url or "wsj.com" in url:
    content = url

multi_summaries = generate_multi_style_summaries(content)
print('')
print('\n处理对话 =======')

script = 'Jenny: ' + multi_summaries['title']
script += '\nAria: ' + multi_summaries['spoken']

new_script = process_chat('Aria: ' + multi_summaries['spoken'])

# print('\n生成音频 =======')
# script_to_wav_files(new_script)

# print('\n合并音频 =======')
# today = datetime.today()
# file_name = sanitize_filename(today.strftime(
#     "%Y%m%d") + "_" + "News_" + multi_summaries['title'] + '.mp3').replace('..', '.')
# combine_wav(file_name)
