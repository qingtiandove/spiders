#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#-------------------------------------------------------------------------
#   程序：comments_youku.py
#   版本：0.1
#   作者：418769227@qq.com
#   日期：2017/07/13
#   语言：Python 3.5.x
#   操作：
#   功能： 爬取优酷网视频播放页评论
#
#
#-------------------------------------------------------------------------
import requests
import json

def get_comments(url):
    headers = {"Host": "p.comments.youku.com",
               "Connection": "keep-alive",
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
               "Accept": "*/*",
               "Referer": "http://v.youku.com/v_show/id_XMjg4NzAwNzU3Ng==.html?spm=a2hww.20023042.m_223465.5~5~5~5~5!2~5~5~A",
               "Accept-Encoding": "gzip, deflate",
               "Accept-Language": "zh-CN,zh;q=0.8"}
    html=requests.get(url,headers=headers,timeout=20)
    #结果为不标准json，需处理
    manage_html=html.text.strip('\r\nn_commentList(').strip(')')
    #字符串转json数据
    json_1=json.loads(manage_html)
    #提取评论
    content=json_1.get('data')['comment'][0].get('content')
    return content

if __name__=="__main__":
    #网址为任意一优酷视频播放页
    url='http://p.comments.youku.com/ycp/comment/pc/commentList?jsoncallback=n_commentList&app=100-DDwODVkv&objectId=721751894&objectType=1&listType=0&currentPage=1&pageSize=30&sign=840d7edaa2fed0dab0af25f4e7a70bb2&time=1499927397'
    comments=get_comments(url)
    print(comments)

#-------------------测试结果-------------------------------
#评论翻页，在网址page加数字即可
#