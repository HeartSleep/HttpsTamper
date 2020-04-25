from mitmproxy import http
import urllib,re,hashlib
import json
from pprint import pprint

import base64

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
rsa_obj = RSA.generate(1024)
private_pem = rsa_obj.exportKey()
public_key = rsa_obj.publickey()
public_pem = public_key.exportKey()


'''
requst ref
https://github.com/mitmproxy/mitmproxy/blob/3cd37652709292cffa1bc733134cef5483489341/mitmproxy/http.py
'''


pub="-----BEGIN PUBLIC KEY-----\r\n" +\
				"MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDOrprzzIrzSMRDLNHVZpQCrfBp\r\n" + \
				"ZVIZ9B9cW/5pFo0DqZPmTYnsf6lwTvMwUyWj+FDkf7k6LiTW82c8QNSbQrPU1WaE\r\n" + \
				"5tVs5Bzc+SJizAhPCJ6UAlJKAcDvz8eWFX9kMV6IPIoOJ2gwDjY12V2WSeuzcUeW\r\n" + \
				"6oB0bLDWYfR23c5XgwIDAQAB\r\n" + \
				"-----END PUBLIC KEY-----\r\n"
public_key = RSA.importKey(pub)

def rsa_long_encrypt(pub_key_str, msg, length=117):

    pubobj = Cipher_pkcs1_v1_5.new(pub_key_str)
    res = bytearray()
    for i in range(0, len(msg), length):
        t=msg[i:i+length]
        a=pubobj.encrypt(bytes(t,'utf-8'))
        res.extend(a)
    return res



def request(flow: http.HTTPFlow) -> None:

    print(flow.request.host)
    if 'api.kxxuai' in flow.request.host:
        #if "POST"== flow.request.method:
        #    pass
        #if "GET" ==flow.request.method:
            #get hooked plain text
        print(11)
        if "_param" in flow.request.query.keys():

            message=flow.request.query['_param']
            obj=json.loads(message)
            originstr=""
            for k in obj.keys():
                originstr=originstr+k+"="+obj[k]+"&"
            originstr=originstr[0:-1]
            print(originstr)
            input1 = rsa_long_encrypt(public_key, originstr)
            basestr = base64.b64encode(input1)
            print(basestr)
            flow.request.query['_param']=basestr



