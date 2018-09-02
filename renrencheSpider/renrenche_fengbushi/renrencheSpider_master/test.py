# -*-coding: utf-8 -*-
__author__ = 'Zhang'

from scrapy_redis.dupefilter import BloomFilter

"""测试 BloomFilter """

import redis


conn = redis.StrictRedis(host='localhost', port=6379, password='')
bf = BloomFilter(conn, 'testbf', 5, 6)
# bf.insert('Hello')
# bf.insert("world")
result = bf.exists('Hello')
print(bool(result))  # True

result2 = bf.exists('python')
print(bool(result2))  # False


import requests

import selenium

