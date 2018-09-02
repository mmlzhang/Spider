
import re
import scrapy

import urllib.request
from lxml import etree

from scrapy_redis.spiders import RedisSpider
from renrencheSpider.items import RedisUrlItem
from utils.user_agent import random_agent


class RenrenCheSpider(RedisSpider):
    """爬取人人车网站的二手车信息"""
    name = 'renrenche2'
    # 允许爬取的域名
    allowed_domains = ['renrenche.com']
    # redis 密钥
    redis_key = 'renrenche:spider'
    # 人人车域名
    domain_url = 'https://www.renrenche.com'

    def start_requests(self):
        """开始请求"""
        page_html = self.urllib_get_page_html(self.domain_url)
        city_xpath = '//div[@class="area-city-letter"]//a[@class="province-item "]/@href'
        brand_xpath = '/html/body/div[3]//div[@class="brand-more-content"]//span[@class="bn"]/a/@href'
        # 城市列表  ['/as/', '/ay/', '/bd/',...]
        city_list = self.etree_xpath_matched(page_html, xpath=city_xpath)
        # 品牌列表   ['/cd/aodi/', '/cd/asidunmading/', '/cd/baojun/'...]
        brand_list_origin = self.etree_xpath_matched(page_html, xpath=brand_xpath)
        # 处理后结果 ['aodi/', 'asidunmading/', 'baojun/'...]
        brand_list = [brand.split('/')[-2] + '/' for brand in brand_list_origin]
        for city in city_list:
            for brand in brand_list:
                url = self.domain_url + city + brand
                print(url)
                # 这里会出现 某个城市可能没有某种品牌的车的情况，在下一步需要过滤
                yield scrapy.Request(url=url)

    def parse(self, response):
        """解析首页， 获取每个城市的url 获得所有的品牌 以及页码"""
        selector = scrapy.Selector(response)
        # 所有的城市列表
        item = RedisUrlItem()
        # 过滤空页面， 空页面是没有分页的 ul class='pagination js-pagination'
        pagination = selector.xpath('//ul[@class="pagination js-pagination"]').extract()
        if pagination:  # 不是空页面的情况(页码也没有超出范围)
            item['url'] = response.url
            yield item
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

    def urllib_get_page_html(self, url, charsets=('utf-8',)):
        """
        使用 urllib 获取页面，并且 解码页面

        :param url: 请求的 url
        :param charsets: 解码字符集，默认 utf-8
        :return: str  解码后的页面内容
        """
        headers = {'User-Agent': random_agent()}
        req = urllib.request.Request(url, headers=headers)
        res = urllib.request.urlopen(req)
        page_bytes = res.read()
        page_html = None
        for charset in charsets:
            try:
                page_html = page_bytes.decode(charset)
                break  # 解析出正取的页面时, 跳出循环
            except UnicodeDecodeError as e:
                # logging.error('Decoder': e)
                pass
                # print('编码错误')
        if page_html:
            return page_html
        else:
            print('解码错误!')

    def etree_xpath_matched(self, html, xpath):
        """
        lxml.etree 匹配需要的内容

        :param html:
        :param xpath:
        :return:  type(list)
        """
        lxml_html = etree.HTML(html)
        result = lxml_html.xpath(xpath)
        return result
