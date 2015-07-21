#!/usr/bin/python
#coding=utf-8

import sys,os
import commands,subprocess
from custom.config.ini import DictConfigParser
import sys,os
import urllib, urllib2
import random
import base64
import hmac
import hashlib
from hashlib import sha1
import time
import uuid
import json
from urllib2 import  URLError
ini_path = os.path.join(os.path.abspath('./config/'),'yun_config')

ini_section_key  ='qcloud'

def get(url,**headers):
    
    httpHandler = urllib2.HTTPHandler(debuglevel=0)
    httpsHandler = urllib2.HTTPSHandler(debuglevel=0)
    opener = urllib2.build_opener(httpHandler, httpsHandler)

    urllib2.install_opener(opener)
    req = urllib2.Request(url)

    if headers:
        for k in headers.keys():
            req.add_header(k,headers[k])

    try:
        response = urllib2.urlopen(req)
        data = response.read()
        return json.loads("".join(data))
        
    except URLError, e:
        print e.code
        print e.read()

def get_rand():
    
    seed ='123456789'  
    r = []
    for i in range(10):
        r.append(random.choice(seed))
    salt=''.join(r)
 
    return int(salt)

def create_str2Sig(body,method,uri,secrectId,nonce,timestamp):
    '''
    生成参数串
    '''
    arr2Sig = [
        "body="+body,
        "method="+method,
        "uri="+uri,
        "x-txc-cloud-secretid="+str(secrectId),
        "x-txc-cloud-nonce="+str(nonce),
        "x-txc-cloud-timestamp="+str(timestamp),
    ]
   

    str2Sig = "&".join(arr2Sig)
    return str2Sig

def create_signature(secretKey, str2Sig):
    '''
    生成签名
    '''
    h = hmac.new(secretKey, str2Sig, sha1)
    signature = base64.encodestring(h.digest()).strip()
    return signature

def create_header(secrectId,nonce,timestamp,signature):
    '''
    生成header
    '''
    return {
        "Content-type": " application/json; charset=utf-8",
        "x-txc-cloud-secretid":secrectId,
        "x-txc-cloud-nonce":str(nonce),
        "x-txc-cloud-timestamp":timestamp,
        "x-txc-cloud-signature":signature
    }
    

def get_cvms():

    
    
    n = DictConfigParser(ini_path)
    access_key_id = n[ini_section_key]['id'].encode('utf-8')
    access_key_secret = n[ini_section_key]['key'].encode('utf-8')
    api_url = n[ini_section_key]['url'].encode('utf-8')

    
    endpoint = api_url
    uri="/v1/cvms"
    method = "GET"
    
     
   
    secrectId = access_key_id
    secretKey = access_key_secret
     
    timestamp =int(time.time())
    #print timestamp
    nonce = get_rand()
    body = ''
     
   

    str2Sig = create_str2Sig(body,method,uri,secrectId,nonce,timestamp)
             

    signature = create_signature(secretKey, str2Sig)

   
    header = create_header(secrectId,nonce,timestamp,signature)
    
    
    
    url="http://"+endpoint+uri

    
    return get(url,**header)['instances']

    