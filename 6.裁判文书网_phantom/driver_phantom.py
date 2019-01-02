import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
#从USER_AGENTS列表中随机选一个浏览器头，伪装浏览器
desired_capabilities["phantomjs.page.settings.userAgent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko\
) Chrome/55.0.2883.87 Safari/537.36"
desired_capabilities["phantomjs.page.settings.loadImages"] = False
driver=webdriver.PhantomJS()
# 隐式等待5秒，可以自己调节
driver.implicitly_wait(5)
# 以前遇到过driver.get(url)一直不返回，但也不报错的问题，这时程序会卡住，设置超时选项能解决这个问题。
driver.set_page_load_timeout(5)
# 设置10秒脚本超时时间
driver.set_script_timeout(5)
driver.maximize_window()
driver.capabilities['applicationCacheEnabled']=True
driver.capabilities["browserName"] = 'chrome'

#print('phantomjs正在启动...')