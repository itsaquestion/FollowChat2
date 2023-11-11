import re
from pathlib import Path
import os
import datetime
import glob


def replace_step_with_caption(text, n, caption, new_line=True):
    # This regex will match the entire '[step n: title]' and replace it with 'caption'
    pattern = r"\[Step " + re.escape(str(n)) + r":.*?\]"

    if not new_line:
        pattern += "\n?"
    new_text = re.sub(pattern, caption, text)
    return new_text


def script_to_md(script_path):
    with open(script_path, "r", encoding="utf-8") as f:
        text = f.read()

    text = replace_step_with_caption(text, 0, "# ", False)
    text = replace_step_with_caption(text, 1, "## Professional English")
    text = replace_step_with_caption(text, 2, "## Simplified English")
    text = replace_step_with_caption(text, 3, "## Spoken English")
    text = replace_step_with_caption(text, 4, "## Spoken English with pause tag")

    text = replace_step_with_caption(text, 5, "## Vocabulary")

    return text


def change_file_extension_to_filename_only(path, new_extension):
    """
    修改给定路径的文件扩展名，并仅返回新的文件名（不包括路径）。

    :param path: 文件的路径。
    :param new_extension: 新的扩展名，不需要以点开头。
    :return: 修改扩展名后的文件名，不包括路径。
    """
    file_path = Path(path)
    # 修改扩展名并提取新的文件名
    new_file_name = file_path.with_suffix("." + new_extension).name
    return new_file_name

def delete_all_md_files(directory):
    # 构建目标目录下所有 .md 文件的路径
    path = os.path.join(directory, '*.md')
    
    # 使用 glob.glob 找到所有匹配的文件
    md_files = glob.glob(path)

    # 遍历并删除每个 .md 文件
    for file in md_files:
        os.remove(file)
        print(f"Deleted: {file}")
        
def conver_all_scripts():
    """转换脚本文件为md文件"""

    quarto_dir = "web"
    script_dir = "data/scripts"

    # 删除quarto_dir下的所有md文件
    delete_all_md_files(quarto_dir)

    # 列出脚本txt
    script_files = [
        Path(script_dir, f) for f in os.listdir(script_dir) if f.endswith(("txt"))
    ]
    # print(script_files)

    # 脚本txt转quarto用的md

    # 记录文件名，后面用来写"_quarto.yml"
    md_file_list = []

    for script_path in script_files:
        md_content = script_to_md(script_path)

        md_filename = change_file_extension_to_filename_only(script_path, "md")

        md_file_list.append(md_filename)

        full_path = Path(quarto_dir, md_filename)

        with open(full_path, "w", encoding="utf-8") as f:
            f.write(md_content)
            print("Writed:", full_path)

    # 从模板填充_quarto.yml
    current_dir = os.path.dirname(__file__)
    template_path = os.path.join(current_dir, "quarto_template.yml")

    with open(template_path, "r") as f:
        template = f.read()

    today = datetime.datetime.today()

    file_list_str = "\n    - ".join(md_file_list)
    file_list_str = "- " + file_list_str

    quarto_yml = template.format(
        date=today.strftime("%Y-%m-%d"), file_list=file_list_str
    )

    # 写入_quarto.yml
    with open(Path(quarto_dir, "_quarto.yml"), "w", encoding="utf-8") as f:
        f.write(quarto_yml)

if __name__ == "__main__":
    conver_all_scripts()
