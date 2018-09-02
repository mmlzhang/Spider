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


class RedisUrlItem(scrapy.Item):

    url = scrapy.Field()


class CarInfoItem(scrapy.Item):
    """1.0版"""
    city_name_en = scrapy.Field()
    # 车辆信息
    id = scrapy.Field()  # 车 id
    title = scrapy.Field()  #  标题
    price = scrapy.Field()  # 标价
    first_pay = scrapy.Field()  # 首付
    month_pay = scrapy.Field()   # 月供
    year = scrapy.Field()  # 上牌时间
    mileage = scrapy.Field()  # 公里数
    standard = scrapy.Field()  # 标准  例：国四
    cc = scrapy.Field()  # 排量
    city = scrapy.Field()  # 上牌城市

    img_src = scrapy.Field()  # 图片
    discount = scrapy.Field()  # 降价
    tags = scrapy.Field()  # 标签 车辆情况
    info_page_url = scrapy.Field()  # 详情页面 的 连接 url


class CarInfoItem2(scrapy.Item):
    """2.0"""
    # 城市名
    city_name = scrapy.Field()
    city_name_en = scrapy.Field()
    # 车的 品牌名
    car_brand_name = scrapy.Field()
    car_brand_name_en = scrapy.Field()
    # 车辆信息
    id = scrapy.Field()  # 车 id
    img_src = scrapy.Field()  # 图片
    title = scrapy.Field()  # 出售 标题
    discount = scrapy.Field()   # 降价
    year = scrapy.Field()  # 购买年份
    mileage = scrapy.Field()  # 里程数
    tags = scrapy.Field()  # 标签 车辆情况
    price = scrapy.Field()  # 标价
    first_pay = scrapy.Field()  # 首付
    info_page_url = scrapy.Field()  # 详情页面 的 连接 url
