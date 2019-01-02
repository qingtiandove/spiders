import requests
from bs4 import BeautifulSoup
from driver_phantom import driver
import time
headers = {'Accept': '*/*',
           'Accept-Encoding': 'gzip, deflate',
           'Accept-Language': 'zh-CN,zh;q=0.8',
           'Connection': 'keep-alive',
           'Host': 'www.ajxxgk.jcy.gov.cn',
           'Referer': 'http://www.ajxxgk.jcy.gov.cn/html/zjxflws/index.html',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
           }
url='http://www.ajxxgk.jcy.gov.cn/html/zjxflws/index.html'
def get_js_cook(url):
    rep=requests.get(url,headers=headers)
    cookie=rep.cookies
    __jsluid=cookie.get('__jsluid')
    html=rep.text

    return __jsluid,html

def parser_html(html):
    soup=BeautifulSoup(html,'html.parser')
    js_text=soup.find('script').text

    return js_text

def parser_js_1(js_text):
    js_text=js_text.replace(';eval',""";var out=document.getElementById('new2');out.innerText=""")
    wirte_js(js_text,'run_js_1')

def wirte_js(js_text,name):
    with open('./js&html/{}.js'.format(name),'w',encoding='utf-8') as f:
        f.write(js_text)

def get_js_2():
    driver.get('./js&html/run_js_1.html')
    time.sleep(0.5)
    js_text = driver.find_element_by_id('new2').text
    return js_text

def parser_js_2(js_text):
    js_text=js_text.replace(r"""while(window._phantom||window.__phantomas){};""",'')
    js_text=js_text.replace(';setTimeout',r""";var out=document.getElementById('new2');out.innerText=dc;setTimeout""")
    js_text=js_text.replace('h.firstChild.href','\"http://www.ajxxgk.jcy.gov.cn/\"')
    wirte_js(js_text,'run_js_2')

def get_jsl():
    driver.get('./js&html/run_js_2.html')
    time.sleep(0.5)
    __jsl_clearance = driver.find_element_by_id('new2').text.replace('__jsl_clearance=','')

    return __jsl_clearance


def main():
    __jsluid,html=get_js_cook(url)
    js_text=parser_html(html)
    parser_js_1(js_text)
    #第二次
    js_text=get_js_2()
    parser_js_2(js_text)
    __jsl_clearance=get_jsl()

    cookies = {'__jsl_clearance': __jsl_clearance,
               '__jsluid': __jsluid,
               'sYQDUGqqzHpid': 'page_0',
               'sYQDUGqqzHtid': 'tab_0'}

    return cookies
if __name__ == '__main__':

    main()