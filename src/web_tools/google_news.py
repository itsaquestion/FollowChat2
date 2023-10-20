from GoogleNews import GoogleNews
import pandas as pd

from functools import partial


def get_news_from_media(keywords, media):
    """从指定媒体抓取新闻

    >>> len(get_news_from_media('tech news','BBC')) > 0
    True
    >>> len(get_news_from_media('tech news','Reuters')) > 0
    True
    """
    googlenews = GoogleNews(period='2d')

    googlenews.search(media + ' ' + keywords)

    df = pd.DataFrame(googlenews.results())

    if (len(df) == 0):
        raise "没数据，可能刷新太多了"

    # print(df[['date','title','media','link']].query(f'media.str.contains("{media}")'))

    query_str = (
        'date.str.contains("hours") and '
        f'media.str.contains("{media}") and '
        '(not link.str.contains("video|podcasts|livecoverage"))'
    )
    columns_to_select = ['date', 'datetime', 'title', 'link']

    result = df.query(query_str)[columns_to_select]

    return result


get_news_bbc = partial(get_news_from_media, media='BBC')

get_news_reuters = partial(get_news_from_media, media='Reuters')

get_news_wsj = partial(get_news_from_media, media='Wall Street Journal')

get_news_scmp = partial(
    get_news_from_media, media='South China Morning Post')

get_news_econ = partial(get_news_from_media, media='The Economist')

def pick_news():

    keywords = ['tech', 'business', 'China']

    result = []

    for k in keywords:
        k += ' news'

        result += [get_news_reuters(k).head(1),
                   get_news_bbc(k).head(1),
                   get_news_scmp(k).head(1)
                   ]

    return pd.concat(result).drop_duplicates(subset='title', keep='first')


if __name__ == "__main__":
    print(get_news_scmp('news').head())
    # print(get_news_scmp('tech news').head())

    # print(pick_news())