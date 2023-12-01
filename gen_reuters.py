from src.gen_album import gen_album
from src.web_tools import google_news
from src.dialogue_script_processor.script_to_md import conver_all_scripts
from src.build_and_deploy import build_web
from src.uploader import upload_all

if __name__ == '__main__':
    
    news_info = google_news.get_news_reuters('').head(2)[['title', 'link']]

    print(news_info)
    
    if news_info is not None:
        urls = news_info['link']
        
        gen_album(urls)

        conver_all_scripts()
        
        build_web()

        upload_all()

