#!/usr/bin/env python3 
# -*- coding=utf-8 -*-

from db import RedisClient 
from crawler import Crawler 
from settings import * 
from tester import Tester 
import sys 

class Getter():
	def __init__(self):
		self.redis = RedisClient()
		self.crawler = Crawler()

	def is_over_threshold(self):
		if self.redis.count() >= POOL_UPPER_THRESHOLD:
			return True 
		else:
			return False 

	def run(self):
		print('获取器开始执行')
		if not self.is_over_threshold():
			for callback_label in range(self.crawler.__CrawlFuncCount__):
				callback = self.crawler.__CrawlFunc__[callback_label]
				# 获取代理
				proxies = self.crawler.get_proxies(callback)
				sys.stdout.flush()
				for proxy in proxies:
					self.redis.add(proxy)
					# print(proxy)


if __name__ == '__main__':
	g = Getter()
	g.run()