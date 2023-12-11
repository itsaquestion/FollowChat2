# %%
from src.dialogue_script_processor.script_to_md import conver_all_scripts
from src.gen_album import gen_album
from src.news import get_headlines_reuters
from src.build_and_deploy import build_web
from src.uploader import upload_all

news_info = get_headlines_reuters()

news_info = news_info.head(5)

print(news_info)

# %%
if news_info is not None:
    urls = news_info['url']
    print(urls)
    
    gen_album(urls)

    conver_all_scripts()
    
    build_web()

    upload_all()