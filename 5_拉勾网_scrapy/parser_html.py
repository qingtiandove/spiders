import re
from bs4 import BeautifulSoup
import json
from datetime import datetime

class ParserHtml():
    def parser_first(self,html_cont):
        soup=BeautifulSoup(html_cont,'html.parser')
        zhaopin_a = soup.find_all('a', href=re.compile(r'www.lagou.com/zhaopin/.*/'))
        print(len(zhaopin_a))  #316
        href_zhaopin = []
        for zhaopin in zhaopin_a:
            href = zhaopin.get('href')
            href_zhaopin.append(href)
        return href_zhaopin

    def parser_shouye(self,html_cont):
        soup=BeautifulSoup(html_cont, 'html.parser')
        page_num = soup.find('a', id="tab_pos").span.text.replace('+', '')

        new_urls_jobs=self.get_job_urls(soup)
        new_urls_comp=self.get_comp_urls(soup)
        return new_urls_jobs,new_urls_comp,page_num

    def get_job_urls(self,soup):
        jobs_a = soup.find_all('a', class_="position_link")
        new_urls_jobs = set()
        for job in jobs_a:
            job_url = job.get('href')
            new_urls_jobs.add(job_url)
        return new_urls_jobs

    def get_comp_urls(self,soup):
        comp_a = soup.find_all('div', class_="company_name")
        new_urls_comp = set()
        for comp in comp_a:
            comp_urls = comp.a.get('href')
            new_urls_comp.add(comp_urls)
        return new_urls_comp

    def paser_job(self,url_job,html_cont):
        soup=BeautifulSoup(html_cont,'html.parser')
        data_job={}
        if soup.find(id="jobid") is None:
            return None
        data_job['id_jobs']=soup.find(id="jobid").get('value')
        data_job['name_job'] = soup.find('span', class_='ceil-job').get_text().replace('/', '')
        data_job['salary'] = soup.find('span', class_="ceil-salary").get_text()

        request_job = soup.find('dd', class_="job_request")
        p_ = request_job.p
        for span in p_:
            if span != "\n":
                text = span.get_text().replace('/', '')
                if '经验' in text:
                    data_job['year_required'] = text.replace('经验', '')
                if '及' in text:
                    data_job['edu_required'] = text
                if '职' in text:
                    data_job['type_work'] = text
        position_label = soup.find('ul', class_="position-label clearfix").find_all('li')
        label = ''
        for li in position_label:
            label+=li.get_text()
        data_job['label']=label
        publish_time = soup.find('p', class_="publish_time").get_text().split('&')[0]
        if '2017' not in publish_time:
            publish_time = datetime.now().strftime('%Y-%m-%d')
        else:
            publish_time = publish_time.replace(' 发布于拉勾网', '').strip()
        data_job['publish_time']=publish_time
        data_job['job_advantage'] = soup.find('dd', class_="job-advantage").get_text().replace(' ', '')
        data_job['description'] = soup.find('dd', class_="job_bt").get_text().replace(' ', '')
        data_job['work_addr'] = soup.find('div', class_="work_addr").get_text().replace(' ', '').replace('查看地图\n', '')

        pos = soup.find_all('input', type="hidden")
        for po in pos:
            if po.get('name') == "positionLng":
                positionLng = po.get('value')
            else:
                positionLng=0
            if po.get('name') == "positionLat":
                positionLat = po.get('value')
            else:
                positionLat=0
        data_job['postion']="{},{}".format(positionLng,positionLat)
        data_job['comp_name'] = soup.find('dl', class_="job_company").find('img').get('alt')
        com_url=soup.find('dl', class_="job_company").find('a').get('href')
        con_re=re.compile(r'/(\d+).')
        data_job['comp_id'] = con_re.search(com_url).group(1)
        data_job['url_job']=url_job
        data_job['time_spider'] = datetime.now()
        return data_job

    def parser_comp(self,url_comp,html_cont):
        soup = BeautifulSoup(html_cont, 'html.parser')
        data_comp={}
        try:
            script_info = soup.find('script', id="companyInfoData").text
        except Exception as e:
            print(e)
            #print(html_cont)
        info_com = json.loads(script_info)

        coreinfo = info_com.get('coreInfo')

        data_comp['companyId'] = coreinfo.get('companyId')
        data_comp['companyName'] = coreinfo.get('companyName')
        data_comp['companyShortName'] = coreinfo.get('companyShortName')
        data_comp['companyIntroduce'] = coreinfo.get('companyIntroduce')
        data_comp['companyUrl'] = coreinfo.get('companyUrl')
        labels=''
        labels_comp=info_com.get('labels')
        for lab in labels_comp:
            labels+=lab
            labels+=','

        data_comp['labels'] = labels
        data_comp['companyProfile'] = info_com.get('introduction').get('companyProfile')

        baseInfo = info_com.get('baseInfo')

        data_comp['financeStage'] = baseInfo.get('financeStage')
        data_comp['city'] = baseInfo.get('city')
        data_comp['companySize'] = baseInfo.get('companySize')
        data_comp['industryField'] = baseInfo.get('industryField')
        data_comp['url_lagou'] = url_comp
        data_comp['time_spider']=datetime.now()

        leaders = info_com.get('leaders')
        data_leader_list=self.get_leaders(leaders)

        address_list = info_com.get('addressList')
        data_address_list=self.get_address(address_list)

        return data_comp,data_leader_list,data_address_list

    def get_leaders(self,leaders):
        data_leader_list=[]
        for leader in leaders:
            data_leader = {}
            data_leader['name'] = leader.get('name')
            data_leader['remark'] = leader.get('remark')
            data_leader['position'] = leader.get('position')
            data_leader['weibo'] = leader.get('weibo')
            data_leader['cyclopediaUrl'] = leader.get('cyclopediaUrl')
            data_leader['companyid'] = leader.get('companyid')
            data_leader['time_spider'] = datetime.now()
            data_leader_list.append(data_leader)
        return data_leader_list

    def get_address(self,address_list):
        data_address_list=[]
        # 地址列表为空的情况
        if address_list is None:
            return None
        for address in address_list:
            data_address = {}
            data_address['province'] = address.get('province')
            data_address['city'] = address.get('city')
            data_address['district'] = address.get('district')
            data_address['businessArea'] = address.get('businessArea')
            data_address['detailAddress'] = address.get('detailAddress')
            data_address['lat'] = address.get('lat')
            data_address['lng'] = address.get('lng')
            data_address['companyId'] = address.get('companyId')
            data_address['time_spider'] = datetime.now()
            data_address_list.append(data_address)
        return data_address_list