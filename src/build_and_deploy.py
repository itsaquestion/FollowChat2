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
    

import paramiko
import os

def recursive_upload(sftp, local_dir, remote_dir):
    """递归上传目录中的所有文件和子目录"""
    for item in os.listdir(local_dir):
        local_path = os.path.join(local_dir, item)
        remote_path = os.path.join(remote_dir, item)

        if os.path.isfile(local_path):
            print(f'正在上传文件：{local_path} 到 {remote_path}')
            sftp.put(local_path, remote_path)
        elif os.path.isdir(local_path):
            print(f'创建远程目录：{remote_path}')
            try:
                sftp.mkdir(remote_path)
            except IOError:
                pass  # 忽略已存在的目录错误
            recursive_upload(sftp, local_path, remote_path)

def upload_files(ssh_host, ssh_username, local_dir, remote_dir):
    try:
        # 创建SSH对象
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ssh_host, username=ssh_username)

        # 创建SFTP客户端
        sftp = ssh.open_sftp()

        # 递归上传文件
        recursive_upload(sftp, local_dir, remote_dir)

        # 关闭连接
        sftp.close()
        ssh.close()
    except Exception as e:
        print(f'上传过程中出错: {e}')



if __name__ == "__main__":
    # build_web()
    import os
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    print("当前工作目录:", os.getcwd())
    # run_command("bin/rsync.exe -av -e ssh _book/ lee@hk.imtass.me:/www/news ")
    
    # 设置参数
    ssh_host = 'hk.imtass.me'
    ssh_username = 'lee'
    local_dir = './web/_book'
    remote_dir = '/www/news'

    # 执行上传
    upload_files(ssh_host, ssh_username, local_dir, remote_dir)
