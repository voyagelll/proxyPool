#!/usr/bin/env python3 
# -*- coding=utf-8 -*-

import redis 
import re 
from random import choice 
from settings import REDIS_HOST, REDIS_PASSWORD, REDIS_PORT, REDIS_KEY
from settings import MAX_SCORE, MIN_SCORE, INITIAL_SCORE


class RedisClient(object):
	# 初始化redis
	def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
		self.db = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)
	
	# 添加代理，设置分数为最高
	def add(self, proxy, score=INITIAL_SCORE):
		if not re.match('\d+.\d+.\d+.\d+\:\d+', proxy):
			print('代理不和规范', proxy, '丢弃')	
		if not self.db.zscore(REDIS_KEY, proxy):
			return self.db.zadd(REDIS_KEY, score, proxy)

	# 随机获取有效代理，首先尝试最高分，若不存在，则按照排名，否则异常
	def random(self):
		result = self.db.zrangebyscore(REDIS_KEY, MAX_SCORE, MAX_SCORE)
		if len(result):
			return choice(result)	
		else:
			result = self.db.zrevrange(REDIS_KEY, 0, 10)
			if len(result):
				return choice(result) 
			else:
				raise PoolEmptyError	

	# 代理值减一分，小于0则删除
	def decrease(self, proxy):
		score = self.db.zscore(REDIS_KEY, proxy)
		if score and score > MIN_SCORE:
			#print('代理请求失败', proxy, '当前分数', score, '减1')
			return self.db.zincrby(REDIS_KEY, proxy, -1)
		else:
			#print('代理请求失败', proxy, '当前分数', score, '移除')
			return self.db.zrem(REDIS_KEY, proxy)

	# 判断是否存在
	def exists(self, proxy):
		return not self.db.zscore(REDIS_KEY, proxy) == None 

	# 将代理设置为max_score
	def max(self, proxy):
		print('代理', proxy, '可用，设置为', MAX_SCORE)
		return self.db.zadd(REDIS_KEY, MAX_SCORE, proxy)

	# 获取数量
	def count(self):
		return self.db.zcard(REDIS_KEY)

	# 获取全部代理
	def all(self):
		return self.db.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)

	def batch(self, start, stop):
		return self.db.zrevrange(REDIS_KEY, start, stop-1)

if __name__ == '__main__':
	conn = RedisClient()
	result = conn.batch(680, 688)
	print(result)	








