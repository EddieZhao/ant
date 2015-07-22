#/usr/bin/python
#coding=utf-8

"""
auth:wuqichao
mail:wuqichao@playcrab.com
createtime:2014-6-13 11:55:57
usege:

"""
import time
from pprint import pprint
from threading import  Thread
from multiprocessing import Process
from api_base import UcloudApiClient

__ALL__ =['API']

class API(Thread):
    
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
    
    def get_idcs(self): 
        '''
        ucloud没有提供此接口
        '''

        param ={}
        param['name'] = '北京BGP-A'
        param['prefix']= 'cn-north-01'      
        param['network_type']= '双线'
        self.result.append(param)

        param ={}
        param['name'] = '北京BGP-B'
        param['prefix']= 'cn-north-02'     
        param['network_type']= '双线'
        self.result.append(param)

        param ={}
        param['name'] = '北京BGP-C'     
        param['prefix']= 'cn-north-03'      
        param['network_type']= '双线'
        self.result.append(param)

        param ={}
        param['name'] = '华东双线'       
        param['prefix']= 'cn-east-01'          
        param['network_type']= '双线'
        self.result.append(param)

        param ={}
        param['name'] = '华南双线'       
        param['prefix']= 'cn-south-01'         
        param['network_type']= '双线'
        self.result.append(param)

        param ={}
        param['name'] = '亚太'           
        param['prefix']= 'hk-01'   
        param['network_type']= '国际线路'
        self.result.append(param)

        param ={}
        param['name'] = '北美'           
        param['prefix']= 'us-west-01'  
        param['network_type']= '国际线路'
        self.result.append(param)
           
        return self.result
    
      
    def get_hosts(self,**idc_dict):
        '''
        获取主机内容 
        '''
        idc =  idc_dict['prefix']
        del idc_dict['prefix']
        

        ApiClient = UcloudApiClient()
        Parameters={
                "Action":"DescribeUHostInstance",
                "Region":"%s"%idc,
               }
        result = ApiClient.get("/", Parameters);
        #pprint(result)

 
        for host in result['UHostSet']:
           
            outer_ip = ''
            inner_ip = ''
            print host['IPSet']
            if host['IPSet'][0].get('Type') == u'Private':
                inner_ip = host['IPSet'][0]['IP']

            if host['IPSet'][1].get('Type')  == u'Bgp':
                outer_ip = host['IPSet'][1]['IP']


            param={}
            param['outer_ip']  = outer_ip
            param['hostname']   = host['Name']
            param['wxsn']       = host['UHostId']
            param['inner_ip']   = inner_ip
            param['purchase_date'] = time.strftime('%Y-%m-%d %H:%M:%S',  time.localtime(host['CreateTime']))
            param['idc_id']    = idc_dict['idc_id']
            param['is_del']    = 0 if host['State']=='Running' else 1
            
            self.result.append(param)
            
        return self.result



    def get_balancers(self,**idc_dict):
        
        idc =  idc_dict['prefix']
        del idc_dict['prefix']
        
        ApiClient = UcloudApiClient(region_id =idc)
        result = ApiClient.get('/ulb/vserver', offset=0, max_count=10);
      
        
        if result['ret_code']==0 and result.get('data',None)!=None:
            
            for balancer in result['data']:
                
                
                public_ip = ''
                inner_ip = ''
                
                if balancer.get('public_ips'):
                    public_ip = balancer['public_ips'][0]['ip']
                #保存代理服务器与后端服务器关系    
                children = []
                #pprint(balancer['vserver_infos'][0]['server_infos'])
                for child in  balancer['vserver_infos'][0]['server_infos']:
                    children.append(child['object_id'])
                    
                #print count
                param={}
                param['public_ip'] = public_ip
                param['hostname']  = balancer['vip_name']
                param['wxsn']      = balancer['vip_id']
                param['idc_id']    = idc_dict['idc_id']
                param['children']  = ','.join(children)
                
                self.result.append(param)
        
        return self.result        


    def get_result(self):
        
        return self.result
 
