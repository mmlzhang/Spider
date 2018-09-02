
import re

import scrapy
from scrapy_redis.spiders import RedisSpider
from renrencheSpider.items import CarInfoItem, RedisUrlItem


class RenrenCheSpider(RedisSpider):
    """爬取人人车网站的二手车信息"""
    name = 'renrenche'
    # 允许爬取的域名
    allowed_domains = ['renrenche.com']
    # redis 密钥
    redis_key = 'renrenche:spider'
    # 人人车域名
    domain_url = 'https://www.renrenche.com'

    def parse(self, response):
        """获取页面 汽车的详细 信息"""
        item = CarInfoItem()
        url = response.url
        # 判断是master中的callback中的url,还是需要解析的页面的url,
        # master 中的 url 有车的品牌
        # 车辆详细信息的页面的每个 url 中 都有 car 例:https://www.renrenche.com/cd/car/CAR_ID
        flag = bool(re.findall(r'car', url))
        if not flag: # 不是解析车辆的详细信息的url, 就帮助master 解析页码, 给redis中添加url
            self.assist_master_parse(response)
        else:
            # 开始解析页面, 抓取需要的数据
            selector = scrapy.Selector(response)
            # 页面内的车辆详细信息
            car_detail_wrapper = selector.xpath('//div[@class="detail-wrapper"]')
            title = car_detail_wrapper.xpath('.//h1/text()').extract()
            if car_detail_wrapper and title:
                try:
                    # 标题
                    item['title'] = title[0]
                    # 城市名称
                    item['city_name_en'] = response.url.split('/')[-3]
                    # 车 id
                    item['id'] = response.url.split('/')[-1]
                    # 原价，新车价
                    item['price'] = car_detail_wrapper.xpath('.//div[@class="new-car-price detail-title-right-tagP"]/span/text()').extract()[0]
                    # 首付
                    first_pay = car_detail_wrapper.xpath('.//p[@class="money detail-title-right-tagP"]/text()').extract()[0]
                    item['first_pay'] = first_pay
                    # 月供
                    month_pay = car_detail_wrapper.xpath('.//p[@class="money detail-title-right-tagP"]/text()').extract()[-1]
                    if month_pay == first_pay:
                        month_pay = None
                    item['month_pay'] = month_pay
                    car_details = car_detail_wrapper.xpath('.//div[@class="row-fluid-wrapper"]//strong/text()').extract()
                    # 上牌时间
                    item['year'] = car_details[0]
                    # 公里数
                    item['mileage'] = car_details[1]
                    # 标准  例：国四
                    item['standard'] = car_details[2]
                    try:
                        # 排量
                        cc = car_details[-3]
                        item['cc'] = cc
                        # 上牌城市
                        licence_city = car_details[-1]
                        if cc == licence_city:
                            licence_city = None
                        item['city'] = licence_city
                    except:
                        pass
                    img_src_list = car_detail_wrapper.xpath('.//ul[@class="slides gallery-img"]/li/div[@class="recommend-img-container"]/img/@src').extract()
                    # 所有的图片
                    imgs = []
                    # i = 1
                    # for img_src in img_src_list[:1]:
                    #     imgs.append('https:' + img_src.split('?')[0])
                    #     i += 1
                    item['img_src'] = 'https:' + img_src_list[0].split('?')[0]
                    item['info_page_url'] = response.url
                except:
                    pass
                yield item

    def assist_master_parse(self, response):
        """帮助master 解析首页， 获取每个城市的url 获得所有的品牌 以及页码"""
        selector = scrapy.Selector(response)
        # 所有的城市列表
        item = RedisUrlItem()
        # 过滤空页面， 空页面是没有分页的 ul class='pagination js-pagination'
        pagination = selector.xpath('//ul[@class="pagination js-pagination"]').extract()
        if pagination:  # 不是空页面的情况(页码也没有超出范围)
            # 开始获取页面的信息，拼接获取每个车详情页面的 url
            car_info_list = selector.xpath('//ul[@class="row-fluid list-row js-car-list"]/li')
            for car in car_info_list:
                href = car.xpath('./a[@class="thumbnail"]/@href').extract()
                # 过滤广告 的 a 标签  (广告 class="sale-car-enter")
                if href:
                    try:
                        # 汽车详情页面 url
                        url = self.domain_url + href[0]
                        # url 会出现
                        item['url'] = url
                        yield item
                    except:
                        continue
            # 下一页，当没有下一页时， 出现的也是空页面
            url = response.url
            page = response.meta.get('page', 2)
            url = re.sub('p\d+/', '', url)
            url = url + 'p%d/' % page
            yield scrapy.Request(url=url, meta={'page': page + 1}) # 默认调用的是 self.parse()
        else:
            # 空页面
            # print('空页面：',response.url)
            pass

