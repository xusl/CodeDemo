# -*- coding:utf-8 -*-
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import urllib2, sys, os
import requests
import hashlib
import math
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

server = sys.argv[1] if len(sys.argv) > 1 else '192.168.43.1'
port = sys.argv[2] if len(sys.argv) > 2 else '8087'
baseUrl = "http://%s:%s/" % (server, port)
clientName = "TestPython"
clientId = hashlib.md5("Nobody inspects the spammish repetition").hexdigest()
timeout = 10
'''
request = urllib2.Request(requestUrl, datagen, headers)
# 实际执行请求并取得返回
print urllib2.urlopen(request).read()
'''


def start_line(text):
    begin = int(math.floor((78 - len(text)) / 2))
    right = 78 - 2 - len(text) - begin
    print "-" * begin, text, "-" * right


def stop_line():
    print "-" * 78, '\n'


start_line("Test register")
r = requests.get(baseUrl+"register/", params={"name": clientName, "id": clientId}, timeout=timeout)
sessionToken = r.json()["token"]
print r.json()
stop_line()

params = {"token": sessionToken, "id": clientId}

start_line("Test login")
r = requests.get(baseUrl+"token_request/", params=params, timeout=timeout)
print '"', r.content, '"', r.json()
stop_line()
# exit(1)

start_line("Test request file list")
r = requests.get(baseUrl+"request/", params=params, timeout=timeout)
print r.json()
stop_line()

start_line("Test download file")
for item in r.json():
    reqParams = dict(params)
    reqParams["file_id"] = item["index"]
    print reqParams
    r = requests.get(baseUrl+"get_file/", params=reqParams, timeout=timeout)
    # print r.json()
stop_line()

start_line("Test request get group")
r = requests.get(baseUrl+"get_group/", params=params, timeout=timeout)
print r.json()
stop_line()

start_line("Test upload file API")
file_data = {'file': (os.path.basename(sys.argv[0]), open(sys.argv[0], 'rb'), 'text/plain')}
r = requests.request('post',
                     baseUrl+"put_file/",
                     data = { 'extra_data': "blah blah blah" , "filename": "ohmygood"},
                     json=None,
                     files = file_data)
print r.status_code
print r.headers['content-type']
print r.headers
print r.content
stop_line()

start_line("Test exit API")
r = requests.get(baseUrl+"share_exit/", params=params, timeout=timeout)
print r.content
