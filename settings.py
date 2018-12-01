#！/usr/bin/env python3
# -*- coding:utf-8 -*-
# redis数据库地址
REDIS_HOST = '127.0.0.1'

# redis端口
REDIS_PORT = 6379

# redis密码
REDIS_PASSWORD = None 

REDIS_KEY = 'proxies'

# 代理分数
MAX_SCORE = 10 
MIN_SCORE = 0 
INITIAL_SCORE = 5

VALID_STATUS_CODES = [200, 302]

# 代理池数量界限
POOL_UPPER_THRESHOLD = 1000

# 检测周期
TESTER_CYCLE = 30  

# 获取周期
GETTER_CYCLE = 500

# 测试API, 抓取哪个测那个
# TEST_URL = 'http://www.nytdc.edu.cn/index.php?m=content&c=index&a=lists&catid=192'
# TEST_URL = 'http://www.ishangzu.com'
# TEST_URL = 'http://school.nihaowang.com'
# TEST_URL = 'https://www.tianyancha.com/'
# TEST_URL = 'https://www.google.com/'
# TEST_URL = 'https://www.baidu.com'
TEST_URL = 'https://m.weibo.cn/'
# TEST_URL = 'https://www.blockchain.com/btc/blocks'

# API配置
API_HOST = '0.0.0.0'
API_PORT = 5555

# 开关
TESTER_ENABLED = True
GETTER_ENABLED = True 
API_ENABLED = True 

# 最大测试批量
BATCH_TEST_SIZE = 100

