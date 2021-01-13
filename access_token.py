#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/2
# @Author  : XDN01
# @Site    : www.raosong.cc
# @File    : sent_wexin.py
#-*- coding:utf-8 -*-
from flask import Flask,request
import json
import requests

app = Flask(__name__)
@app.route('/getmsg',methods=['POST'])
def index():
    corpid = "xxxxxxxxxxx"
    secret = "xxxxxxxxxxxxxxxx"
    agentid = "xxxxxxxxx"
    #if request.method == 'GET':
     #   return 'Deny'
     #接收POST的数据
    if request.method == 'POST':
        if request.form.get('checkid') == 'checkid':  # 校验的id，避免有人恶意发送
            GetMsg = request.form.get('msg')
            print(GetMsg)
            wechat = WeChat(corpid, secret, agentid)
            if wechat.send_message(GetMsg) == 1:
                return 'Sent to weixin successed'
            else:
                return 'Failed'
        else:
            return 'Deny'

class WeChat(object):
    def __init__(self, corpid, secret, agentid):
        self.url = "https://qyapi.weixin.qq.com"
        self.corpid = corpid
        self.secret = secret
        self.agentid = agentid

    # 获取企业微信的 access_token
    def access_token(self):
        url_arg = '/cgi-bin/gettoken?corpid={id}&corpsecret={crt}'.format(
            id=self.corpid, crt=self.secret)
        url = self.url + url_arg
        response = requests.get(url=url)
        text = response.text
        self.token = json.loads(text)['access_token']

    # 构建消息格式
    def messages(self, msg):
        values = {
            "touser": '@all',
            # "toparty" : "PartyID1|PartyID2",   # 向这些部门发送  #'@all'给所有的发
            "msgtype": 'text',
            "agentid": self.agentid,
            "text": {'content': msg},
            "safe": 0
        }
        self.msg = (bytes(json.dumps(values), 'utf-8'))


    # 发送信息
    def send_message(self, msg):
        self.access_token()
        self.messages(msg)
        send_url = '{url}/cgi-bin/message/send?access_token={token}'.format(url=self.url, token=self.token)
        response = requests.post(url=send_url, data=self.msg)
        errcode = json.loads(response.text)['errcode']
        if errcode == 0:
            return 1
        else:
            return 0

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8000,debug=True)