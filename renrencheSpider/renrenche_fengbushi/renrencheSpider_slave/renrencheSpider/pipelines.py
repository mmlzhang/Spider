
import pymongo
import redis

from scrapy.conf import settings

from renrencheSpider.items import CarInfoItem, CarInfoItem2


class RenrenchespiderPipeline(object):
    def process_item(self, item, spider):
        return item


class MongodbRenrenchePipeline(object):
    """插入数据"""
    def __init__(self):
        conn = pymongo.MongoClient(host=settings['MONGO_HOST'],
                                 port=settings['MONGO_PORT'])
        self.db = conn.renrenche

    def process_item(self, item, spider):
        # 1.0 版本
        if isinstance(item, CarInfoItem):
            try:
                collection = self.db['rrc_data']
                collection.update({'id': item['id']},
                                       {'$set': dict(item)},
                                       upsert=True)
            except:
                pass
        # 2.0版本
        # if isinstance(item, CarInfoItem2):
        #     try:
        #         collection = self.db['rrc_fengbushi2']
        #         collection.update({'id': item['id']},
        #                                {'$set': dict(item)},
        #                                upsert=True)
        #     except:
        #         pass

        return item

