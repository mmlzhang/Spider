
import re
from base64 import b64decode

import scrapy
from scrapy_redis.spiders import RedisSpider
from renrencheSpider.items import CarInfoItem2


class RenrenCheSpider(RedisSpider):
    """爬取人人车网站的二手车信息"""
    name = 'renrenche2'
    # 允许爬取的域名
    allowed_domains = ['renrenche.com']
    # redis 密钥
    redis_key = 'renrenche:spider'
    # 人人车域名
    domain_url = 'https://www.renrenche.com'

    def parse(self, response):
        """获取页面 汽车的详细 信息"""

        item = CarInfoItem2()

        selector = scrapy.Selector(response)
        car_info_list = selector.xpath('//ul[@class="row-fluid list-row js-car-list"]/li')
        if car_info_list:
            for car in car_info_list:
                try:
                    # 车的 id
                    id = car.xpath('./a/@href').extract()[0]
                    id = id.split('/')[-1]
                    item['id'] = id
                    # 图片地址
                    img_src = car.xpath('./a/div[@class="img-backgound"]/img/@src').extract()
                    if img_src:
                        try:
                            img = img_src[0].split('?')[0]
                            if '=' in img or 'base64' in img:
                                img = b64decode(img)
                            item['img_src'] = 'https:' + img
                        except:
                            item['img_src'] = None
                    # 标题
                    item['title'] = car.xpath('./a/h3/text()').extract()[0]
                    # 降价
                    discount = car.xpath('./a//div[@class="dis-main"]//text()').extract()
                    if discount:
                        item['discount'] = ' '.join(discount).replace(' ', '').replace('\n', ' ').strip()
                    year_mileage = car.xpath('./a//div[@class="mileage"]//text()').extract()
                    year_mileage = ''.join(year_mileage)
                    # 购买年份
                    year = year_mileage.split('/')[0].strip()
                    # 里程数
                    mileage = year_mileage.split('/')[-1].strip()
                    item['year'] = year if len(year) < 12 else year[:12]
                    item['mileage'] = mileage
                    # 标签 车辆情况
                    tags = car.xpath('./a//div[@class="mileage-tag-box"]//text()').extract()
                    if tags:
                        item['tags'] = ''.join(tags).replace(' ', '').replace('\n', ' ')
                    # 标价
                    price = car.xpath('./a//div[@class="price"]//text()').extract()
                    item['price'] = ''.join(price).strip().split(' ')[0]
                    # 首付
                    first_pay = car.xpath('./a//div[@class="down-payment"]//text()').extract()
                    if first_pay:
                        item['first_pay'] = ''.join(first_pay[1:])
                    # 详情页面 url
                    item['info_page_url'] = self.domain_url + car.xpath('./a/@href').extract()[0]
                except Exception as e:
                    s = e
                    continue
                yield item

