from selenium import webdriver
# 初始化浏览器驱动
driver = webdriver.Chrome()
# 打开网页
driver.get("https://elicit.com/notebook/ff06e965-e962-4800-a658-2aa2d510c2c8")
# 获取浏览器Cookies
cookies = driver.get_cookies()
# 打印Cookies
for cookie in cookies:
    print(cookie)