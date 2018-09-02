
import pymongo

# mongodb 设置
MONGO = {
    "HOST": '10.7.152.75',
    "PORT": 27017,
    "DB": "fenqile",  # 数据库名称
    "COLLECTION": "goods",  # collection 数据集的名称
    "USER": None,  # 用户名
    "PASSWORD": None,  # 密码
}

# mongodb  连接
CONN = pymongo.MongoClient(
    host=MONGO["HOST"],
    port=MONGO["PORT"]
)

# 连接的数据库, 需要哪张表可以在上面的 COLLECTION 字段进行设置
MONGO_DB = CONN[MONGO["DB"]]
# collection mongodb 中的表
COLLECTION = MONGO_DB[MONGO["COLLECTION"]]



