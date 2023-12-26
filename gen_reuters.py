# %%
import subprocess



from src.dialogue_script_processor.script_to_md import conver_all_scripts

from src.news import get_headlines_reuters
from src.build_and_deploy import build_web
from src.uploader import upload_all

from time import sleep

import sys
import warnings


# 保存原始的stdout
original_stdout = sys.stdout
original_filters = warnings.filters[:]

# 创建一个空的输出流，将其用于屏蔽输出
null_output = open('/dev/null', 'w')  # On Windows, you can use 'nul' instead of '/dev/null'

# 将stdout重定向到空的输出流
sys.stdout = null_output

# 禁用所有警告
warnings.simplefilter("ignore")

# 执行带有import语句的代码
from src.gen_album import gen_album

# 恢复原始的stdout
sys.stdout = original_stdout
warnings.filters = original_filters
# 关闭空的输出流
null_output.close()

def run_shell_command(command):
    try:
        # 使用subprocess执行Shell命令，并等待其完成
        completed_process = subprocess.run(command, shell=True, check=True)

        # 检查命令的返回代码
        if completed_process.returncode == 0:
            return True, "Shell命令成功执行"
        else:
            return False, "Shell命令执行失败"
    except subprocess.CalledProcessError as e:
        return False, f"Shell命令执行失败: {e}"
    

run_shell_command('docker restart chrome')

sleep(5)

news_info = get_headlines_reuters()

news_info = news_info.head(5)

print(news_info)

# %%
if news_info is not None:
    urls = news_info['url']
    print(urls)
    
    gen_album(urls)

    conver_all_scripts()
    
    build_web()

    upload_all()