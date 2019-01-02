#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#-------------------------------------------------------------------------
#   程序：url_qqvideo.py
#   版本：0.1
#   作者：418769227@qq.com
#   日期：2017/07/13
#   语言：Python 3.5.x
#   操作：
#   功能：	爬取腾讯视频播放链接
#
#-------------------------------------------------------------------------
import time
import re
from selenium import webdriver

#腾讯视频防爬，检测是否js解析能力
def url_qqvideo(url):
    # phantomjs绝对路径
    phantomjs_driver = 'C:/Users/41876/Desktop/cookis/phantomjs-2.1.1-windows/bin/phantomjs'
    driver = webdriver.PhantomJS(executable_path=phantomjs_driver)
    driver.get(url)
    time.sleep(1)
    #正则匹配网址
    content=re.findall('https://imgcache.qq.com/tencentvideo_v1/.*=0', driver.page_source)
    print(content)


if __name__=="__main__":
    #位任意一腾讯视频播放网页
    url="https://v.qq.com/x/cover/dhzimk1qzznf301.html"
    url_qqvideo(url)


#-------------------测试结果-------------------------------
#当信息类别少或者特征明显时，使用正则表达式更加高效，例如网址
# 'https://imgcache.qq.com/tencentvideo_v1/playerv3/TPout.swf?max_age=86400&amp;v=20161117&amp;vid=l0024si3r7q&amp;auto=0'
#