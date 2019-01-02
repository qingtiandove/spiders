#! python2
# -*- coding: utf-8 -*-
from peewee import *
from datetime import datetime


try:
    import psycopg2
    from playhouse.pool import PooledPostgresqlExtDatabase

    db = PooledPostgresqlExtDatabase(
        'ajxxgk',
        max_connections=8,
        stale_timeout=300,
        user='jd',
        host='***',
        password='***',
        autorollback=True,
        register_hstore=False)
except ImportError:
    db = SqliteDatabase('ajxxgk.sqlite')


class BaseModel(Model):
    class Meta:
        database = db


class Document(BaseModel):
    id = IntegerField(null=False, primary_key=True, verbose_name='法律文书URL数字ID')
    url = CharField(null=False, max_length=1000, verbose_name='法律文书URL')
    case_title = CharField(null=True, max_length=1000, verbose_name='法律文书标题')
    court = CharField(null=True, max_length=500, verbose_name='法律文书法院')
    law = CharField(null=True, max_length=1000, verbose_name='法律条例')
    content = TextField(null=True, verbose_name='法律文书内容')
    occur_time = DateTimeField(null=True, verbose_name='评论时间')

    created_time = DateTimeField(default=datetime.now, verbose_name='创建时间')


if __name__ == '__main__':
    Document.create_table()
