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


def build_web():
    run_command(command="quarto render web")

