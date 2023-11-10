from src.gen_album import gen_album
from src.web_tools import google_news
from icecream import ic
from src.web_tools.wsj_headlines import get_wsj_headlines
from src.dialogue_script_processor.script_to_md import conver_all_scripts
from src.build_and_deploy import build_and_deploy

if __name__ == '__main__':
    
    news_info = get_wsj_headlines()

    print(news_info)
    
    if news_info is not None:
        urls = news_info.head(5)['link']
        
        gen_album(urls)
        
        conver_all_scripts()
        
        build_and_deploy()