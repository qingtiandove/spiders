#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#-------------------------------------------------------------------------
#   程序：comments_qqvideo.py
#   版本：0.1
#   作者：418769227@qq.com
#   日期：2017/07/17
#   语言：Python 3.5.x
#   操作：
#   功能：抓取腾讯视频播放页，评论
#
#-------------------------------------------------------------------------
import requests
import json

#找出特定请求，模拟发送
def get_comments(url):
    headers={'accept':'*/*',
             'accept-encoding':'gzip, deflate, br',
             'accept-language':'zh-CN,zh;q=0.8',
             'referer':'https://v.qq.com/txyp/coralComment_yp_1.0.htm',
             'host':'coral.qq.com',
             'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
    }
    rep=requests.get(url,headers=headers,timeout=20)
    manage_html=rep.text.strip('\r\njQuery112406957335427885001_1500256541686(').strip(')')
    #字符串转json数据
    json_1=json.loads(manage_html)
    #提取评论
    content=json_1.get('data')['commentid'][0].get('content')
    return content

if __name__=="__main__":
    url = "https://coral.qq.com/article/1970987440/comment?commentid=0&reqnum=10&tag=&callback=jQuery112406957335427885001_1500256541686&_=1500256541687"
    comments=get_comments(url)
    print(comments)
#-------------------测试结果-------------------------------
#开启fiddle4，会报错（原因更改了端口）
# requests.exceptions.SSLError: ("bad handshake: Error([('SSL routines', 'ssl3_get_server_certificate', 'certificate verify failed')],)",)
#
#
#
