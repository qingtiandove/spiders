

class UrlManager(object):
    def __init__(self):
        self.zhaopin_urls=set()
        self.new_urls = set()
        self.old_urls = set()

    def read_redis(self,redis_zhaopin):
        self.zhaopin_urls=redis_zhaopin.smembers('zhaopin_2')
        print(len(self.zhaopin_urls))

    def has_new_url(self):
        return self.new_url_size() != 0

    def get_new_url(self):
        new_url = self.new_urls.pop()
        self.old_urls.add(new_url)
        return new_url

    def add_new_url(self, url):
        if url is None:
            return
        if url not in self.new_urls and url not in self.old_urls:
            self.new_urls.add(url)

    def add_new_urls(self, urls):
        if urls is None or len(urls) == 0:
            return
        for url in urls:
            self.add_new_url(url)

    def new_url_size(self):
        return len(self.new_urls)

    def old_url_size(self):
        return len(self.old_urls)

if __name__ == '__main__':
    import redis
    redis_zhaopin=redis.Redis(host='127.0.0.1',port=6379,db=1,decode_responses=True)
    test=UrlManager()
    test_2=test.read_redis(redis_zhaopin)
    print('结束')