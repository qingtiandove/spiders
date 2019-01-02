import requests
import re
import time

from bs4 import BeautifulSoup

from get_cookie import main
from model import Document
from tets import app

# 过期时间，3天
from redis import Redis

conn = Redis(host='localhost', port=6379, db=5, password='**', decode_responses=True)

EXPIRE_TIME=60*60*24*3
headers = {'Accept': '*/*',
           'Accept-Encoding': 'gzip, deflate',
           'Accept-Language': 'zh-CN,zh;q=0.8',
           'Connection': 'keep-alive',
           'Host': 'www.ajxxgk.jcy.gov.cn',
           'Referer': 'http://www.ajxxgk.jcy.gov.cn/html/zjxflws/index.html',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
           }

def down_html(url,cookies):
    rep=requests.get(url,headers=headers,cookies=cookies)
    time.sleep(1)
    if rep.status_code == 200:
        html=rep.text
    else:
        html=None
    return html

def paser_list_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    contents = soup.find_all("div", class_="crow")
    for content in contents:
        content_dict={}
        court_xiang = content.find('div', class_='ajh')
        url_2 = court_xiang.a.attrs.get('href')
        pat = re.compile(r'/(\d+).html')
        id = pat.search(url_2).group(1)
        url = 'http://www.ajxxgk.jcy.gov.cn{}'.format(url_2)
        law = court_xiang.a.attrs.get('title')
        court = content.find('div', class_="ctitle").a.attrs.get('title')
        case_title = content.find('div', class_="ctitle").contents[3].attrs.get('title')
        occur_time = soup.find('div', class_='sj').text.strip()

        content_dict['id']=id
        content_dict['url'] = url
        content_dict['law'] = law
        content_dict['case_title'] = case_title
        content_dict['court'] = court
        content_dict['occur_time'] = occur_time

        if conn.sadd('id',id):
            conn.sadd('id_new',id)
            conn.hmset(id,content_dict)
            conn.expire(id,EXPIRE_TIME)
            print(id)

def parser_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    #pat = re.compile(r'（(.*)）')
    #case_title = soup.title.text
    #case_title_2 = pat.search(case_title).group(1)

    #court = soup.find(attrs={"name": "title"}).text
    # title_2=court.find(name='title')
    content = soup.find('div', class_="content")

    return content

@app.task
def main_list():
    cookies=main()
    start_time=time.time()
    for i in range(1,1000):
        if i==1:
            url = 'http://www.ajxxgk.jcy.gov.cn/html/zjxflws/index.html'
        else:
            url='http://www.ajxxgk.jcy.gov.cn/html/zjxflws/{}.html'.format(i)
        html=down_html(url,cookies)
        if not html:
            continue
        paser_list_html(html)
        print('page_num: {}'.format(i))

        end_time=time.time()

        if int(end_time-start_time) >=50*60:
            cookies=main()
            start_time=time.time()


@app.task()
def main_content():
    ids=conn.smembers('id_new')
    cookies=main()
    start_time=time.time()
    for i,id in enumerate(ids):
        content_dict=conn.hmget(id,['id','url','case_title','court','law','occur_time'])
        id=content_dict[0]
        url=content_dict[1]

        html=down_html(url,cookies)
        if not html:
            conn.delete(id)
            conn.srem('id_new', id)
            continue
        content_html=parser_content(html)

        try:
            Document.create(id=int(content_dict[0]),
                          url=content_dict[1],
                          case_title=content_dict[2],
                          court=content_dict[3],
                          law=content_dict[4],
                          content=content_html,
                          occur_time=content_dict[5],
                          )
            print('{}-已成功存入：{}'.format(i,url))
        except Exception as e:
            print(e)
            print('存入数据库出现错误！')
        finally:
            conn.delete(id)
            conn.srem('id_new', id)

        end_time=time.time()
        if int(end_time-start_time) >= 50*60:
            cookies=main()
            start_time=time.time()

if __name__ == '__main__':
    main_content()