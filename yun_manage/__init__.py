#/usr/bin/python
#coding=utf-8

"""
auth:wuqichao
mail:wuqichao@playcrab.com
createtime:2014-6-13 11:55:57
usege:

"""

import sys
import json
from assets.db_config import session
from assets.logic import *


class Desc(object):
    "A descriptor example that just demonstrates the protocol"

    def __get__(self, obj, cls=None): 
            pass

    def __set__(self, obj, val):
            pass

    def __delete__(self, obj): 
            pass
                
class yun_manage():
    
    
    data = Desc()
        
         
            
    def save_idcs(self):
        
        if self.data == None:
            return False
        
        print self.data

        for  param in  self.data:
            try:
               
                logic_idc.save(param)
               
            except Exception as e:
                pass

    
            

    def save_hosts(self):
        
        if self.data == None:
            return False

        for param in self.data:
            param['hostname'] = 'game _group_type'
            param['asset_id'] =  logic_asset.save(param)
            param['ip_id'] = logic_ip.save(param)
            logic_idc_op_ship.save(param)
            logic_sys_op_ship.save(param)
                
    def save_balancers(self):
        
        if self.data == None:
            return False
                
        for param in self.data:
#           print param
            #标为负载均衡大类
            print param
            param['asset_id'] =  logic_balancer.save(param)
            param['ip_id'] = logic_ip.save(param)
            
            '''
            param['main_category_id'] = 25
            param['is_balancers'] = 1
            
            sql ='select count(*) as count from assets where wxsn= %s'
            p =(param['wxsn'],)
            count = db.count(sql,*p)
            
            #将负载加到asserts表中
            try:
                parent_id = 0
                if count['count'] ==0:
                    parent_id = db.insert('assets',**param)      
                else:
                    sql ='select id from assets where wxsn= %s and idc_id = %s'
                    p =(param['wxsn'],param['idc_id'],)
                    parent_id = db.get(sql,*p)['id']
                    db.update('assets','wxsn="%s"'%param['wxsn'],**param)
                
                #更新负载与后端实例的关系
                for wxsn in param['children'].encode('utf-8').split(','):
                    updata ={}
                    updata['parent_id'] = parent_id
                    db.update('assets','wxsn="%s"'%wxsn,**updata)
            except Exception as e:
                print e
            '''

                
                    
                        