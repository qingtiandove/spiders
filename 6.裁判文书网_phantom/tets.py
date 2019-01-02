# tasks.py
import time
from celery import Celery
from random import random
from celery.schedules import crontab

#broker='redis://:qingtian@localhost:6379/0',
app = Celery('tets',
             broker='redis://:qingtian@localhost:6379/0',
             backend='redis://:qingtian@localhost:6379/0',)
app.conf.update(
   #  配置所在时区
    CELERY_TIMEZONE='Asia/Shanghai',
    CELERY_ENABLE_UTC=True,
    #  官网推荐消息序列化方式为json
    #CELERY_ACCEPT_CONTENT = ['application/json'],
    CELERY_TASK_SERIALIZER='json',
    CELERY_RESULT_SERIALIZER='json',
    CELERYBEAT_SCHEDULE={
        'get_list': {
            'task': 'ajxxgk.main_list',  # tasks.py模块下的add方法
            'schedule': crontab(hour=3, minute=10),
        },
        'get_content':{
            'task': 'ajxxgk.main_content',  # tasks.py模块下的add方法
            'schedule': crontab(hour=3, minute=30),
        }
    }
)

# 配置定时任务


@app.task
def get_x(x,y):
   return x+y

@app.task
def produce_data():
    data=random()
    name={'xu':data}
    return name

