#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#-------------------------------------------------------------------------
#   程序：get_mac_location.py
#   版本：0.1
#   作者：418769227@qq.com
#   日期：2017/07/17
#   语言：Python 3.5.x
#   操作：
#   功能：爬取网站http://api.cellocation.com/rewifi.html，输入经纬度，获得附近的mac地址
#
#-------------------------------------------------------------------------
import requests
import json

#输入经纬度
def get_mac(lon,lat):
    headers={'Accept':'*/*',
             'Accept-Encoding':'gzip, deflate',
             'Accept-Language':'zh-CN,zh;q=0.8',
             'Referer':'http://api.cellocation.com/rewifi.html',
             'Host':'api.cellocation.com',
             'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
             }
    parameter={'incoord':'gcj02',
               'coord':'gcj02',
               'lat':lat,
               'lon':lon}
    rep=requests.get(url,headers=headers,params=parameter,timeout=20)
    #数据json
    mac_json=json.loads(rep.text)
    mac=mac_json[0].get('mac')
    print(mac)
    return mac

if __name__=="__main__":
    url='http://api.cellocation.com/rewifi'
    lon='118.742694'  #经度
    lat='39.996518'  #维度
    mac=get_mac(lon,lat)
#-------------------测试结果-------------------------------
#查看网页源代码，有查询次数限制及其他限制
#
#
#
