
import pymongo

from RRC_show_by_Django.settings import MONGO_PORT, MONGO_HOST

conn = pymongo.MongoClient(host=MONGO_HOST, port=MONGO_PORT)

mongodb_car_info = conn.renrenche.rrc_data
