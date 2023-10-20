import re
import os
import shutil

def sanitize_filename(filename):
    """替换Windows和Linux中都不允许的字符"""
    
    sanitized = re.sub(r'[\\/:*?"<>|]', '_', filename)
    
    # 检查文件名长度
    if len(sanitized) > 255:
        raise ValueError("Filename too long")
    
    return sanitized


def reset_directory(directory_path):
    """清空文件夹：存在在删除，然后递归建立"""
    # 检查文件夹是否存在
    if os.path.exists(directory_path):
        # 删除文件夹及其所有内容
        shutil.rmtree(directory_path)
    
    # 递归创建文件夹
    os.makedirs(directory_path)
    

def move_and_tag(src_file_path, dst_directory_path, tag=None):
    """
    将文件从源路径（src_file_path）移动到目标文件夹（dst_directory_path），并根据需要添加标签（tag）。

    参数:
    src_file_path (str): 源文件的完整路径
    dst_directory_path (str): 目标文件夹的路径
    tag (str, optional): 要添加到文件名的标签，默认为None

    返回:
    None
    """
    # 确保目标文件夹存在，如果不存在，则创建
    if not os.path.exists(dst_directory_path):
        os.makedirs(dst_directory_path)
    
    # 获取源文件的文件名和扩展名
    src_file_name, file_extension = os.path.splitext(os.path.basename(src_file_path))
    
    # 如果提供了标签，添加到文件名中
    if tag:
        src_file_name = f"{src_file_name}_{tag}"
    
    # 构建目标文件的完整路径
    dst_file_path = os.path.join(dst_directory_path, f"{src_file_name}{file_extension}")
    
    # 移动文件
    shutil.move(src_file_path, dst_file_path)
    
def move_file_to_directory(src_file_path, dst_directory_path):
    """
    将文件从源路径（src_file_path）移动到目标文件夹（dst_directory_path）。

    参数:
    src_file_path (str): 源文件的完整路径
    dst_directory_path (str): 目标文件夹的路径

    返回:
    None
    """
    # 确保目标文件夹存在，如果不存在，则创建
    if not os.path.exists(dst_directory_path):
        os.makedirs(dst_directory_path)
    
    # 获取源文件的文件名
    src_file_name = os.path.basename(src_file_path)
    
    # 构建目标文件的完整路径
    dst_file_path = os.path.join(dst_directory_path, src_file_name)
    
    # 移动文件
    shutil.move(src_file_path, dst_file_path)
    
def setup_dirs():
    # %%
    # 建立2个必要文件夹
    if not os.path.exists('data'):
        os.mkdir('data')
    if not os.path.exists('data/album'):
        os.mkdir('data/album')
    if not os.path.exists('data/scripts'):
        os.mkdir('data/scripts')

    # 清空2个文件夹
    reset_directory('data/output')
    reset_directory('data/fragments')
