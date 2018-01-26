# -*- coding:utf-8 -*-
import fnmatch
import hashlib
import json
import math
import os
import requests
import sys
import urllib

from poster.encode import multipart_encode
from poster.streaminghttp import register_openers

# test
# python upload.py httpbin.org 80
# Palmplay FreeShare
# python upload.py 192.168.43.1 8087

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
imei = u'708784188888888'
mac = u'cb1d622f-03c0-4a59-9cec-7cff3dfd8724'
timeout = 120
chunk_size = 8192
'''
request = urllib2.Request(requestUrl, datagen, headers)
# 实际执行请求并取得返回
print urllib2.urlopen(request).read()
'''

import hashlib
import base64

'''
sha1 file with filename (SHA1)
'''


def SHA1FileWithName(fineName, block_size=64 * 1024):
    with open(fineName, 'rb') as f:
        sha1 = hashlib.sha1()
        while True:
            data = f.read(block_size)
            if not data:
                break
            sha1.update(data)
        return sha1.hexdigest()
        # retsha1 = base64.b64encode(sha1.digest())
        # return retsha1


'''
md5 file with filename (MD5)
'''


def MD5FileWithName(fineName, block_size=64 * 1024):
    with open(fineName, 'rb') as f:
        md5 = hashlib.md5()
        while True:
            data = f.read(block_size)
            if not data:
                break
            md5.update(data)
        return md5.digest()
        # retmd5 = base64.b64encode(md5.digest())
        # return retmd5


def start_line(text):
    begin = int(math.floor((78 - len(text)) / 2))
    right = 78 - 2 - len(text) - begin
    print "-" * begin, text, "-" * right


def stop_line():
    print "-" * 78, '\n'


def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result


def upload_file(file_path, upload_url):
    metadata = {u'size': os.path.getsize(file_path),
                u'index': 0,
                u'name': os.path.basename(file_path),
                u'packageName': u'',
                u'isActived': False,
                u'iconUrl': u'5.7.0.8',
                u'mac': mac,
                u'version': 5708,
                u'isGrp': False,
                u'coin': 0,
                u'type': 6,
                u'senderIMEI': imei,
                u'itemID': SHA1FileWithName(file_path)}
    file_data = {'upload_file': (os.path.basename(file_path), open(file_path, 'rb'), 'text/plain'),
                 # 'file_metadata': (os.path.basename(file_path), open(file_path, 'rb'), 'application/json')
                 }

    upload_response = requests.post(upload_url,
                                    data={'file_metadata': json.dumps(metadata)},
                                    files=file_data,
                                    timeout=timeout)

    # print upload_response.status_code
    # print upload_response.headers['content-type']
    # print upload_response.headers
    print upload_response.content


start_line("Test register")
r = requests.get(baseUrl + "register/", params={"name": clientName, "id": clientId}, timeout=timeout)
sessionToken = r.json()["token"]
print r.json()
stop_line()

params = {"token": sessionToken, "id": clientId}

start_line("Test login")
r = requests.get(baseUrl + "token_request/", params=params, timeout=timeout)
print '"', r.content, '"', r.json()
stop_line()
# exit(1)

start_line("Test request file list")
r = requests.get(baseUrl + "request/", params=params, timeout=timeout)
print r.json()
stop_line()

start_line("Test download file")
for item in r.json():
    reqParams = dict(params)
    reqParams["file_id"] = item["index"]
    print reqParams
    r = requests.get(baseUrl + "get_file/", params=reqParams, timeout=timeout)
    print r.headers
    with open(item["name"], 'wb') as fd:
        for chunk in r.iter_content(chunk_size):
            fd.write(chunk)
            # print r.json()
stop_line()

start_line("Test completed file download")
r = requests.get(baseUrl + "completed/", params=params, timeout=timeout)
print r.content  # , r.text
stop_line()

start_line("Test request get group")
r = requests.get(baseUrl + "get_group/", params=params, timeout=timeout)
print r.json()
stop_line()

start_line("Test upload file API")
upload_url = baseUrl + "put_file/" + "?" + urllib.urlencode(params)
upload_file(sys.argv[0], upload_url)
for share_file in find("*.png", "."):
    upload_file(share_file, upload_url)

stop_line()

start_line("Test exit API")
r = requests.get(baseUrl + "share_exit/", params=params, timeout=timeout)
print r.content  # , r.text
