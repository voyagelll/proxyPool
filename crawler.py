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
			# time.sleep(random.random() * 5)


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
			# time.sleep(random.random() * 5)



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
			# time.sleep(random.random() * 5)


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











import re 
# import PyV8 
import requests 
session = requests.Session()



def get_html():
	url = 'http://www.66ip.cn/'
	headers = {
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
		'Accept-Encoding': 'gzip, deflate',
		'Accept-Language': 'zh-CN,zh;q=0.9',
		'Host': 'www.66ip.cn',
		'Proxy-Connection': 'keep-alive',
		'Upgrade-Insecure-Requests': '1',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
	}
	# {'Date': 'Thu, 20 Dec 2018 13:46:45 GMT', 'Content-Type': 'text/html', 'Connection': 'keep-alive', 'Set-Cookie': 'yd_cookie=a01ed4a2-e7e2-443dcd35770c2721a700a773b0bd8c00894d; Expires=1545320805; Path=/; HttpOnly', 'Cache-Control': 'no-cache, no-store', 'content-encoding': 'gzip', 'Content-length': '849', 'Server': 'WAF/2.4-12.1'}

	rsp1 = requests.get(url, headers=headers)
	# print(rsp1.text)
	# print(rsp1.headers)

	js_func = ''.join(re.findall(r'(function .*?)</script>', rsp1.text))
	print('js_func: ', js_func)

	js_arg = ''.join(re.findall(r"setTimeout\(\".*?\"\)", rsp1.text))
	print(js_arg)


if __name__ == '__main__':
	get_html()










# get_html(url)


# def executeJS(js_func_string, arg):
# 	ctxt = PyV8.JSContext()
# 	ctxt.enter()
# 	func = ctxt.eval("{js}".format(js=js_func_string))
# 	return func(arg)


# def parseCookie(string):
# 	string = string.replace("document.cookie=", "")
# 	clearance = string.split(';')[0]
# 	return {clearance.split('=')[0]: clearance.split('=')[1]}


# first_html = get_html(url)
# js_func = ''.join(re.findall(r'(function .*?)</script>', first_html))
# print('js func:', js_func)

# js_arg = ''.join(re.findall(r'setTimeout\(\"\D+\((\d+)\)\"', first_html))

# cookie_str = executeJS(js_func, js_arg)
# cookie = parseCookie(cookie_str)
# print(cookie)
# print(get_html(url, cookie))



# function gu(VG) {
#     var qo, mo = "",
#     no = "",
#     oo = [0xae, 0x04, 0x09, 0x84, 0xf4, 0x6f, 0x6a, 0xe2, 0xdd, 0xcd, 0xaa, 0x24, 0xb6, 0x32, 0xad, 0x2b, 0xa9, 0x22, 0xdc, 0x2f, 0x88, 0x0c, 0x82, 0x7a, 0xe0, 0x5a, 0x56, 0xce, 0x47, 0x3a, 0x1a, 0x94, 0x8f, 0x09, 0x81, 0xd5, 0x00, 0x79, 0x72, 0x42, 0x11, 0x0a, 0x46, 0x9c, 0x94, 0x0d, 0x5f, 0xda, 0xc0, 0x11, 0x62, 0x32, 0x88, 0x02, 0x0a, 0x59, 0xa9, 0x22, 0x71, 0xc3, 0x2e, 0x04, 0xd6, 0x2b, 0x24, 0x80, 0x30, 0x82, 0x7b, 0xd1, 0x4a, 0xa6, 0x4e, 0x1e, 0x6d, 0x65, 0x35, 0x91, 0x75, 0x4b, 0x1d, 0xef, 0xe8, 0x43, 0x8e, 0x08, 0xd7, 0x28, 0xfd, 0x76, 0xdf, 0x30, 0x86, 0x7f, 0xcf, 0xc8, 0xb9, 0x8c, 0x5b, 0xb7, 0x0a, 0x5a, 0x19, 0xea, 0x39, 0x8c, 0xde, 0x2f, 0xa3, 0x79, 0xcf, 0xa5, 0xfc, 0xd6, 0xd8, 0x4f, 0x45, 0x37, 0xb5, 0xa8, 0x14, 0x8c, 0xfd, 0x52, 0x52, 0x50, 0xb8, 0x27, 0x03, 0xde, 0xaf, 0x81, 0x15, 0x71, 0x79, 0xf1, 0x6b, 0xc7, 0xd2, 0x23, 0xfa, 0xd4, 0x25, 0x78, 0x50, 0x25, 0x77, 0x4d, 0x24, 0x76, 0x32, 0x08, 0xe1, 0x69, 0xf5, 0xf5, 0x42, 0x97, 0x71, 0x69, 0xe6, 0x61, 0x9b, 0x16, 0x94, 0x8f, 0xe3, 0xc0, 0x3b, 0x0c, 0xdc, 0x59, 0x4b, 0x28, 0x2f, 0xaa, 0xa5, 0xfc, 0xd6, 0xc8, 0xdd, 0x58, 0x48, 0x46, 0x9a, 0xf5, 0x5a, 0xb1, 0x07, 0xe2, 0x52, 0xd0, 0x1f, 0x1c, 0x14, 0x8f, 0x00, 0xdb, 0x44, 0x3c, 0xb7, 0x31, 0xa1, 0x1e, 0x89, 0x02, 0xfe, 0xee, 0xc9, 0xc5, 0xb3, 0x2f, 0xaa, 0x23, 0x13, 0x91, 0xf3, 0x6f, 0x6c, 0xc0, 0xb8, 0x34, 0x7f, 0xfa, 0x69, 0xe5, 0x5e, 0x59, 0x86, 0x76, 0x51, 0xd1, 0xd4, 0xe0, 0xee, 0x3b];
#     qo = "qo=234; do{oo[qo]=(-oo[qo])&0xff; oo[qo]=(((oo[qo]>>1)|((oo[qo]<<7)&0xff))-185)&0xff;} while(--qo>=2);";
#     eval(qo);
#     qo = 233;
#     do {
#         oo[qo] = (oo[qo] - oo[qo - 1]) & 0xff;
#     } while (-- qo >= 3 );
#     qo = 1;
#     for (;;) {
#         if (qo > 233) break;
#         oo[qo] = ((((((oo[qo] + 146) & 0xff) + 213) & 0xff) << 2) & 0xff) | (((((oo[qo] + 146) & 0xff) + 213) & 0xff) >> 6);
#         qo++;
#     }
#     po = "";
#     for (qo = 1; qo < oo.length - 1; qo++) if (qo % 6) po += String.fromCharCode(oo[qo] ^ VG);
#     eval("qo=eval;qo(po);");
# }
