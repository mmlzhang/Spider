
import redis

from scrapy.conf import settings


class RenrenchespiderPipeline(object):
    def process_item(self, item, spider):
        return item


class RedisRenrenchePipeline(object):

    def __init__(self):
        self.redis = redis.Redis(host=settings['REDIS_HOST'],
                                 port=settings['REDIS_PORT'])

    def process_item(self, item, spider):
        try:
            self.redis.lpush('renrenche:spider', item['url'])
        except:
            pass
        return item
