from src.gen_album import gen_album
from src.web_tools import google_news
from icecream import ic
from src.web_tools.wsj_headlines import get_wsj_headlines

if __name__ == '__main__':
    
    news_info = get_wsj_headlines()

    ic(news_info)
    
    if news_info is not None:
        urls = news_info.head(2)['link']
        
        gen_album(urls)
        