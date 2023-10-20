from src.gen_album import gen_album
from src.web_tools import google_news

if __name__ == '__main__':
    
    news_info = google_news.get_news_scmp('').head(5)[['title', 'link']]

    urls = news_info['link']
    
    gen_album(urls,'scmp')


