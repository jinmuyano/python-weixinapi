#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/12
# @Author  : XDN01
# @Site    : www.raosong.cc
# @File    : weixin.py
#-*- coding:utf-8 -*-
from flask import Flask,request
from WXBizMsgCrypt import WXBizMsgCrypt
import xml.etree.cElementTree as ET
import sys
import config_weixin
# from RedisUtil import RedisUtil
app = Flask(__name__)
@app.route('/weixin', methods=['GET','POST'])   #用来微信-》企业验证，微信用户消息--》企业
def index():
    sToken = config_weixin.sToken         #在企业微信端获取信息
    sEncodingAESKey = config_weixin.sEncodingAESKey
    sCorpID = config_weixin.sCorpID
    wxcpt=WXBizMsgCrypt(sToken,sEncodingAESKey,sCorpID)

    # 获取url验证时微信发送的相关参数
    sVerifyMsgSig=request.args.get('msg_signature')
    sVerifyTimeStamp=request.args.get('timestamp')
    sVerifyNonce=request.args.get('nonce')
    sVerifyEchoStr=request.args.get('echostr')
    #
    sReqMsgSig = sVerifyMsgSig
    sReqTimeStamp = sVerifyTimeStamp
    sReqNonce = sVerifyNonce
    #
    sResqMsgSig = sVerifyMsgSig
    sResqTimeStamp = sVerifyTimeStamp
    sResqNonce = sVerifyNonce
    #验证url
    if request.method == 'GET':
        ret,sEchoStr=wxcpt.VerifyURL(sVerifyMsgSig, sVerifyTimeStamp,sVerifyNonce,sVerifyEchoStr)
        if (ret != 0 ):
            print("ERR: VerifyURL ret:",ret)
            sys.exit(1)
        return sEchoStr

    #接收客户端消息
    if request.method == 'POST':
        sReqMsgSig = sVerifyMsgSig
        sReqTimeStamp = sVerifyTimeStamp
        sReqNonce = sVerifyNonce
        sReqData = request.data

        ret,sMsg=wxcpt.DecryptMsg( sReqData, sReqMsgSig, sReqTimeStamp, sReqNonce)
        if (ret != 0):
            print("ERR: VerifyURL ret:")
            sys.exit(1)

        #解析发送的内容
        xml_tree = ET.fromstring(sMsg)
        content = xml_tree.find("Content").text

        print(content)
        #将接收到的内容记录在文件当中
        f1 = open('weixin_soc_get.txt', 'a')
        f1.writelines(content+"\n")
        f1.close()
        return "OK" # 默认发送三次 ，接收到ok之后就不会重复发送

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)   #与微信通信的api地址
