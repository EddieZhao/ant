#/usr/bin/python evn
#coding=utf-8

"""
auth:wuqichao
mail:wuqichao@playcrab.com
createtime:2014-7-9上午11:26:08
usege:

"""

import json
from threading import  Thread


from api_base import get_cvms




__ALL__ =['API']

class API(Thread):
    '''
    
    '''

    def __init__(self,func,**param):
        super(API,self).__init__()
        self.func = func
        self.param = param
        self.result = []
        
    def  run(self):
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
        
        
       
        result = get_cvms()

        if result!=[]:
#             print result
            for i in result:
            
                param={}
                param['public_ip'] = i['instanceInfo']['wanIp']
                param['hostname']  = str(i['instanceId'])
                param['wxsn']      = str(i['instanceId'])
                param['inner_ip']  = i['instanceInfo']['lanIp']
                param['purchase_date'] = '0000-00-00 00:00:00'      
                param['idc_id']    = idc_dict['idc_id']
                self.result.append(param)
                
            return self.result
        
    
    def get_idcs(self):
        '''
        获取idc信息
        '''
        return []
            
    def get_balancers(self,**idc_dict):

        return []
                
    def get_result(self):
        
        return self.result


