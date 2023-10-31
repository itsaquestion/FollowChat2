from src.web_tools.get_page import get_page
from bs4 import BeautifulSoup
import pandas as pd

def get_wsj_headlines():

    page_source = get_page('https://www.wsj.com')
    
    print('分析页面')
    # 使用 BeautifulSoup 解析页面源代码
    soup = BeautifulSoup(page_source, 'html.parser')

    # 初始化一个空列表来存储结果
    articles_data = []

    # 遍历所有的 <article> 标签
    for article in soup.find_all('article'):
        # 查找每个 <article> 下的第一个 <h3> 标签
        h3_tag = article.find('h3')
        
        # 查找 <h3> 下的第一个 <a> 标签
        a_tag = h3_tag.find('a') if h3_tag else None

        if h3_tag and a_tag:
            # 获取 <h3> 标签的文本内容
            h3_text = h3_tag.text

            # 获取 <a> 标签的 href 属性，即链接
            a_href = a_tag['href']

            # 将结果存储为一个字典，并添加到列表中
            articles_data.append({'title': h3_text, 'link': a_href})

    if len(articles_data) == 0:
        return None
    
    return pd.DataFrame(articles_data)

if __name__ == "__main__":
    df = get_wsj_headlines()
    print(df.head())