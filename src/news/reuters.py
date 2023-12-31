# %%
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

import pandas as pd
import requests

from readability import Document

from bs4.element import Comment
from bs4 import BeautifulSoup

import time
import random


def make_chrome_options():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("window-size=1920,1080")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
    )
    chrome_options.add_argument("--allow-running-insecure-content")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--enable-chrome-browser-cloud-management")

    # 创建 WebDriver 实例，并应用设置
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)

    return chrome_options


def init_chrome():
    driver = webdriver.Remote(options=make_chrome_options(),command_executor='http://127.0.0.1:4444/wd/hub')
    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )
    return driver


def get_headlines_reuters():
    driver = init_chrome()

    driver.get("https://www.reuters.com/")

    # 找到所有具有特定data-testid的<a>元素
    elements = driver.find_elements(By.XPATH, '//a[@data-testid="Heading"]')

    time.sleep(random.randrange(2,4))
    # 初始化数据存储列表
    data = []

    # 遍历元素，提取标题和URL
    for element in elements:
        title = element.text
        url = element.get_attribute("href")
        data.append({"title": title, "url": url})

    # 创建DataFrame
    df = pd.DataFrame(data).query('url != "None"')

    driver.quit()
    return df


# print(get_headlines_reuters().head())


def get_page_html(url):
    driver = init_chrome()

    try:
        # 加载网页
        driver.get(url)
        
        time.sleep(random.randrange(2,4))
        
        # 获取网页的HTML内容
        html = driver.page_source

        return html
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        # 关闭WebDriver
        driver.quit()


def extract_text_content(url):
    response = requests.get(url)
    doc = Document(response.text)
    return doc.summary(html_partial=False)


def tag_visible(element):
    if element.parent.name in [
        "style",
        "script",
        "head",
        "title",
        "meta",
        "[document]",
    ]:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(body):
    soup = BeautifulSoup(body, "html.parser")
    texts = soup.findAll(string=True)
    visible_texts = filter(tag_visible, texts)
    return " ".join(t.strip() for t in visible_texts)


def get_news_content_reuters(url):
    content = get_article_text(get_page_html(url))
    return content.split("Our Standards:")[0]

def get_article_text(page_source):
    soup = BeautifulSoup(page_source, 'html.parser')
    article = soup.find("article")
    title = soup.find("title").text
    doc = Document(str(article))
    text = text_from_html(doc.summary(html_partial=False))
    return f"Title: {title}\n\n{text}"

# %%
if __name__ == "__main__":

    # 使用函数
    url = "https://www.reuters.com/world/global-2024-staple-food-supplies-be-strained-by-dry-weather-export-curbs-2023-12-26/"
    
    text = get_news_content_reuters(url)
    print(text)
