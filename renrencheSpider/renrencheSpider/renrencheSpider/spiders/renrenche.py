
import re
import scrapy

from renrencheSpider.items import CarInfoItem


class RenrenCheSpider(scrapy.spiders.Spider):
    """爬取人人车网站的二手车信息"""
    name = 'renrenche'
    # 允许爬取的域名
    allowed_domains = ['renrenche.com']
    # 人人车域名
    domain_url = 'https://www.renrenche.com'
    # 开始的网址
    start_urls = [domain_url,]

    def parse(self, response):
        """解析首页， 获取每个城市的url """
        selector = scrapy.Selector(response)
        # 所有的城市列表
        city_list = selector.xpath('//div[@class="area-city-letter"]//a[@class="province-item "]')
        for city in city_list:
            try:
                # 城市 url
                city_url = city.xpath('./@href').extract()[0]
                # 城市名称
                city_name = city.xpath('./text()').extract()[0]
                city_name_en = city_url.replace('/', '')
                # 拼接 url
                url = self.domain_url + city_url
            except:
                continue

            yield scrapy.Request(url=url,
                                 meta={'city_name': city_name,
                                       'city_name_en': city_name_en},
                                 callback=self.parse_car_brand)

    def parse_car_brand(self, response):
        """通过每个城市的url 获取所有汽车种类的url """
        selector = scrapy.Selector(response)
        # 城市名称
        city_name = response.meta.get('city_name')
        city_name_en = response.meta.get('city_name_en')
        # 所有的 车的 品牌
        car_brands = selector.xpath('/html/body/div[3]//div[@class="brand-more-content"]//span[@class="bn"]/a')
        for car_brand in car_brands:
            try:
                # 该品牌的 url  例：'/my/aodi/'  my-城市（绵阳）  aodi-车的品牌名（奥迪）
                car_brand_url = car_brand.xpath('./@href').extract()[0]
                # 该品牌的 名称
                car_brand_name = car_brand.xpath('./text()').extract()[0]
                car_brand_name_en = car_brand_url.split('/')[-2]

                url = self.domain_url + car_brand_url
            except:
                continue
            yield scrapy.Request(url=url,
                                 meta={'city_name': city_name,
                                       'city_name_en': city_name_en,
                                       'car_brand_name': car_brand_name,
                                       'car_brand_name_en': car_brand_name_en},
                                 callback=self.parse_car_info)

    def parse_car_info(self, response):
        """获取页面 汽车的详细 信息"""

        item = CarInfoItem()
        # 城市名称
        city_name = response.meta.get('city_name')
        item['city_name'] = city_name
        city_name_en = response.meta.get('city_name_en')
        item['city_name_en'] = city_name_en
        # 品牌名称
        car_brand_name = response.meta.get('car_brand_name')
        item['car_brand_name'] = car_brand_name
        car_brand_name_en = response.meta.get('car_brand_name_en')
        item['car_brand_name_en'] = car_brand_name_en

        selector = scrapy.Selector(response)
        car_info_list = selector.xpath('//ul[@class="row-fluid list-row js-car-list"]/li')
        if car_info_list:
            for car in car_info_list:
                try:
                    # 车的 id
                    href = car.xpath('./a/@href').extract()[0]
                    id = href.split('/')[-1]
                    item['id'] = id
                    # 汽车详情页面 url
                    item['info_page_url'] = self.domain_url + href
                    # 图片地址
                    img_src = car.xpath('./a/div[@class="img-backgound"]/img/@src').extract()
                    if img_src:
                        item['img_src'] = 'https:' + img_src[0]
                    # 标题
                    item['title'] = car.xpath('./a/h3/text()').extract()[0]
                    # 降价
                    discount = car.xpath('./a//div[@class="dis-main"]//text()').extract()
                    if discount:
                        item['discount'] = ' '.join(discount).replace(' ', '').replace('\n', ' ')
                    year_mileage = car.xpath('./a//div[@class="mileage"]//text()').extract()
                    year_mileage = ''.join(year_mileage)
                    # 购买年份
                    year = year_mileage.split('/')[0]
                    # 里程数
                    mileage = year_mileage.split('/')[-1]
                    item['year'] = year
                    item['mileage'] = mileage
                    # 标签 车辆情况
                    tags = car.xpath('./a//div[@class="mileage-tag-box"]//text()').extract()
                    if tags:
                        item['tags'] = ''.join(tags).replace(' ', '').replace('\n', ' ')
                    # 标价
                    price = car.xpath('./a//div[@class="price"]//text()').extract()
                    item['price'] = ''.join(price).strip()
                    # 首付
                    first_pay = car.xpath('./a//div[@class="down-payment"]//text()').extract()
                    if first_pay:
                        item['first_pay'] = ' '.join(first_pay)
                   
                except:
                    continue
                yield item

            # 下一页
            page = response.meta.get('page', 2)
            url = response.url
            url = re.sub('p\d+/', '', url)
            url = url + 'p%d/' % page
            yield scrapy.Request(url=url,
                                 meta={'page': page + 1,
                                       'city_name': city_name,
                                       'city_name_en': city_name_en,
                                       'car_brand_name': car_brand_name,
                                       'car_brand_name_en': car_brand_name_en},
                                 callback=self.parse_car_info)
