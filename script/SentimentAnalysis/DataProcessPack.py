#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time
import urllib.request
import urllib.parse
import json
import hashlib
import base64
#接口地址
url ="http://ltpapi.xfyun.cn/v2/sa"
#开放平台应用ID
x_appid = "5fca4198"
#开放平台应用接口秘钥
api_key = "315af78182250a0d0a99e1a406941641"
#语言文本
# TEXT="woc,这也太牛逼了吧"


def get_sentiment(TEXT):
    body = urllib.parse.urlencode({'text': TEXT}).encode('utf-8')
    param = {"type": "dependent"}
    x_param = base64.b64encode(json.dumps(param).replace(' ', '').encode('utf-8'))
    x_time = str(int(time.time()))
    x_checksum = hashlib.md5(api_key.encode('utf-8') + str(x_time).encode('utf-8') + x_param).hexdigest()
    x_header = {'X-Appid': x_appid,
                'X-CurTime': x_time,
                'X-Param': x_param,
                'X-CheckSum': x_checksum}
    req = urllib.request.Request(url, body, x_header)
    result = urllib.request.urlopen(req)
    result = result.read()
    print(result.decode('utf-8'))
    return eval(result.decode('utf-8'))


if __name__ == '__main__':
    TEXT = "我很不开心"
    data = get_sentiment(TEXT)
    print(data)
    print(type(data))
    print(data['data']['score'])
    print(data['data']['sentiment'])
    print(data["desc"])
    print(data['sid'])
