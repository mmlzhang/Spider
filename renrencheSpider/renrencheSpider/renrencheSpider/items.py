# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RenrenchespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class CarInfoItem(scrapy.Item):

    collection = 'renrencheInfo'
    # 城市名
    city_name = scrapy.Field()
    city_name_en = scrapy.Field()
    # 车的 品牌名
    car_brand_name = scrapy.Field()
    car_brand_name_en = scrapy.Field()
    # 车辆信息
    # 车 id
    id = scrapy.Field()
    # 图片
    img_src = scrapy.Field()
    # 出售 标题
    title = scrapy.Field()
    # 降价
    discount = scrapy.Field()
    # 购买年份
    year = scrapy.Field()
    # 里程数
    mileage = scrapy.Field()
    # 标签 车辆情况
    tags = scrapy.Field()
    # 标价
    price = scrapy.Field()
    # 首付
    first_pay = scrapy.Field()
    # 详情页面 的 连接 url
    info_page_url = scrapy.Field()


