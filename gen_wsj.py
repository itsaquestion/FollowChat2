from src.gen_album import gen_album
from src.web_tools import google_news
from icecream import ic

if __name__ == '__main__':
    
    news_info = google_news.get_news_wsj('-livecoverage -"Head Topics"').head(5)[['title', 'link']]

    ic(news_info)
    
    urls = news_info['link']
    
    gen_album(urls,'wsj')
    