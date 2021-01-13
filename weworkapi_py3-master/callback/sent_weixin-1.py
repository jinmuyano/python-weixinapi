#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/6/2
# @Author  : XDN01
# @Site    : www.raosong.cc
# @File    : sent_wexin.py
#-*- coding:utf-8 -*-
from flask import Flask,request
import json
import requests
import config_weixin


# 发送消息的类
class WeChat(object):
    def __init__(self, corpid, secret, agentid):
        self.url = "https://qyapi.weixin.qq.com"     #微信的发送消息acess_api访问地址
        self.corpid = corpid
        self.secret = secret
        self.agentid = agentid

    # 获取企业微信的 access_token
    def access_token(self):
        url_arg = '/cgi-bin/gettoken?corpid={id}&corpsecret={crt}'.format(
            id=self.corpid, crt=self.secret)
        url = self.url + url_arg
        print(url)
        response = requests.get(url=url)
        print('xxx')
        text = response.text
        print(text)
        self.token = json.loads(text)['access_token']

    # 构建消息格式
    def messages(self, msg):
        values = {
            "touser": '@all',
            # "toparty" : "PartyID1|PartyID2",   # 向这些部门发送  #'@all'给所有的发
            "msgtype": 'text',               #控制消息格式，支持图文消息，视频，markdown
            "agentid": self.agentid,
            "text": {'content': msg},
            "safe": 0
        }
        self.msg = (bytes(json.dumps(values), 'utf-8'))


    # 发送文本信息
    def send_message(self, msg):
        self.access_token()
        self.messages(msg)
        send_url = '{url}/cgi-bin/message/send?access_token={token}'.format(url=self.url, token=self.token)
        print(send_url)
        response = requests.post(url=send_url, data=self.msg)  #发送到是文本消息
        print(json.loads(response.text))
        errcode = json.loads(response.text)['errcode']

        if errcode == 0:   # 消息发送成功
            return 1
        else:
            return 0    #消息发送失败




app = Flask(__name__)
@app.route('/sendmsg',methods=['POST'])      # prom访问这个地址(http://127.0.0.1/sendmsg)，拿到发送的消息内容和企业应用信息,注意访问地址不能加sendmsg/
def index():
    corpid = config_weixin.corpid
    secret = config_weixin.secret
    agentid = config_weixin.agentid
    #if request.method == 'GET':
     #   return 'Deny'
    try:
        data = json.loads(request.data)
        print(data)
        alerts = data['alerts']
        for i in alerts:
            print('SEND SMS: ' + str(i))
            GetMsg=str(i)
            wechat = WeChat(corpid, secret, agentid)
            if wechat.send_message(GetMsg) == 1:  # 发送消息成功
                print("success")
                return 'Sent to weixin successed'
            else:
                print("faild")
                return 'Failed'
    except Exception as e:
        print(e)
        return 'error'
    return 'ok'
     #接收POST的数据
    # if request.method == 'POST':
    #     if request.form.get('checkid') == 'checkid':  # checkid,发送消息时带上验证checkid，校验的id，避免有人恶意发送
    #         GetMsg = request.form.get('msg')          # 从post请求中获取msg
    #         print(GetMsg)
    #         wechat = WeChat(corpid, secret, agentid)
    #         if wechat.send_message(GetMsg) == 1:   # 发送消息成功
    #             print("success")
    #             return 'Sent to weixin successed'
    #         else:
    #             print("faild")
    #             return 'Failed'
    #     else:
    #         print("get")
    #         return 'Deny'



if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5001,debug=True)   #prom连接地址，接收post数据，企业信息和消息
