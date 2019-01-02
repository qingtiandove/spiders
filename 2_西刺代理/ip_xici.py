#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#-------------------------------------------------------------------------
#   程序：ip_xici.py
#   版本：0.1
#   作者：418769227@qq.com
#   日期：2017/07/13
#   语言：Python 3.5.x
#   操作：
#   功能：爬取西刺代理，免费国内高匿代理
#
#-------------------------------------------------------------------------
import time
from bs4 import BeautifulSoup
from selenium import webdriver

#西刺代理（防爬策略，检测有无js能力）
def ip_xici(url):
    #phantomjs绝对路径
    phantomjs_driver = 'C:/Users/41876/Desktop/cookis/phantomjs-2.1.1-windows/bin/phantomjs'
    driver = webdriver.PhantomJS(executable_path=phantomjs_driver)
    driver.get(url)
    time.sleep(3)
    bs0bj = BeautifulSoup(driver.page_source, "html.parser")
    name = bs0bj.findAll('tr')
    #每页100数据
    for list in name[1:100]:
        #定位
        ip = list('td')[1].get_text()
        duan = list('td')[2].get_text()
        print(ip+":"+duan)

if __name__=="__main__":
    url="http://www.xicidaili.com/nn/"
    ip_xici(url)

#-------------------测试结果-------------------------------
#翻页修改url
#27.28.84.178:8118
#115.53.103.71:808
#150.255.184.202:808
