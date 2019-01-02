import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime

def get_cookie(cookie_name):
    txt_name = '{}.txt'.format(cookie_name)
    cookies = {}
    with open(txt_name, 'r') as f:
        cooke = f.readlines()
    cookie = cooke[0]
    cookie = cookie.split(';')
    for cook in cookie:
        name1, name2 = cook.split('=')
        cookies[name1] = name2
    return cookies

def get_404(html):
    soup=BeautifulSoup(html,'html.parser')
    title=soup.find('title').text
    if '404' in title:
        return False
    return  True


class Lagou_downloader():
    def __init__(self):
        self.down_num=0
        self.cookie_name='cookie'
        self.cookies=get_cookie(self.cookie_name)

    def download(self, url):
        if url is None:
            return None
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
Chrome/59.0.3071.115 Safari/537.36'
        headers = {"User-Agent": user_agent}
        r = requests.get(url, headers=headers,cookies=self.cookies)

        time.sleep(1)
        #todo
        if r.history:
            print("访问被重定向,尝试更换cookie")
            if self.cookie_name=='cookie_2':
                print('访问被重定向：{}'.format(url))
                print(datetime.now())
                #exit()
            else:
                self.cookie_name='cookie_2'
                self.cookies=get_cookie(self.cookie_name)
                self.download(url)
        if r.status_code == 200:
            if not get_404(r.text):
                print('访问404：{}'.format(url))
                return None
            r.encoding = 'utf-8'
            self.down_num += 1
            print('第{}成功访问：{}'.format(self.down_num,url))
            return r.text
        return None


if __name__ == '__main__':
    import redis
    from datetime import datetime
    zhaopin_redis = redis.Redis(host='localhost', port=6379, db=1)
    import re
    url='https://www.lagou.com/jobs/3476891.html'
    test_1=Lagou_downloader()
    html=test_1.download(url)
    soup = BeautifulSoup(html, 'html.parser')
    publish_time = soup.find('p', class_="publish_time").get_text()
    if '2017' not in publish_time:
        publish_time = datetime.now().strftime('%Y-%m-%d')
    else:
        publish_time=publish_time.replace(' 发布于拉勾网','')


    print('结束')
