
import os
import shutil

from datetime import datetime
import os
from pydub import AudioSegment


def merge_mp3_files_in_directory(directory_path):

    all_files = [f for f in os.listdir(directory_path) if f.endswith(
        '.mp3') and ("Chat_" in f or "Disc_" in f or "News_" in f)]

    # 2. 使用日期创建一个字典
    files_by_date = {}
    for file_name in all_files:
        date_type = '_'.join(file_name.split('_')[:2])
        if date_type not in files_by_date:
            files_by_date[date_type] = []
        files_by_date[date_type].append(file_name)

    # 3. 合并同一天的所有MP3文件
    for date_type, files in files_by_date.items():
        output_path = os.path.join(directory_path, f"{date_type}.mp3")
        print(f'{output_path=}')
        # 如果输出文件已经存在，跳过
        if os.path.exists(output_path):
            print(f"{date_type}.mp3已经存在，跳过")
            continue

        combined = AudioSegment.empty()
        for file_name in files:
            path = os.path.join(directory_path, file_name)
            audio = AudioSegment.from_mp3(path)
            combined += audio

        combined.export(output_path, format="mp3",
                        codec="libmp3lame", parameters=["-q:a", "0"])
    
    return output_path


def combine_wav(file_name, input_dir='data/fragments', output_dir='data/output'):
    audio_files = sorted(
        [f for f in os.listdir(input_dir) if f.endswith('.wav')])
    # audio_files

    # 初始化一个空的音频段
    combined_audio = AudioSegment.empty()

    # 遍历每个音频文件
    for audio_file in audio_files:
        # 加载音频
        audio = AudioSegment.from_wav(os.path.join(input_dir, audio_file))

        # 创建一个等长的静音段
        silence = AudioSegment.silent(duration=len(audio))

        # 合并音频和静音段
        segment_to_add = audio + audio + silence + audio + silence

        # 添加到总的音频段
        combined_audio += segment_to_add

    # 保存合并后的音频
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_path = os.path.join(output_dir, file_name)
    combined_audio.export(output_path, format="mp3", bitrate='256k')

    output_path
