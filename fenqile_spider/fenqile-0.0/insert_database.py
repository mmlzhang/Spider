# coding=utf-8

"""

    将 mongodb 中的原始数据进行过滤，筛选出需要的字段存储在 MySQL 中

"""



import json
import datetime

import requests
import pymysql
import pymongo


def insert_category(conn):
    """将商品的种类插入数据库 """
    # 商品种类的 id 和对应的名称
    categories_dict = {
        66: "手机",
        327: "腕表配饰",
        65: "电脑办公",
        67: "相机单反",
        217: "平板数码",
        179: "运动户外",
        255: "家电家居",
    }
    with conn.cursor() as cursor:
        for category_id, category_name in categories_dict.items():
            sql = "insert into goods_category (category_id, category_name, create_time) values (%s, %s, %s)"
            t = datetime.datetime.now()
            create_time = datetime.datetime.strftime(t, "%Y-%m-%d %H:%M:%S")
            result = cursor.execute(sql, (category_id, category_name, create_time))
            conn.commit()


def insert_brand(conn):
    """将商品的品牌插入数据库"""
    brand_list = []
    category_id_list = [66, 327, 65, 67, 217, 179, 255]
    for category_id in category_id_list:
        try:
            brand_url = "https://channel.fenqile.com/product/query_filter_list.json?line_type=category_id_1&category_id={category_id}"
            res = requests.get(brand_url.format(category_id=category_id))
            # 所有的brand字典组成的列表
            brands = json.loads(res.content.decode("utf-8")).get("brand_list")
            brand_list += brands
        except:
            print("出错了：category_id:", category_id)
            print()
            continue

    key_words = ['brand_id', 'brand_name', 'brand_name_ch', 'brand_name_en', 'category_id_1']
    sql = "insert into goods_brand values (%s, %s, %s, %s, %s, %s)"
    with conn.cursor() as cursor:
        brand_set = set()
        for brand in brand_list:
            brand_id = int(brand.get("brand_id"))
            print(brand_id)
            if brand_id not in brand_set:
                t = datetime.datetime.now()
                create_time = datetime.datetime.strftime(t, "%Y-%m-%d %H:%M:%S")
                brand_name = brand.get("brand_name")
                brand_name_ch = brand.get("brand_name_ch") if brand.get("brand_name_ch") else brand_name
                brand_name_en = brand.get("brand_name_en") if brand.get("brand_name_en") else brand_name
                category_id = int(brand.get("category_id_1"))
                category_id = category_id if category_id in category_id_list else 1000
                # 插入数据库
                result = cursor.execute(sql, (brand_id, create_time, brand_name, brand_name_ch, brand_name_en, category_id))
                print(result)
                conn.commit()
            # 加入去重队列
            brand_set.add(brand_id)


def insert_goods(conn, GOODS):
    """将商品信息插入数据库"""
    # 数据库中的所有的字段 22 个
    kws = ("sku_id", "product_name", "category_id_1", "brand_id", "product_desc",
         "short_product_name", "sku_key_1", "sku_key_2", "sku_key_3", "product_flag",
         "min_firstpay", "is_product_up_down", "real_amount", "mart_amount", "fq_num",
         "product_info", "delivery_time", "gift_list", "fe_params", "slider_imgs",
         "detail_imgs", "create_time")
    sql = "insert into goods values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

    goods = GOODS.find()
    for good in goods:
        try:
            data = []
            # 商品 id 去重集合
            good_id_set = set()
            for kw in kws[:-5]:
                info = good["detail_data"].get(kw)
                data.append(info)
            # 单独处理复杂的项目
            gift_list = " ".join([str(s) for s in good["detail_data"].get("gift_list")[-1].values()])
            data.append(gift_list)
            fe_params = json.dumps(good["detail_data"].get("fe_params"))
            data.append(fe_params)
            slider_imgs = "||".join(good["slider_imgs"])
            data.append(slider_imgs)
            detail_imgs = "||".join(good["detail_imgs"])
            data.append(detail_imgs)
            t = datetime.datetime.now()
            create_time = datetime.datetime.strftime(t, "%Y-%m-%d %H:%M:%S")
            data.append(create_time)
            # 判断 id 是否重复
            if good["good_id"] not in good_id_set:
                with conn.cursor() as cursor:
                    cursor.execute("select brand_id from goods_brand")
                    all_brand_ids = [brand_id[0] for brand_id in cursor.fetchall()]
                    cursor.execute("select category_id from goods_category")
                    all_category_ids = [category_id[0] for category_id in cursor.fetchall()]
                    data[2] = 1000 if int(data[2]) not in all_category_ids else int(data[2])
                    data[3] = 10000 if int(data[3]) not in all_brand_ids else (data[3])
                    cursor.execute(sql, tuple(data))
                    conn.commit()
            good_id_set.add(good["good_id"])
        except:
            continue



def main():
    # MySQL 连接
    conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", password="123456",
                           db="test", charset="utf8", autocommit=False)

    # 将 分类插入数据库
    # insert_category(conn)

    # 将品牌插入数据库
    # insert_brand(conn)

    # 将商品插入数据库
    # mongodb  连接
    CONN = pymongo.MongoClient(host='10.7.152.75', port=27017)
    GOODS = CONN["fenqile"]["goods"]

    insert_goods(conn, GOODS)

    conn.close()


if __name__ == "__main__":
    main()
