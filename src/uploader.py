import paramiko
import os
from tqdm import tqdm

def get_ssh_config(host_name):
    """从SSH配置文件中获取主机配置信息"""
    ssh_config = paramiko.SSHConfig()
    user_config_file = os.path.expanduser("~/.ssh/config")
    if os.path.exists(user_config_file):
        with open(user_config_file) as f:
            ssh_config.parse(f)

    return ssh_config.lookup(host_name)

def upload_files(ssh_host, local_dir, remote_dir, delete_remote=False, verbose=False):
    try:
        # 获取SSH配置
        config = get_ssh_config(ssh_host)
        print(config)

        # 创建SSH对象
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # 连接SSH
        ssh.connect(config.get('hostname', ssh_host),
                    username=config.get('user'),
                    port=config.get('port', 22),
                    key_filename=config.get('identityfile'))

        # 创建SFTP客户端
        sftp = ssh.open_sftp()

        # 如果指定了删除远程文件夹的内容
        if delete_remote:
            print(f"正在删除远程目录 {remote_dir} 的内容...")
            stdin, stdout, stderr = ssh.exec_command(f'rm -rf {remote_dir}/*')
            print(stdout.read().decode('utf-8'))
            print(stderr.read().decode('utf-8'))

        # 递归上传文件
        recursive_upload(sftp, local_dir, remote_dir,verbose = verbose)

        # 关闭连接
        sftp.close()
        ssh.close()
    except Exception as e:
        print(f'上传过程中出错: {e}')

def list_files_for_upload(local_dir):
    """递归列出所有待上传的文件"""
    files_for_upload = []
    for root, dirs, files in os.walk(local_dir):
        for file in files:
            local_path = os.path.join(root, file)
            # 将路径转换为Linux格式
            relative_path = os.path.relpath(local_path, local_dir).replace('\\', '/')
            files_for_upload.append(relative_path)
    return files_for_upload

def recursive_upload(sftp, local_dir, remote_dir, verbose=True):
    """递归上传目录中的所有文件，可选择显示详细信息或进度条"""
    files = list_files_for_upload(local_dir)
    progress = tqdm(files, desc="上传中", disable=verbose)

    for file in progress:
        local_path = os.path.join(local_dir, file).replace('\\', '/')
        remote_path = os.path.join(remote_dir, file).replace('\\', '/')

        # 如果需要，创建远程目录
        remote_folder = os.path.dirname(remote_path)
        try:
            sftp.listdir(remote_folder)
        except IOError:
            create_remote_dir(sftp, remote_folder)

        sftp.put(local_path, remote_path)
        if verbose:
            print(f'上传文件：{local_path} 到 {remote_path}')

    progress.close()

def create_remote_dir(sftp, remote_directory):
    """递归创建远程目录"""
    if remote_directory == "/":
        # 如果是根目录，则不需要创建
        return
    if remote_directory == "":
        return
    try:
        sftp.listdir(remote_directory)  # 测试目录是否存在
    except IOError:
        create_remote_dir(sftp, os.path.dirname(remote_directory))  # 创建父目录
        sftp.mkdir(remote_directory)  # 创建当前目录

def upload_all():
    # 设置参数
    ssh_host = 'hk.imtass.me'  # 或者在~/.ssh/config中配置的主机名

    # 执行上传
    upload_files(ssh_host, './web/_book', '/www/news', delete_remote=True, verbose=False)
    upload_files(ssh_host, 'data/album', '/home/lee/docker-jellyfin/media', delete_remote=True,verbose=False)

if __name__ == "__main__":
    upload_all()
