#/usr/bin/python evn
#coding=utf-8


import os
from  yun.api import api
from  yun_manage import yun_manage 
from assets.logic import logic_idc

def run(yun_name):
    
    
    strat = api(yun_name,'get_idcs')    
    data = strat.get_result()
    
    if data !=None and len(data):
        yun1 = yun_manage()
        yun1.data =data
        yun1.save_idcs()
    
    for idc in logic_idc.get_idcs(yun_name):
        print idc.name,idc.prefix
        param ={}
        param['prefix'] = idc.prefix
        param['idc_id'] = idc.id

        t = api(yun_name,'get_hosts',param)
        data =  t.get_result()
        
        
        if data !=None and len(data):
            print 'host count:',len(data)
            yun1 = yun_manage()
            yun1.data =data
            yun1.save_hosts()
       
    exit()
    for idc in logic_idc.get_idcs(yun_name):
        #print idc
        print idc.name,idc.prefix
        param ={}
        param['prefix'] = idc.prefix
        param['idc_id'] = idc.id

        t = api(yun_name,'get_balancers',param)
        data =  t.get_result()

        if data !=None and len(data):
            yun1 = yun_manage()
            yun1.data =data
            yun1.save_balancers() 

          
if __name__ == '__main__':
    

    yun_list = ['ucloud'] 
    for yun in yun_list:
         
        run(yun)


   
   
