#!/usr/bin/env python3 
# -*- coding=utf-8 -*-

import json 
import re
import requests
from lxml import etree 
from fake_useragent import UserAgent 
from db import RedisClient 

redis = RedisClient()
ua = UserAgent()
# headers = {'User-Agent': ua.random}
proxies = {
	'http': 'http://' + redis.random(),
	'https': 'https://' + redis.random(),
}
# print(proxies)

class ProxyMetaclass(type):
	def __new__(cls, name, bases, attrs):
		count = 0
		attrs['__CrawlFunc__'] = []
		for k, v in attrs.items():
			if 'crawl_'in k:
				attrs['__CrawlFunc__'].append(k)
				count += 1 
		attrs['__CrawlFuncCount__'] = count 
		return type.__new__(cls, name, bases, attrs)


class Crawler(object, metaclass=ProxyMetaclass):
	def get_proxies(self, callback):
		proxies = []
		for proxy in eval("self.{}()".format(callback)):
			print('成功获取到代理', proxy)
			proxies.append(proxy)
		return proxies 


	def crawl_66ip_api(self):
		print('获取66ip_api代理：')
		url = 'http://www.66ip.cn/nmtq.php?getnum=300&isp=0&anonymoustype=3&start=&ports=&export=&ipaddress=&area=0&proxytype=1&api=66ip'
		headers = {
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
			'Accept-Encoding': 'gzip, deflate',
			'Accept-Language': 'zh-CN,zh;q=0.9',
			'Connection': 'keep-alive',
			'Cookie': 'yd_cookie=8f466d20-b998-450013c7b6c0778df705bd027b48d6d9dea5; _ydclearance=eb9e4f095a82fb8783a28d4a-ea44-459e-8bd8-ce4566c5a3b5-1542896989; Hm_lvt_1761fabf3c988e7f04bec51acd4073f4=1541639201,1542889796; Hm_lpvt_1761fabf3c988e7f04bec51acd4073f4=1542890615',
			'Host': 'www.66ip.cn',
			'Referer': 'http://www.66ip.cn/nm.html',
			'Upgrade-Insecure-Requests': '1',
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
		}
		rsp = requests.get(url, headers=headers)
		print(rsp)
		if rsp.status_code == 200:
			ips = re.findall('\d+.\d+.\d+.\d+:\d+', rsp.text)
			print('获取成功')
			for ip in ips:
				yield ip


	def crawl_66ip(self):
		print('获取66ip代理')
		headers = {
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
			'Accept-Encoding': 'gzip, deflate',
			'Accept-Language': 'zh-CN,zh;q=0.9',
			'Cache-Control': 'max-age=0',
			'Connection': 'keep-alive',
			'Cookie': 'yd_cookie=8f466d20-b998-450013c7b6c0778df705bd027b48d6d9dea5; _ydclearance=eb9e4f095a82fb8783a28d4a-ea44-459e-8bd8-ce4566c5a3b5-1542896989; Hm_lvt_1761fabf3c988e7f04bec51acd4073f4=1541639201,1542889796; Hm_lpvt_1761fabf3c988e7f04bec51acd4073f4=1542889980',
			'Host': 'www.66ip.cn',
			'Upgrade-Insecure-Requests': '1',
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
		}
		for i in range(2, 3):
			url = 'http://www.66ip.cn/' + str(i) + '.html'
			# headers = {
			# 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
			# }
			rsp = requests.get(url, headers=headers)
			print(rsp)
			doc = etree.HTML(rsp.text)
			trs = doc.xpath('//div[@align="center"]/table/tr')
			for tr in trs[1:]:
				ip = tr.xpath('td[1]/text()')[0]
				port = tr.xpath('td[2]/text()')[0]
				# print(ip + ':' + port)
				proxy = ip + ':' + port
				yield proxy


	def crawl_dragonfly(self):
		print('获取蜻蜓免费代理')
		url = 'https://proxy.horocn.com/day-free-proxy/0NlM.html'
		headers = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
		}
		rsp = requests.get(url, headers=headers)
		print(rsp)
		if rsp.status_code == 200:
			ips = re.findall('\d+.\d+.\d+.\d+:\d+', rsp.text)
			print('获取成功')
			for ip in ips:
				yield ip


	def crawl_xici(self):
		ips = []
		print('获取西刺免费代理')
		headers = {
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
			'Accept-Encoding': 'gzip, deflate',
			'Accept-Language': 'zh-CN,zh;q=0.9',
			'Cache-Control': 'max-age=0',
			'Connection': 'keep-alive',
			# 'Cookie': '_free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJTQxNjQ2OWQ5OWI4Yjc4ZmY3OTE2NWViNjNmMzkzMGUwBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMWxLNERLTGs5eGdUREpKa3A5LzFoRmhYelN1dEpJZlJzWHJUYmsxZnpjRjQ9BjsARg%3D%3D--d4c4dea0e2a7109c697a371afcd1003774e841d7; Hm_lvt_0cf76c77469e965d2957f0553e6ecf59=1542022766,1542023452,1542889042; Hm_lpvt_0cf76c77469e965d2957f0553e6ecf59=1542889120',
			'Host': 'www.xicidaili.com',
			'If-None-Match': 'W/"7f0f61a7eadb0d36be352ec2cb5b58f8"',
			'Referer': 'http://www.xicidaili.com/',
			# 'Upgrade-Insecure-Requests': '1',
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
		}
		for i in range(3):
			try:
				url = 'http://www.xicidaili.com/wn/' + str(i+1)
				rsp = requests.get(url, headers=headers)

				print(rsp)
				if rsp.status_code == 200:
					doc = etree.HTML(rsp.text)
					trs = doc.xpath('//table[@id="ip_list"]/tr')
					for tr in trs[1:]:
						ip = tr.xpath('td[2]/text()')[0]
						port = tr.xpath('td[3]/text()')[0]
						yield (ip+':'+port)
			except:
				print('请求失败', proxies)



	


# url = 'http://www.66ip.cn/1.html'
# headers = {
# 	# 'cookie': '__cfduid=d5a8bb7f6837b8aa87d4df2131e4b1e661541647482; Hm_lvt_8ccd0ef22095c2eebfe4cd6187dea829=1541647487; statistics=90ff8ae6231a43c42b418e1765751722; cf_clearance=40e1c57b597f0514678331e590a3a7fe1413e1d7-1541648002-1800-250; Hm_lpvt_8ccd0ef22095c2eebfe4cd6187dea829=1541648008',
# 	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
# }
# rsp = requests.get(url, headers=headers)
# print(rsp)
# # print(rsp.text)
# # ips = re.findall('\d+\.\d+\.\d+\.\d+:\d+', rsp.text)
# # print(ips)


# doc = etree.HTML(rsp.text)
# trs = doc.xpath('//table[@id="ip_list"]/tr')
# # print(trs)
# for tr in trs[1:]:
# 	ip = tr.xpath('td[2]/text()')[0]
# 	port = tr.xpath('td[3]/text()')[0]
# 	print(ip + ':' + port)
# # print(ips)


		


# print('获取66ip')
# # for i in range(1):
# url = 'http://www.66ip.cn/2.html'

# rsp = requests.get(url, headers=headers)
# print(rsp)
# doc = etree.HTML(rsp.text)
# trs = doc.xpath('//div[@align="center"]/table/tr')
# for tr in trs[1:]:
# 	ip = tr.xpath('td[1]/text()')[0]
# 	port = tr.xpath('td[2]/text()')[0]
# 	print(ip + ':' + port)
# 	# proxy = ip + ':' + port
# 	# yield proxy


# print('获取66ip代理：')
# url = 'http://www.66ip.cn/nmtq.php?getnum=300&isp=0&anonymoustype=3&start=&ports=&export=&ipaddress=&area=0&proxytype=1&api=66ip'
# headers = {
# 	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
# 	'Accept-Encoding': 'gzip, deflate',
# 	'Accept-Language': 'zh-CN,zh;q=0.9',
# 	'Connection': 'keep-alive',
# 	'Cookie': 'yd_cookie=8f466d20-b998-450013c7b6c0778df705bd027b48d6d9dea5; _ydclearance=eb9e4f095a82fb8783a28d4a-ea44-459e-8bd8-ce4566c5a3b5-1542896989; Hm_lvt_1761fabf3c988e7f04bec51acd4073f4=1541639201,1542889796; Hm_lpvt_1761fabf3c988e7f04bec51acd4073f4=1542890615',
# 	'Host': 'www.66ip.cn',
# 	'Referer': 'http://www.66ip.cn/nm.html',
# 	'Upgrade-Insecure-Requests': '1',
# 	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
# }
# rsp = requests.get(url, headers=headers)
# print(rsp)
# if rsp.status_code == 200:
# 	ips = re.findall('\d+.\d+.\d+.\d+:\d+', rsp.text)
# 	print('获取成功')
# 	for ip in ips:
# 		print(ip)
# 		# yield ip