#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''/**
 * LOG
 *
 * <pre>
 * Modify Information:
 * Author        Date          Description
 * ============ =========== ============================
 * liuwei     2019年06月10日       Create this file
 * </pre>
 */'''
import os,sys,time,random
import platform,hashlib,base64,urllib
import traceback,binascii,hmac
try:
    from Cryptodome.Cipher import DES3
except:
    from Crypto.Cipher import DES3
from gmssl.sm3 import sm3_hash,sm3_kdf 
from gmssl.sm4 import CryptSM4, SM4_ENCRYPT, SM4_DECRYPT
from OpenSSL import crypto
from Crypto import Random,Hash
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES,PKCS1_v1_5
from Crypto.Signature import PKCS1_v1_5 as PKCS1_v1_5_sign
from mylog import MyLogger as myLog
from cryptography.hazmat.primitives.serialization import pkcs12  
#linux python3 pip3 install pycryptodome
#pip install gmssl 国密SM4
#pip install pyOpenSSL

class KeyApi:
    def __init__(self,des='pay'):
        #3DES的key和偏移iv; 入库存储，数据库连接加密的是一般key，接口传输的是bigdata_key
        self.secret_key = {'pay':{'key':'中金支付有限公司', 'iv':'Cpcn1@34'},
                           'bigdata':{'key':'中金融信信融天下', 'iv':'CPCN!@#$'}}
        self.des = des
        #sm4国密默认16位
        key_iv = sm3_kdf("Cpcn1234#".encode('utf8').hex().encode('utf8'), 32)
        self.secret_sm4 = {'key' : bytes.fromhex(key_iv[32:]),
                           'iv' : bytes.fromhex(key_iv[0:32])}                              
        #解密去补位
        self.unpad = lambda s: s[0:-ord(s[-1])]
        #hash算法
        self.hashlib_code = {"md5": hashlib.md5,
                        "sha1": hashlib.sha1,
		     			"sha256": hashlib.sha256,
				    	"sha512": hashlib.sha512}
        
    @myLog()
    def decode(self, _bytes):
        #byte 使用 decode 方法就能转变成 str
        if '3' == sys.version_info.major:
            string = str(_bytes, encoding = "utf8").strip()                   
        else:
            string = str(_bytes).strip()    
        return string
    
    @myLog()
    def encoding(self, _str):
        #str 使用 encode 方法就能转变成 byte 
        _bytes = _str.encode('UTF-8') 
        return _bytes      
    
    @myLog()    
    def pkcs5(self,s):
        """
        #填充函数，使被加密数据的字节码长度是block_size的整数倍 
        #填充方式为Pkcs5Padding 8位
        """
        src = s.encode('UTF-8')
        y = 8 - len(src) % 8
        if y == 0 or y == 8:
            add = '\x08\x08\x08\x08\x08\x08\x08\x08'
        if y == 7:
            add = '\x07\x07\x07\x07\x07\x07\x07'
        if y == 6:
            add = '\x06\x06\x06\x06\x06\x06'
        if y == 5:
            add = '\x05\x05\x05\x05\x05'
        if y == 4:
            add = '\x04\x04\x04\x04'
        if y == 3:
            add = '\x03\x03\x03'
        if y == 2:
            add = '\x02\x02'
        if y == 1:
            add = '\x01'
        s += add
        return s.encode('UTF-8')
    
    @myLog()
    def pkcs7(self,s,block_size=16):
        """
        #填充函数，使被加密数据的字节码长度是block_size的整数倍 
        #填充方式为PKCS7 16位
        """
        str_to_bytes = s.encode('UTF-8')
        padding_len = block_size-len(str_to_bytes)%block_size
        s = s + (chr(padding_len) * padding_len)
        return s.encode("UTF-8")

    @myLog()
    def decrypt(self,cipherText,secretKey,code,hashFunction='',signature=''):
        if hashFunction == 'HMAC':
            result = '不支持解密解码'
        elif hashFunction == 'RSA':
            # 验签 # secretKey publicKey
            if signature:
                result = self._encryptRSA(cipherText,secretKey,code,signature)
            else:    
                result = '不支持解密解码'
        else:
            result = self._decrypt(cipherText,secretKey,code)
        return result 
        
    @myLog()
    def _decrypt(self,cipherText,secretKey,code):
        if code == '3des':
            if len(cipherText.encode('UTF-8')) % 8 == 0:
                if '2' == sys.version_info.major:
                    # DES3的加密模式为CBC, key: 密钥， iv：偏移量
                    desObj = DES3.new(self.secret_key[self.des]['key'], DES3.MODE_CBC, self.secret_key[self.des]['iv'])
                    des_3 = desObj.decrypt(cipherText.decode('hex'))#.decode("utf-8")
                else:
                    desObj = DES3.new(self.secret_key[self.des]['key'].encode('UTF-8'), DES3.MODE_CBC, self.secret_key[self.des]['iv'].encode('UTF-8'))
                    des_3 = desObj.decrypt(bytes.fromhex(cipherText)).decode("utf-8",'ignore')
                result = self.unpad(des_3)    
            else:
                result = '不正确的加密字符' 
        elif code == 'base64':
            des_3 = base64.b64decode(cipherText.encode('utf-8'))
            result = des_3.decode('utf-8')   
        elif code == 'url':
            #对字符串进行url解码
            result = urllib.parse.unquote(cipherText)
        elif code == 'sm4':
            sm4 = CryptSM4()
            _cipherText = base64.b64decode(cipherText)
            sm4.set_key(self.secret_sm4['key'], SM4_DECRYPT)
            # 调用加密方法解密(十六进制的bytes类型)
            des_3 = sm4.crypt_cbc(self.secret_sm4['iv'], _cipherText)
            result = des_3.decode('utf-8', 'ignore')
        elif code == 'rsa':
            # // RSA非对称解密 公钥加密，私钥解密
            _cipherText = base64.b64decode(cipherText.encode('utf-8'))
            private_key = RSA.importKey(secretKey)
            rsa = PKCS1_v1_5.new(private_key)
            result = rsa.decrypt(_cipherText, sentinel=0).decode('utf-8')
        elif code == 'aes256':
            # // AES256对称解密
            if len(secretKey.encode('UTF-8')) % 16 == 0:
                _cipherText = base64.b64decode(cipherText.encode('utf-8'))
                # IV = Random.new().read(16)
                aes = AES.new(secretKey.encode('utf-8'), AES.MODE_ECB)
                des_3 = aes.decrypt(_cipherText).decode("utf-8",errors='ignore')
                result = self.unpad(des_3)
            else:
                result = '不正确的密钥长度'             
        else:
            result = '不支持解密解码'
        return result
     
    @myLog()
    def encrypt(self,plainText,secretKey,code,hashFunction=''):
        if hashFunction == 'HMAC':
            # Hmac算法；第一个参数是密钥key，第二个参数是待加密的字符串，第三个参数是hash函数 
            if code in self.hashlib_code:
                mac = hmac.new(secretKey.encode('utf-8'),plainText.encode('utf-8'),self.hashlib_code[code])
                # result = mac.digest() # 字符串的ascii格式 
                result = mac.hexdigest() # 加密后字符串的十六进制格式           
            else:
                result = '不存在的加密方式'
        elif hashFunction == 'RSA':
            # 数字签名算法；
            result = self._encryptRSA(plainText,secretKey,code)            
        else:
            result = self._encrypt(plainText,secretKey,code)
        return result                                 

    @myLog()
    def _encryptRSA(self,plainText,secretKey,code,signature=''):
        if code in self.hashlib_code:
            secret_key = RSA.importKey(secretKey)
            signer = PKCS1_v1_5_sign.new(secret_key)
            # SHA1withRSA    
            hash_obj = self.hashlib_code[code](plainText.encode('utf-8'))        
            if signature:
                # 验签 secretKey publicKey #返回 True/False
                sign = bytes.fromhex(signature)
                result = signer.verify(hash_obj,sign)
            else:
                # 签名 secretKey privateKey
                sign_bytes = signer.sign(hash_obj) # bytes
                result = self.bytes2hex(sign_bytes)#.hex().upper()
        elif code == 'rsa':
            # java和python加密后不一致，问题关键是在填充(padding)算法不一样
            secret_key = RSA.importKey(secretKey)
            # RSA非对称加密 secretKey publicKey
            rsa = PKCS1_v1_5.new(secret_key)
            rsaMsg = rsa.encrypt(plainText.encode('utf-8'))
            result = base64.b64encode(rsaMsg).decode('utf-8')
        else:
            result = '不存在的加密方式'    
        return result

    @myLog()
    def _encrypt(self,plainText,secretKey,code):
        if code in self.hashlib_code:
            # 哈希算法
            m=self.hashlib_code[code](plainText.encode('utf-8'))
            result = m.hexdigest()  
        elif code == '3des':
            if '2' == sys.version_info.major:
                desObj = DES3.new(self.secret_key[self.des]['key'], DES3.MODE_CBC, self.secret_key[self.des]['iv'])            
                result = desObj.encrypt(self.pkcs5(plainText)).encode('hex').upper() 
            elif '3.4' in sys.version:
                desObj = DES3.new(self.secret_key[self.des]['key'].encode('UTF-8'), DES3.MODE_CBC, self.secret_key[self.des]['iv'].encode('UTF-8'))
                a_bytes = desObj.encrypt(self.pkcs5(plainText))
                result = (''.join(['%02x' % b for b in a_bytes])).upper()
            else:
                desObj = DES3.new(self.secret_key[self.des]['key'].encode('UTF-8'), DES3.MODE_CBC, self.secret_key[self.des]['iv'].encode('UTF-8'))
                result = desObj.encrypt(self.pkcs5(plainText)).hex().upper()           
        elif 'sm3' in code:
            if code == 'unionsm3':
                lenth = str(len(plainText)) if len(plainText)!='' else ''
                plainText = lenth + plainText
            msg = [i for i in bytes(plainText.encode('UTF-8'))] 
            result = sm3_hash(msg).upper() 
        elif code == 'base64':
            des_3 = base64.b64encode(plainText.encode('utf-8'))
            result = des_3.decode('utf-8')
        elif code == 'url':
            # 编码算法；#对字符串进行url编码
            result = urllib.parse.quote(plainText.encode('utf-8'))       
        elif code == 'sm4':
            # 调用加密方法加密(十六进制的bytes类型)
            sm4 = CryptSM4()
            sm4.set_key(self.secret_sm4['key'], SM4_ENCRYPT)
            des_3 = sm4.crypt_cbc(self.secret_sm4['iv'], plainText.encode('utf-8'))
            result = base64.b64encode(des_3).decode('utf-8', 'ignore') 
        elif code == 'rsa':
            # // RSA非对称加密 public_key
            result = self._encryptRSA(plainText,secretKey,code)
        elif code == 'aes256':
            # AES256对称加密
            if len(secretKey.encode('UTF-8')) % 16 == 0:
                _plainText = self.pkcs7(plainText)
                # IV = Random.new().read(16)
                aes = AES.new(secretKey.encode('utf-8'), AES.MODE_ECB)
                des_3 = aes.encrypt(_plainText)
                result = base64.b64encode(des_3).decode('utf-8')
            else:
                result = '不正确的密钥长度'           
        else:
            result = '不存在的加密方式'
        return result
    
    @myLog()
    def encryptMd5File(self,filename,buffer = 100*1024*1024):
        if not os.path.isfile(filename):  
            return self.encrypt(filename,secretKey='',code='md5')
        else:
            f_name = os.path.basename(filename)
            f_size = os.stat(filename).st_size
            m = hashlib.md5()
            with open(filename,'rb') as fileObj:
                if f_size < buffer:
                    m.update(fileObj.read())   
                else:
                    while(f_size > buffer):
                        tmp_data = fileObj.read(buffer)
                        m.update(tmp_data)
                        f_size/=buffer
                    if(f_size>0) and (f_size<=buffer):
                        m.update(fileObj.read())                    
            return m.hexdigest(),f_size,f_name

    @myLog()
    def getPublicKey(self,cert_path):
        # 从CERT证书中提取公钥, 证书序列号
        with open(cert_path, 'rb') as f:
            data = f.read()
        x509Cert = crypto.load_certificate(crypto.FILETYPE_PEM, data)
        pubkey = x509Cert.get_pubkey()
        public_key = crypto.dump_publickey(crypto.FILETYPE_PEM, pubkey).decode("utf-8").strip()
        encryptSN = x509Cert.get_serial_number()
        return public_key, encryptSN
        
    @myLog()
    def getPrivateKey(self,pfx_path,password):
        # 从PFX证书中提取私钥和证书序列号，如果证书已加密，需要输入密码
        with open(pfx_path, 'rb') as f:
            data = f.read()        
        #x509Pfx = crypto.load_pkcs12(data, password)
        x509Pfx = pkcs12.load_pkcs12(data, password)
        prikey = x509Pfx.get_privatekey()
        private_key = crypto.dump_privatekey(crypto.FILETYPE_PEM, prikey).decode("utf-8").strip()
        signSN = x509Pfx.get_certificate().get_serial_number()
        return private_key, signSN

    @myLog()
    def getCertInfo(self,cert_path):
        # 从CERT证书中提取证书信息
        if not os.path.isfile(cert_path):
            data = cert_path
        else:    
            with open(cert_path, 'rb') as f:
                data = f.read()
        pem = crypto.load_certificate(crypto.FILETYPE_PEM, data)
        x509 = pem.get_subject()
        info = x509.get_components()
        sign = pem.get_signature_algorithm().decode("utf-8")
        sn = pem.get_serial_number()
        starttime = pem.get_notBefore().decode('utf-8')
        start = time.strptime(starttime[:14], "%Y%m%d%H%M%S")
        start = time.strftime("%b %d, %Y %H:%M:%S %p", start)        
        endtime = pem.get_notAfter().decode('utf-8') # 20211012032759Z
        end = time.strptime(endtime[:14], "%Y%m%d%H%M%S") # 先转换为时间数组 后转换为其他格式
        end = time.strftime("%b %d, %Y %H:%M:%S %p", end) # #Oct 12, 2021 03:27:59 AM  
        ex = pem.has_expired()
        cert_info = f"证书DN：CN={x509.CN}, OU={x509.OU}, OU={x509.OU}, O={x509.O}, C={x509.C}\n序列号：{sn}\n签名算法：{sign}\n起始日期：{start}\n结束日期：{end}\n是否过期：{ex}"
        return cert_info

    @myLog()
    def bytes2hex(self,_bytes):
        # 十六进制 和bytes互转 to_bytes: bytes.fromhex("0064")
        # to_hex: data_bytes.hex()
        result = []
        if not _bytes:
            return null
        for i in range(0, len(_bytes)):
            b = '{:X}'.format(_bytes[i] & 0xFF)
            if (len(b) == 1):
                result.append("0")
            result.append(b)
        return ''.join(result).upper()    

