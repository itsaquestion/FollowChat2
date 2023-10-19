"""
抓取BBC News,Reuters和南华早报的网页内容
"""
from bs4 import BeautifulSoup
import requests
import functools


def get_news_content(url):
    """
    通过网址，返回BBC News或者Reuters的内容

    Args:
        url: BBC News或者Reuters的网址

    Returns:
        一个字典，{'title': title, 'url': url,'content': text}

    >>> res = get('https://www.bbc.com/news/business-67118263')
    >>> res['title'][0]
    'N'
    >>> len(res['content']) > 0
    True

    >>> res = get('https://www.reuters.com/business/country-gardens-entire-offshore-debt-be-default-if-tuesday-payment-not-made-2023-10-16/')
    >>> res['title'][0]
    'C'
    >>> len(res['content']) > 0
    True

    >>> res = get('https://www.scmp.com/news/china/diplomacy/article/3238360/belt-and-road-forum-china-launches-ai-framework-urging-equal-rights-and-opportunities-all-nations')
    >>> res['title'][0]
    'B'
    >>> len(res['content']) > 0
    True
    """

    # 获取网页内容
    # url = 'https://www.bbc.com/news/business-67118263'

    response = requests.get(url)
    html_content = response.text

    # 使用BeautifulSoup解析HTML内容
    soup = BeautifulSoup(html_content, 'html.parser')
    title = soup.title.string

    # 查找所有<article>标签
    article = soup.find_all('article')[0]

    # 遍历并处理每一个<div>标签

    text = ''

    for div in article.find_all('p'):
        text += div.text + '\n\n'

    text = text.strip()

    return {'title': title,
            # 'url': url,
            'content': text}


if __name__ == "__main__":
    print(get_news_content('https://www.scmp.com/news/china/diplomacy/article/3238360/belt-and-road-forum-china-launches-ai-framework-urging-equal-rights-and-opportunities-all-nations'))
