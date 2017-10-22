#!/usr/bin/python
# -*- coding: UTF-8 -*-
from datetime import datetime
import urllib.parse
import urllib.request as urlrequest
import os.path
import os
import time
from random import randint
import socket

socket.setdefaulttimeout(2*60) # wait for maximum two miniutes for downloading the file
PROXY_FILE = './proxies.csv'

with open(PROXY_FILE) as input_proxy_file:
    proxy_list = ['no']
    for line in input_proxy_file:
        proxy_ip, proxy_port = line.split('\t')
        proxy_list.append("{}:{}".format(proxy_ip, proxy_port))

while(True):
	province_list = ['北京市','天津市','上海市','重庆市','河北省','山西省','辽宁省','吉林省','黑龙江省','江苏省','浙江省','安徽省','福建省','江西省','山东省','河南省','湖北省','湖南省','广东省','海南省','四川省','贵州省','云南省','陕西省','甘肃省','青海省','台湾省','内蒙古自治区','广西壮族自治区','西藏自治区','宁夏回族自治区','新疆维吾尔自治区','香港特别行政区','澳门特别行政区']

	currentTime = datetime.now()
	time_str = currentTime.strftime("%Y-%m-%d-%H-%M-%S")
	print("crawl {}...".format(time_str))
	for province in province_list:
		# for proxy_url in proxy_list:
		while(True):
			try:
				# print("try downlaod {} ...".format(proxy_url))
				proxy_url = 'no'
				print("downloading....")
				if proxy_url != 'no':
					# create the object, assign it to a variable
					proxy = urlrequest.ProxyHandler({'https': proxy_url})
					# construct a new opener using your proxy settings
					opener = urlrequest.build_opener(proxy)
				else:
					opener = urlrequest.build_opener()
				opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.1 Safari/603.1.30')]
				# install the openen on the module-level
				urlrequest.install_opener(opener)

				print(province, "...")
				directory = './{}'.format(province)
				if not os.path.exists(directory):
					os.makedirs(directory)
				country_all_url = "https://www.teld.cn/StationNetwork/GetStationNetword?ProvinceName={}&rows=2000".format(urllib.parse.quote(province.encode('utf-8')))
				currentTime = datetime.now()
				time_str = currentTime.strftime("%Y-%m-%d-%H-%M-%S")
				urlrequest.urlretrieve(country_all_url,"./{}/{}.json".format(province, time_str))
				time.sleep(randint(20,30))
				break
			except:
				print("exception, wait 10 miinutes, and try again...")
				time.sleep(10*60)
