from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd


def connect(hub_url = "http://localhost:4444/wd/hub", do_test=False):
    
    # 配置 Chrome 浏览器选项
    chrome_options = Options()

    chrome_options.add_argument("--blink-settings=imagesEnabled=false")
    
    print('连接到selenium')
    # 使用 Remote WebDriver 连接到 Selenium Grid
    driver = webdriver.Remote(
        command_executor=hub_url,
        options=chrome_options
    )
    
    if do_test:
        print('测试google')
        try:
            # 打开 Google 主页
            driver.get("https://www.google.com")
            
            # 检查标题是否为 “Google”
            assert "Google" in driver.title
        
            print("Test Passed")
            # close_all_tabs(driver)
            return driver
        
        except Exception as e:
            print(f"Test Failed: {e}")
            
            return None
        
    return driver

def close_all_tabs(driver):
    print('关闭所有tab')
    for handle in driver.window_handles:
        driver.switch_to.window(handle)
        driver.close()

def get_wsj_headlines(hub_url = "http://localhost:4444/wd/hub"):

    driver = connect(hub_url)

    print('获取wsj首页')
    driver.get('https://www.wsj.com/')

    page_source = driver.page_source
    
    print('退出chrome，分析页面')
    driver.quit()
    
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