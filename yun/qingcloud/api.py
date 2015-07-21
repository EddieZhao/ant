#/usr/bin/python evn
#coding=utf-8

"""
auth:wuqichao
mail:wuqichao@playcrab.com
createtime:2014-7-9上午11:26:08
usege:

"""

import json
import socket
from pprint import pprint
from threading import  Thread
from api_base import QingCloudApiBase
import time


__ALL__ =['API']

class API(Thread):
    '''
    
    '''

    def __init__(self,func,**param):
        super(API,self).__init__()
        self.func = func
        self.param = param
        self.result = []
        
    def run(self):
        '''
        任务调度，根据不函数名不同进行任务作业
        '''
        if callable(getattr(self ,self.func)):
            if isinstance(self.param,dict) and self.param !={}:
                self.result = getattr(self, self.func)(**self.param)
            else:
                self.result = getattr(self, self.func)()
        

    def get_hosts(self,**idc_dict):
        '''
        获取主机内容 
        '''
        zone =  idc_dict['prefix']
        
        api = QingCloudApiBase(zone)
        hosts = api.get_describe('instances')
         
        if hosts == None:
            return []

        for info in hosts:
            param = {}
            
            param['public_ip'] = info['eip']['eip_addr'].encode('utf8') if info.has_key('eip') else ''
            param['inner_ip'] = info['vxnets'][0]['private_ip'].encode('utf8')
            param['hostname'] = info['instance_name'].encode('utf8')
            
            purchase_date = time.mktime(time.strptime(info['create_time'].encode('utf8'),"%Y-%m-%dT%H:%M:%SZ"))
            param['purchase_date'] = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(purchase_date))

            param['wxsn'] = info['instance_id'].encode('utf8')
            param['os'] = info['image']['image_id'].encode('utf8')
            
            param['is_del'] = 0 if info['status']=='running' else 1
            
            param['idc_id'] = idc_dict['idc_id']

            self.result.append(param)
            
        return self.result   
        

    def get_idcs(self):
        '''
        获取idc信息
        '''
        param ={}
        param['network_type']=u'双线'
        param['name'] = u'qingcloud[北京一区]'
        param['prefix']= 'pek1'
        self.result.append(param)
        
        
        param ={}
        param['network_type']=u'双线'
        param['name'] = u'qingcloud[北京二区]'
        param['prefix']= 'pek2'
        self.result.append(param) 
        
        
        param ={}
        param['network_type']=u'双线'
        param['name'] = u'qingcloud[广东一区]'
        param['prefix']= 'gd1'
        self.result.append(param) 
        
        param ={}
        param['network_type']=u'双线'
        param['name'] = u'qingcloud[亚太一区]'
        param['prefix']= 'ap1'
        self.result.append(param) 
        
        return self.result
            
    def get_balancers(self,**idc_dict):

        '''
        获取用于负载均衡的机器信息
        '''
        zone =  idc_dict['prefix']
        api = QingCloudApiBase(zone)
        balances  = api.get_describe('loadbalancers')
        
        if balances == None:
            return []
        
        for info in balances:
            children = []
            child_data = api.get_describe('loadbalancer_listeners',info['loadbalancer_id'])[0]
            for instance_info in child_data['backends']:
                children.append(instance_info['resource_id'])
            
            param = {}
            param['public_ip'] = info['eips'][0]['eip_addr'].encode('utf8') if info.has_key('eips') else ''
            param['hostname'] = info['loadbalancer_name'].encode('utf8')
            param['wxsn'] = info['loadbalancer_id'].encode('utf8')
            param['idc_id'] = idc_dict['idc_id']
            param['children']  = ','.join(children)
            
            self.result.append(param)
            
        return self.result
            
    def get_result(self):
        
        return self.result

