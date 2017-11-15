# -*- coding:utf-8 -*-
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import urllib2, sys, os
import requests
import hashlib

#test 
#python upload.py httpbin.org 80
#Palmplay FreeShare
#python upload.py 192.168.43.1 8087
 
# 在 urllib2 上注册 http 流处理句柄
register_openers()
 
# 开始对文件 "DSC0001.jpg" 的 multiart/form-data 编码
# "image1" 是参数的名字，一般通过 HTML 中的 <input> 标签的 name 参数设置
 
# headers 包含必须的 Content-Type 和 Content-Length
# datagen 是一个生成器对象，返回编码过后的参数
datagen, headers = multipart_encode({"file_upload": open(sys.argv[0], "rb")})
 
# 创建请求对象
print sys.argv

server = sys.argv[1] if len(sys.argv) > 1 else 'localhost'
port = sys.argv[2] if len(sys.argv) > 2 else '8080'
baseUrl = "http://%s:%s/" % (server, port)
clientName = "TestPython"
clientId = hashlib.md5("Nobody inspects the spammish repetition").hexdigest()

if server.startswith("httpbin.org"):
    requestUrl = "http://%s:%s/post" % (server, port)
else:
    requestUrl = "http://%s:%s/" % (server, port)
print requestUrl
'''
request = urllib2.Request(requestUrl, datagen, headers)
# 实际执行请求并取得返回
print urllib2.urlopen(request).read()
''' 

r = requests.get(baseUrl+"register/", params={"name": clientName, "id": clientId})
print r.json()

exit(1)

requests.get(baseUrl+"request/")
requests.get(baseUrl+"token_request/")
requests.get(baseUrl+"get_file/")
requests.get(baseUrl+"get_group/")

#file_data = { 'file': ('test.png', open(sys.argv[0], 'rb'), 'image/png') }
file_data = { 'file': (os.path.basename(sys.argv[0]), open(sys.argv[0], 'rb'), 'text/plain') }
r = requests.post(requestUrl, data = { 'extra_data': "blah blah blah" , "filename": "ohmygood"}, files = file_data)
print r.status_code
print r.headers['content-type']
print r.headers
print r.content

