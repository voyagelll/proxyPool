#!/usr/bin/env python3 
# -*- coding=utf-8 -*-

import json 
import re
import time
import random
import requests
from lxml import etree 
from fake_useragent import UserAgent 
from db import RedisClient 

redis = RedisClient()
ua = UserAgent()

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
			'Host': 'www.xicidaili.com',
			'If-None-Match': 'W/"7f0f61a7eadb0d36be352ec2cb5b58f8"',
			'Referer': 'http://www.xicidaili.com/',
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
		}
		for i in range(5):
			try:
				url = 'http://www.xicidaili.com/wn/' + str(i+1)
				rsp = requests.get(url, headers=headers)
				time.sleep(random.random() * 5)
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


	def crawl_goubanjia(self):
		print('获取goubanjia代理：')
		url = 'http://www.goubanjia.com/'
		headers = {
			'User-Agent': ua.random
		}
		rsp = requests.get(url, headers=headers)
		print(rsp)
		if rsp.status_code == 200:
			doc = etree.HTML(rsp.text)
		trs = doc.xpath('//div[@class="span12"]/table/tbody/tr')
		for tr in trs:
			raw_ip = tr.xpath('td[1]')[0]
			ip = raw_ip.xpath('string(.)')
			yield ip.replace('..', '.')


	def crawl_ip3366(self):
		print('获取ip3366代理：')
		for page in range(1, 6):
			url = 'http://www.ip3366.net/?stype=1&page=' + str(page)
			headers = {
				'User-Agent': ua.random
			}
			rsp = requests.get(url, headers=headers)
			print(rsp)
			if rsp.status_code == 200:
				doc = etree.HTML(rsp.text)
				trs = doc.xpath('//div[@id="list"]/table/tbody/tr')
				for tr in trs:
					ip = tr.xpath('td[1]/text()')[0] + ':' + tr.xpath('td[2]/text()')[0]
					# print(ip)
					yield ip
			time.sleep(random.random() * 5)


	def crawl_kaixin(self):
		print('获取kxdaili代理：')
		for page in range(5):
			url = 'http://ip.kxdaili.com/ipList/%s.html#ip' % (str(page + 1))
			print(url)
			headers = {
				'User-Agent': ua.random
			}
			rsp = requests.get(url, headers=headers)
			print(rsp)
			if rsp.status_code == 200:
				doc = etree.HTML(rsp.text)

				trs = doc.xpath('//div[@class="tab_c_box buy_tab_box"]/table/tbody/tr')
				for tr in trs:
					ip = tr.xpath('td[1]/text()')[0] + ':' + tr.xpath('td[2]/text()')[0]
					# print(ip)
					yield ip
			time.sleep(random.random() * 5)



	def crawl_xproxy(self):
		print('获取xroxy代理：')
		for page in range(1):
			url = 'https://www.xroxy.com/free-proxy-lists/?port=&type=Anonymous&ssl=&country=&latency=5000&reliability='
			headers = {
				'User-Agent': ua.random
			}
			rsp = requests.get(url, headers=headers)
			print(rsp)

			if rsp.status_code == 200:
				doc = etree.HTML(rsp.text)

				trs = doc.xpath('//tr[@role="row"]')
				for tr in trs[1:]:
					ip = tr.xpath('td[1]/text()')[0] + ':' + tr.xpath('td[2]/text()')[0]
					# print(ip)
					yield ip


	def crawl_kuaidaili(self):
		print('获取kxdaili代理：')
		for page in range(5):
			url = 'https://www.kuaidaili.com/free/inha/%s/' % (str(page +1))
			# print(url)
			headers = {
				'User-Agent': ua.random
			}
			rsp = requests.get(url, headers=headers)
			print(rsp)
			# print(rsp.text)
			if rsp.status_code == 200:
				doc = etree.HTML(rsp.text)
				trs = doc.xpath('//div[@id="list"]/table/tbody/tr')
				print(trs)
				for tr in trs[:]:
					ip = tr.xpath('td[1]/text()')[0] + ':' + tr.xpath('td[2]/text()')[0]
					# print(ip)
					yield ip
			time.sleep(random.random() * 5)


	def crawl_iphai(self):
		print('获取iphai代理：')
		for page in range(1):
			url = 'http://www.iphai.com/' 
			# print(url)
			headers = {
				'User-Agent': ua.random
			}
			rsp = requests.get(url, headers=headers)
			print(rsp)
			# print(rsp.text)
			if rsp.status_code == 200:
				doc = etree.HTML(rsp.text)
				trs = doc.xpath('//div[@class="table-responsive module"]/table/tr')
				print(trs)
				for tr in trs[1:]:
					ip = tr.xpath('td[1]/text()')[0].replace('\n', '').replace('\t','').replace('\r','').replace(' ','') + ':' \
					+ tr.xpath('td[2]/text()')[0].replace('\n', '').replace('\t','').replace('\r','').replace(' ','')
					# print(ip)
					yield(ip)


	def crawl_89ip(self):
		print('获取89ip代理：')
		for page in range(1):
			url = 'http://www.89ip.cn/tqdl.html?num=500&address=&kill_address=&port=&kill_port=&isp=' 
			# print(url)
			headers = {
				'User-Agent': ua.random
			}
			rsp = requests.get(url, headers=headers)
			print(rsp)
			if rsp.status_code == 200:
				doc = etree.HTML(rsp.text)
				trs = doc.xpath('//div[@class="layui-col-md8"]/div/div/text()')
				for tr in trs[1:-1]:
					yield str(tr).replace(' ', '')

	


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


# print('获取kxdaili代理：')
# for page in range(5):
# 	url = 'https://www.kuaidaili.com/free/inha/%s/' % (str(page +1))
# 	# print(url)
# 	headers = {
# 		'User-Agent': ua.random
# 	}
# 	rsp = requests.get(url, headers=headers)
# 	# print(rsp)
# 	# print(rsp.text)
# 	if rsp.status_code == 200:
# 		doc = etree.HTML(rsp.text)
# 		trs = doc.xpath('//div[@id="list"]/table/tbody/tr')
# 		print(trs)
# 		for tr in trs[:]:
# 			ip = tr.xpath('td[1]/text()')[0] + ':' + tr.xpath('td[2]/text()')[0]
# 			print(ip)
# 	time.sleep(random.random() * 5)

# print('获取kxdaili代理：')
# for page in range(1):
# 	url = 'http://www.iphai.com/' 
# 	# print(url)
# 	headers = {
# 		'User-Agent': ua.random
# 	}
# 	rsp = requests.get(url, headers=headers)
# 	print(rsp)
# 	# print(rsp.text)
# 	if rsp.status_code == 200:
# 		doc = etree.HTML(rsp.text)
# 		trs = doc.xpath('//div[@class="table-responsive module"]/table/tr')
# 		print(trs)
# 		for tr in trs[1:]:
# 			ip = tr.xpath('td[1]/text()')[0].replace('\n', '').replace('\t','').replace('\r','').replace(' ','') + ':' \
# 			+ tr.xpath('td[2]/text()')[0].replace('\n', '').replace('\t','').replace('\r','').replace(' ','')
# 			print(ip)
# 	# time.sleep(random.random() * 5)



# print('获取89ip代理：')
# for page in range(1):
# 	url = 'http://www.89ip.cn/tqdl.html?num=500&address=&kill_address=&port=&kill_port=&isp=' 
# 	# print(url)
# 	headers = {
# 		'User-Agent': ua.random
# 	}
# 	rsp = requests.get(url, headers=headers)
# 	print(rsp)
# 	# print(rsp.text)
# 	if rsp.status_code == 200:
# 		doc = etree.HTML(rsp.text)
# 		trs = doc.xpath('//div[@class="layui-col-md8"]/div/div/text()')
# 		# print(trs)
# 		for tr in trs[1:-1]:
# 			print(str(tr).replace(' ', ''))
# 		# for tr in trs[:]:
# 		# 	print(tr.xpath('text()'))
# 		# print(trs.xpath('string(.)'))
# 			# ip = tr.xpath('/text()')#[0].replace('\n', '').replace('\t','').replace('\r','').replace(' ','')
# 			# print(ip)
# 	# time.sleep(random.random() * 5)
