# coding=utf-8

"""

    爬取分期乐的全部的数据，存储在 mongodb 中

"""
import json

import requests

from utils.functions import etree_xpath
from utils.mongo_conn import COLLECTION   # mongodb的数据集


def get_good_page_url(url, category_id):
    """
    获取详情每个商品的详情页面的 url

    :param url: 发送 post 请求的 url
    :return:  所有详情页面的 url  "https://item.fenqile.com/S201709120586965.html"
    """
    # 所有的大类型：如：66-手机  327-腕表配饰  65-电脑办公  67-相机单反  217-平板数码  179-运动户外 255-家电家居
    # category_id_1_list = [66, 327, 65, 67, 217, 179]
    # for category_id_1 in category_id_1_list:

    # post 请求的表单数据
    url_list = []
    page = 0
    flag = True
    while flag:
        try:
            page += 1
            data = {
                'category_id_1': category_id,  # 来自 category_id_1_list
                'category_id_2': 0,  # 手机系统类型 id  0-全部  如： ios-99   Android-597
                'category_id_3': 0,  # 暂时无用
                'feature_id_1': 0,  # 暂时无用
                'feature_id_2': 0,  # 暂时无用
                'feature_id_3': 0,  # 暂时无用
                'brand_id': 0,  # 0-全部 品牌 id  如：小米-12
                'amount': 0,  # 暂时无用
                'undefined': 0,  # 暂时无用
                'page': page,  # 页码， 最后会有一个 total_page
            }

            # 解析 url 获取数据
            res = requests.post(url, data)
            json_data = json.loads(res.content.decode("utf-8"))
            html = json_data.get('html')
            url_xpath = '//ul[@class="list-li fn-clear js-noraml-li"]/li/@data-url'
            # 获取每一页的 url 列表
            page_url_list = etree_xpath(html, url_xpath)
            url_list += ["https:" + url for url in page_url_list]
        except:
            print("获取详情每个商品的详情页面的 url 错误：", page, url)
            print()
            continue
        # 达到最后一页，停止循环
        if page == json_data.get("total_page"):
            flag = False
    return url_list


def get_goods_details(good_id):
    """
    获取商品的详情

    get_details_insert_db 函数内调用
    :param good_id: str 商品的编号
    :return: 商品的所有信息
    """
    base_url = "https://item.fenqile.com/item/query_sku_info.json?sku_id={good_id}&province_id=19&city_id=1601&area_id=36953&direct_send=1&product_type=normal&index_flag=1"
    url = base_url.format(good_id=good_id)
    res = requests.get(url)
    if int(res.status_code) == 200:
        good_data = json.loads(res.content.decode("utf-8")).get("sku")
        return good_data


def get_comments(product_id):
    """
    获取商品的评论

    :param product_id: int 商品的id
    :return: 商品的所有评论列表
    """
    comment_list = []
    comment_url = "https://item.fenqile.com/item/query_product_comment.json?product_id={product_id}&page={page}"
    page = 0
    flag = True
    while flag:
        page += 1
        url = comment_url.format(product_id=product_id, page=page)
        res = requests.get(url)
        data = json.loads(res.content.decode("utf-8"))
        comments = data.get("comment_list")
        total_page = data.get("total_page")
        comment_list += comments
        if  page == int(total_page):
            flag = False
    return comment_list


def get_details_insert_db(detail_urls, category_id):
    """
    获取商品的详情 插入数据库

    :param detail_urls:  list  商品详情页面的 url 列表
    """
    for url in detail_urls:
        try:
            goods = {}
            # 商品的 id
            good_id = url.split('/')[-1].split(".")[0]
            goods["good_id"] = good_id
            goods["category_id"] = category_id
            res = requests.get(url)
            html = res.content.decode("utf-8")
            # 展示商品的轮播图
            slider_xpath = '//ul[@class="fn-clear"]//img/@src'
            slider_imgs = etree_xpath(html, slider_xpath)
            goods["slider_imgs"] = slider_imgs
            # 详情图片 大图
            detail_img_xpath = '//div[@class="product-msg"]//img/@data-original'
            detail_imgs = etree_xpath(html, detail_img_xpath)
            goods["detail_imgs"] = detail_imgs
            # 获取商品的详情数据
            detail_data = get_goods_details(good_id)
            goods["detail_data"] = detail_data
            # 品牌 id
            brand_id = detail_data.get("brand_id")
            goods["brand_id"] = brand_id
            # product_id
            product_id = detail_data.get("product_id")
            comments = get_comments(product_id)
            goods["comments"] = comments
            # 将图片插入数据库 mongodb
            COLLECTION.update({"good_id": good_id}, {"$set": goods}, upsert=True)
        except:
            print("获取商品的详情 插入数据库 出错了:", url)
            print()
            continue


def main():
    # 获取数据的 url  发送 post 请求
    post_url = 'https://channel.fenqile.com/product/get_more.json'
    # 商品种类  如：66-手机  327-腕表配饰  65-电脑办公  67-相机单反  217-平板数码  179-运动户外 255-家电家居
    category_id_list = [66, 327, 65, 67, 217, 179, 255]
    for category_id in category_id_list:
        try:
            # category_id = 66
            # 获取单个种类的详情页面的 url
            detail_urls = get_good_page_url(post_url, category_id)
            # detail_urls = ["https://item.fenqile.com/S201709120586965.html"]  # 测试用
            # 获取商品的的详情并插入数据库
            get_details_insert_db(detail_urls, category_id)
        except:
            print("出错了：category_id:", category_id)
            print()
            continue


if __name__ == "__main__":
    main()