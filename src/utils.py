import re

def sanitize_filename(filename):
    # 替换Windows和Linux中都不允许的字符
    sanitized = re.sub(r'[\\/:*?"<>|]', '_', filename)
    
    # 检查文件名长度
    if len(sanitized) > 255:
        raise ValueError("Filename too long")
    
    return sanitized