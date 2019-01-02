import pymysql
from datetime import datetime

class DataOutput(object):
    def __init__(self):
        self.connection= pymysql.connect(host='localhost',
                                         port=3306,
                                         user='root',
                                         passwd='***',
                                         db='***',
                                         charset='utf8')
        self.cur = self.connection.cursor()
        self.cur.execute('USE la_gou_wang')
        self.datas_job=[]
        self.datas_comp=[]
        self.datas_leader=[]
        self.datas_address=[]

    def clear_data(self):
        self.datas_job = []
        self.datas_comp = []
        self.datas_leader = []
        self.datas_address = []

    def store_data_job(self,data_job):
        if data_job is None:
            return
        self.datas_job.append(data_job)

    def store_data_comp(self,data_comp):
        if data_comp is None:
            return
        self.datas_comp.append(data_comp)

    def store_data_leader(self,data_leader_list):
        if data_leader_list is None:
            return
        for data_leader in data_leader_list:
            self.datas_leader.append(data_leader)

    def store_data_address(self,data_address_list):
        if data_address_list is None:
            return
        for data_address in data_address_list:
            self.datas_address.append(data_address)

    def close_data(self):
        self.cur.close()
        self.connection.close()

    def output_url(self,spidered,urls):
        data_url_list=[]
        for url in urls:
            time_spider=datetime.now()
            if 'jobs' in url:
                data=(url,'jobs',spidered,time_spider)
            if 'gongsi' in url:
                data=(url,'gongsi',spidered,time_spider)
            data_url_list.append(data)
        self.cur.executemany("insert into url_manager ("
                             "url,"
                             "type,"
                             "spidered,"
                             "time_spider) values (%s,%s,%s,%s)",
                             data_url_list)
        self.cur.connection.commit()

    def output_job(self):
        data_job_list=[]
        for data_job in self.datas_job:
            data=(data_job.get('id_jobs'),
                  data_job.get('name_job'),
                  data_job.get('salary'),
                  data_job.get('year_required'),
                  data_job.get('edu_required'),
                  data_job.get('type_work'),
                  data_job.get('label'),
                  data_job.get('publish_time'),
                  data_job.get('job_advantage'),
                  data_job.get('description'),
                  data_job.get('work_addr'),
                  data_job.get('postion'),
                  data_job.get('comp_name'),
                  data_job.get('comp_id'),
                  data_job.get('url_job'),
                  data_job.get('time_spider'))
            data_job_list.append(data)
        try:
            self.cur.executemany("insert into jobs("
                                 "id_jobs,"
                                 "name_job,"
                                 "salary,"
                                 "year_required,"
                                 "edu_required,"
                                 "type_work,"
                                 "label,"
                                 "publish_time,"
                                 "job_advantage,"
                                 "description,"
                                 "work_addr,"
                                 "postion,"
                                 "comp_name,"
                                 "comp_id,"
                                 "url_job,"
                                 "time_spider) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                 data_job_list)
            self.cur.connection.commit()
        except Exception as e:
            print("储存数据出错：{}".format(e))

    def output_comp(self):
        data_comp_list=[]
        for data_comp in self.datas_comp:
            data=[data_comp['companyId'],
                  data_comp['companyName'],
                  data_comp['companyShortName'],
                  data_comp['companyIntroduce'],
                  data_comp['companyUrl'],
                  data_comp['labels'],
                  data_comp['companyProfile'],
                  data_comp['financeStage'],
                  data_comp['city'],
                  data_comp['companySize'],
                  data_comp['industryField'],
                  data_comp['url_lagou'],
                  data_comp['time_spider']
                  ]
            data_comp_list.append(data)
        try:
            self.cur.executemany("insert into company values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                 data_comp_list)
            self.cur.connection.commit()
        except Exception as e:
            print("储存数据出错：{}".format(e))

    def output_leaders(self):
        data_leader_list=[]
        for data_leader in self.datas_leader:
            data=[data_leader['name'],
                  data_leader['remark'],
                  data_leader['position'],
                  data_leader['weibo'],
                  data_leader['cyclopediaUrl'],
                  data_leader['companyid'],
                  data_leader['time_spider']]
            data_leader_list.append(data)
        try:
            self.cur.executemany("insert into leaders ("
                                 "name,"
                                 "remark,"
                                 "position,"
                                 "weibo,"
                                 "cyclopediaUrl,"
                                 "companyid,"
                                 "time_spider) values (%s,%s,%s,%s,%s,%s,%s)",
                                 data_leader_list)
            self.cur.connection.commit()
        except Exception as e:
            print("储存数据出错：{}".format(e))

    def output_address(self):
        data_address_list=[]
        for data_address in self.datas_address:
            data=[data_address['province'],
                  data_address['city'],
                  data_address['district'],
                  data_address['businessArea'],
                  data_address['detailAddress'],
                  data_address['lat'],
                  data_address['lng'],
                  data_address['companyId'],
                  data_address['time_spider']]
            data_address_list.append(data)
        try:
            self.cur.executemany("insert into address ("
                                 "province,"
                                 "city,"
                                 "district,"
                                 "businessArea,"
                                 "detailAddress,"
                                 "lat,"
                                 "lng,"
                                 "companyId,"
                                 "time_spider) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                 data_address_list)
            self.cur.connection.commit()
        except Exception as e:
            print("储存数据出错：{}".format(e))

    def select_spidered_urls(self):
        self.cur.execute('select url_job from jobs')
        num_2=self.cur.fetchall()
        job_urls=[url[0] for url in num_2]
        self.cur.execute('select url_lagou from company')
        num_2=self.cur.fetchall()
        comp_urls=[url[0] for url in num_2]
        spidered_url=job_urls+comp_urls

        return spidered_url

if __name__ == '__main__':
    data_out=DataOutput()
    data_job=data_out.select_spidered_urls()