#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''/**
 * CPCN接口请求
 *
 * <pre>
 * Modify Information:
 * Author        Date          Description
 * ============ =========== ============================
 * lw     2022年08月12日       Create this file
 * </pre>
 */'''
import random
import DataCenter as dc
from common import *
from encryptApi import KeyApi
from mylog import MyLogger as myLog

class Cpcn(object):
    def __init__(self):
        self.SECRET_KEY = "5253BEDFE5EF3ACD"
        self.certificateFilepath = r"D:\SVN\R09\20-工作计划\02-自动化测试\02-自动化工具\config\dsptest.cer"
        self.myKeystoreFilepath = r"D:\SVN\R09\20-工作计划\02-自动化测试\02-自动化工具\config\test.pfx"
        self.myKeystorePassword = "cfca1234"   
    
    @myLog()
    def dealOriginJson(self, text, hash_way=''):
        # 根据CPCN处理逻辑，处理 HMAC 加密前的原字符串，非json格式字符不作转换
        if hash_way == "HmacSHA1":
            text_json = dc.formatJson(text, 0, True, 1)
            if isinstance(text_json, dict) and 'error_code' not in text_json:
                _text = []
                for k, v in text_json.items():
                    if v:
                        _text.append(("{0}={1}".format(k,v)).upper())
                text = "&".join(_text)
        return text
    
    @myLog()
    def decodeResponse(self, input_data, cpcn):
        # # 数据系统响应解析
        if cpcn:
            keyway = KeyApi()
            #  请求成功的响应需要aes256解密，而失败的只BASE64
            if ',' in input_data:
                respMsg = input_data.split(",")
                result = self.initEnv(keyway)
                if len(respMsg) < 5 or not all(result):
                    return input_data
                input_data = respMsg[0]
                requestDgtlEnvlp = respMsg[2]
                respEncryptSN = respMsg[4]
                # RSA解密拿到随机密钥 privateKey
                randomKeyData2 = keyway.decrypt(requestDgtlEnvlp, result[1], 'rsa')                
                response = keyway.decrypt(input_data, randomKeyData2, 'aes256')                
            else:
                response = keyway.decrypt(input_data,secretKey='',code='base64')
            if "Traceback (most recent call last)" in response:
                response = input_data
            else:
                result = dc.formatJson(response)
                if "error_code" not in result:
                    response = result         
        else:
            response = input_data        
        return response

    @myLog()
    def randomHexString(self, len=32):
        # 生成AES密钥（随机密钥，len=32）
        result = []
        for i in range(len):
            integer = random.randint(0,15)
            # 随机整数，十进制15，对应16进制的F
            result.append('{:X}'.format(integer)) 
        return ''.join(result).upper()

    @myLog()
    def initEnv(self,keyway):
        publicKey,privateKey,encryptSN,signSN = '','','',''
        if os.path.isfile(self.certificateFilepath):
            certificatePath = self.certificateFilepath
        else:  
            certificatePath = Common().filePath(name='',suffix='.cer',file_path=self.certificateFilepath)
        if os.path.isfile(self.myKeystoreFilepath):
            myKeystorePath = self.myKeystoreFilepath
        else:
            myKeystorePath = Common().filePath(name='',suffix='.pfx',file_path=self.myKeystoreFilepath)
        if certificatePath:
            publicKey,encryptSN = keyway.getPublicKey(certificatePath)
        if myKeystorePath: 
            privateKey,signSN = keyway.getPrivateKey(myKeystorePath,self.myKeystorePassword)
        return publicKey,privateKey,encryptSN,signSN

    @myLog()
    def creatRequest(self,source):
        requestParam = {}
        source_json = dc.formatJson(source)
        keyway = KeyApi()
        # 随机秘钥
        randomKeyData = self.randomHexString()
        # print("随机密钥_source： %s"%randomKeyData)
        result = self.initEnv(keyway)
        if all(result):
            # RSA非对称加密 公钥加密、私钥解密
            dgtlenvlp = keyway.encrypt(randomKeyData, result[0], 'rsa')
            # AES256对称加密
            message =  keyway.encrypt(source_json, randomKeyData, 'aes256')
            # 签名 SHA1withRSA 私钥签名、公钥验签
            signature = keyway.encrypt(source_json,result[1],'sha1','RSA')
            requestParam['message'] = message
            requestParam['signature'] = signature        
            requestParam['dgtlenvlp'] = dgtlenvlp
            requestParam['signSN'] = result[3] 
            requestParam['encryptSN'] = result[2]  
        return requestParam

    @myLog()
    def parseResult(self,requestDgtlEnvlp,requestMessage,sign):
        verifyer = False
        keyway = KeyApi()
        # RSA解密拿到随机密钥 privateKey 
        result = self.initEnv(keyway)
        if all(result):
            randomKeyData2 = keyway.decrypt(requestDgtlEnvlp, result[1], 'rsa')
            randomKeyData3 = bytes.fromhex(randomKeyData2)
            # print("随机密钥_return： " + randomKeyData3)
            decryptMsg = keyway.decrypt(requestMessage, randomKeyData2, 'aes256')
            # print("将消息解密后： " + decryptMsg)
            # 验签 publicKey
            verifyer = keyway.decrypt(decryptMsg, result[0], 'sha1', 'RSA', sign)
        return verifyer

# source='''{
#     "TxCode":"5153",
#     "IdentificationNumber":"7e3ce4844900887c092a41548d7c7740",
#     "EncryptType":"md5",
#     "InstitutionID":"00020",
#     "TxSN":"202208301051513667044706280",
#     "Remark":""
# }'''

# requestParam=Cpcn().creatRequest(source)

# Cpcn().parseResult(requestParam['dgtlenvlp'],requestParam['message'],requestParam['signature'])

