#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#-------------------------------------------------------------------------
#   程序：youku_url.py
#   版本：0.1
#   作者：418769227@qq.com
#   日期：2017/07/13
#   语言：Python 3.5.x
#   操作：python read_useragent_txt_forge.py
#   功能：	爬取优酷网视频播放链接,及页面评论
#         读取一个随机的头部User-Agent 信息 添加到请求中此作为基础的伪造,
#
#-------------------------------------------------------------------------
import random
import requests
import re

#仿造请求头，请求网页
def get_url_video(url,user_agent):
    if len(user_agent)<10:
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko\
) Chrome/55.0.2883.87 Safari/537.36"
        #3a2c2h1u
    headers={"Connection": "keep-alive",
             "Host":"v.youku.com",
             "User - Agent":user_agent,
             "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
             "Accept - Encoding":"gzip, deflate",
             "Accept-Language":"zh-CN,zh;q=0.8",
             'Cache-Control': 'no-cache',
             "Referer":"http://www.youku.com/"
             }
    try:
        html=requests.get(url,headers=headers,timeout=20).text
        return html
    except Exception as e:
        print(e)
        return -1

if __name__=="__main__":
    #url为任意一优酷视频播放页面
    url='http://v.youku.com/v_show/id_XMjg4NzAwNzU3Ng==.html?spm=a2hww.20023042.m_223465.5~5~5~5~5!2~5~5~A#paction'
    #读取txt，获得user_agent列表
    user_agent_list=[]
    f=open('user_agent.txt', 'r')
    for text_line in f:
        user_agent_list.append(text_line.replace("\n",""))
    user_agent=random.choice(user_agent_list)

    html_body=get_url_video(url,user_agent)
    #正则——[A-Za-z0-9=]*
    print(re.findall('http://player.youku.com/player.php/sid/[A-Za-z0-9=]*/v.swf',html_body))


#-------------------测试结果-------------------------------
# 存在问题——————抓取的链接并不能播放
#[
# http://player.youku.com/player.php/sid/XMjg4NzAwNzU3Ng==/v.swf
# http://player.youku.com/player.php/sid/XMjg4NzAwNzU3Ng==/v.swf'
#]
