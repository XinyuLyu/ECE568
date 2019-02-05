# -*- coding: utf-8 -*-
"""
Created on Sat Apr 21 22:21:46 2018

@author: admin
"""
#!/usr/bin/env python
#  -*- coding:utf-8 -*-
# File http_post.py

import urllib
import urllib2
import json
    
def http_post():
    url='http://192.168.1.13:9999/test'
    values ={'user':'Smith','passwd':'123456}

    jdata = json.dumps(values)             # 对数据进行JSON格式化编码
    req = urllib2.Request(url, jdata)       # 生成页面请求的完整数据
    response = urllib2.urlopen(req)       # 发送页面请求
    return response.read()                    # 获取服务器返回的页面信息

resp = http_post()
print resp
