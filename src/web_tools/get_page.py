from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


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

def get_page(url, hub_url = "http://localhost:4444/wd/hub"):
    driver = connect(hub_url)

    print("获取页面: " + url)
    driver.get(url)

    page_source = driver.page_source
    
    print('退出chrome')
    driver.quit()
    
    return page_source