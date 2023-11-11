"""
1. 渲染web目录下的quarto工程
2. 删除/www/followchat2
3. 拷贝/web/_book到/www/followchat2
"""
import subprocess
import shutil
import os


def run_command(command):
    # 定义要运行的shell命令

    # 使用 subprocess.Popen 运行命令，并捕获输出
    process = subprocess.Popen(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
    )

    # 实时打印命令的输出
    for line in iter(process.stdout.readline, ""):
        print(line, end="")

    # 等待进程完成
    process.stdout.close()
    return_code = process.wait()
   
    return return_code 
#    if return_code:
#        raise subprocess.CalledProcessError(return_code, command)



def build_and_deploy():
    run_command(command="quarto render web")
    path = '/www/followchat2'
    
    if os.path.exists(path) and os.path.isdir(path):
        # 删除文件夹及其所有内容
        shutil.rmtree(path)
        print(f"Folder '{path}' has been deleted.")

    src = 'web/_book'
    dst = '/www/followchat2'

    if not os.path.exists(src) or not os.path.isdir(src):
        print(f"Source directory '{src}' does not exist or is not a directory.")
        return

    # 检查目标目录是否存在
    if os.path.exists(dst):
        print(f"Destination directory '{dst}' already exists.")
        return

    # 拷贝目录
    shutil.copytree(src, dst)
    print(f"Directory '{src}' has been copied to '{dst}'.")
    

if __name__ == "__main__":
    build_and_deploy()
    # print(return_code)
