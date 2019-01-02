import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import json
from url_manager import UrlManager
from downloader_html import Lagou_downloader
from  parser_html import ParserHtml
from data_base import DataOutput

def add_to_redis(key,urls):
    for url in urls:
        redis_lagou.sadd(key,url)

class SpiderMan(object):
    def __init__(self):
        self.manager=UrlManager()
        self.downloader=Lagou_downloader()
        self.parser=ParserHtml()
        self.output=DataOutput()

    def get_all_urls(self):
        self.manager.read_redis(redis_lagou)
        spider_urls=redis_lagou.smembers('spidered')
        for zhao_url in self.manager.zhaopin_urls:
            if zhao_url not in spider_urls:
                html = self.downloader.download(zhao_url)
                new_urls_jobs, new_urls_comp,page_num = self.parser.parser_shouye(html)
                add_to_redis('jobs',new_urls_jobs)
                add_to_redis('comp',new_urls_comp)
                if page_num==500:
                    for i in range(2,31):
                        zhao_url_2='{}{}/'.format(zhao_url,i)
                        html=self.downloader.download(zhao_url_2)
                        if not html:
                            continue
                        new_urls_jobs, new_urls_comp,page_ = self.parser.parser_shouye(html)
                        add_to_redis('jobs', new_urls_jobs)
                        add_to_redis('comp', new_urls_comp)
                else:
                    for i in range(2,int(page_num)//15+2):
                        zhao_url_2 = '{}{}/'.format(zhao_url,i)
                        html = self.downloader.download(zhao_url_2)
                        if not html:
                            continue
                        new_urls_jobs, new_urls_comp,page_= self.parser.parser_shouye(html)
                        add_to_redis('jobs', new_urls_jobs)
                        add_to_redis('comp', new_urls_comp)
            redis_lagou.sadd('spidered',zhao_url)

    def crawl(self):
        save_data=10 # 10个网址存储一次
        jobs_urls=redis_lagou.smembers('jobs')
        comps_urls=redis_lagou.smembers('comp')
        zong_urls=jobs_urls | comps_urls

        old_urls=self.output.select_spidered_urls()
        add_to_redis('old_urls', old_urls)
        #筛选已经爬取的网址
        zong_urls=list(set(zong_urls).difference(set(old_urls)))

        print('待爬取网址数：{}'.format(len(zong_urls)))
        print('已爬取网址数：{}'.format(len(old_urls)))

        self.manager.add_new_urls(zong_urls)
        try:
            num_spider=0
            while num_spider<=save_data and self.manager.has_new_url():
                new_url=self.manager.get_new_url()
                html=self.downloader.download(new_url)
                if not html:
                    continue
                #print(new_url)
                if 'jobs' in new_url:
                    data_job=self.parser.paser_job(new_url,html)
                    self.output.store_data_job(data_job)

                elif 'gongsi' in new_url:
                    data_comp, data_leader_list, data_address_list=self.parser.parser_comp(new_url,html)
                    self.output.store_data_comp(data_comp)
                    self.output.store_data_leader(data_leader_list)
                    self.output.store_data_address(data_address_list)
                if num_spider==save_data-1:
                    num_spider=0
                    self.output.output_job()
                    self.output.output_comp()
                    self.output.output_address()
                    self.output.output_leaders()
                    self.output.clear_data()
                else:
                    num_spider+=1

        finally:
            new_urls=self.manager.new_urls
            old_urls=self.manager.old_urls
            add_to_redis('new_urls', new_urls)
            add_to_redis('old_urls',old_urls)

            self.output.close_data()


if __name__ == '__main__':
    # 同一账号，不能同时访问
    import redis
    import time
    redis_lagou = redis.Redis(host='127.0.0.1', port=6379, db=1, decode_responses=True)

    url = 'https://www.lagou.com/zhaopin/Python/?labelWords=label'
    spider_man = SpiderMan()
    #爬取次级页面的job，comp信息
    while True:
        try:
            spider_man.get_all_urls()
            # 爬取职位，公司页面的具体信息
            spider_man.crawl()
        except Exception as e:
            print(e)
            time.sleep(120)
            print('尝试重新启动。')