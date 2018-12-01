#!/usr/bin/env python3 
# -*- coding=utf-8 -*-

from gevent import monkey 
monkey.patch_all()
from gevent.pool import Pool 
import multiprocessing 
import requests 
import time 
import random 
import re 
import pymongo
import pymysql
from fake_useragent import UserAgent 
from lxml import etree 
import redis 

REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_PASSWORD = None
REDIS_KEY = 'urls'

ua = UserAgent()
headers = {'User-Agent': ua.random}

class RedisClient(object):
	def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
		self.db = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)

	def add(self, url, score=3):
		if not re.match('[http-https]://.*', url):
			print('url不符合规范', url, '丢弃')
		if not self.db.zscore(REDIS_KEY, ulr):
			return self.db.zadd(REDIS_KEY, score, url)

