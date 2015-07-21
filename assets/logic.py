#!/usr/bin/python
#coding=utf-8

"""
auth:wuqichao
mail:wuqichao@playcrab.com
createtime:2014-7-10下午2:24:30
usege:

"""
from db_config import session
from models import *


class logic_idc(object):


    @staticmethod
    def save(param):
        try:
            # 创建新User对象:
            new_user =IDC( name=param['name'],prefix=param['prefix'])
            session.add(new_user)
            session.commit()
        except:
            session.rollback()
            

    @staticmethod
    def get_by_prefix(prefix):

        return session.query(User).filter("prefix=:prefix").params(prefix=prefix).all() 

    @staticmethod
    def get_by_id(id):
        
        return session.query(User).filter("id=:id").params(id=id).all() 

    @staticmethod
    def get_idcs(idc):
        return  session.query(IDC)




class logic_asset(object):


    @staticmethod
    def save(param):
        try:
            # 创建新User对象:
            new_asset =Asset( sn=param['wxsn'], purchase_date=param['purchase_date'], idc_id =param['idc_id'], is_virtual =1)
            session.add(new_asset)
            session.flush()
            session.commit()

            return new_asset.id
        except:
            session.rollback()

    @staticmethod
    def get_by_prefix(prefix):

        return session.query(Asset).filter("prefix=:prefix").params(prefix=prefix).all() 

    @staticmethod
    def get_by_id(id):
        
        return session.query(Asset).filter("id=:id").params(id=id).all() 

    @staticmethod
    def get_idcs(idc):
        return  session.query(Asset)




class logic_ip(object):


    @staticmethod
    def save(param):
        try:
            # 创建新User对象:
            new_ip =IP( outer_ip=param['outer_ip'],inner_ip=param['inner_ip'],idc_id =param['idc_id'])
            session.add(new_ip)
            session.flush()
            session.commit()

            return new_ip.id
        except:
            session.rollback()

    @staticmethod
    def get_by_prefix(prefix):

        return session.query(IP).filter("prefix=:prefix").params(prefix=prefix).all() 

    @staticmethod
    def get_by_id(id):
        
        return session.query(IP).filter("id=:id").params(id=id).all() 

    @staticmethod
    def get_idcs(idc):
        return  session.query(IP)




class logic_idc_op_ship(object):


    @staticmethod
    def save(param):
        try:
            # 创建新User对象:
            new_idc_op_ship =idc_op_ship( asset_id=param['asset_id'],cabinet_id= 0 , game_id=0 , cluster_id = 0, idc_id =param['idc_id'], ip_id = param['ip_id'])
            session.add(new_idc_op_ship)
            session.flush()
            session.commit()

            return new_idc_op_ship.id
        except:
            session.rollback()

    @staticmethod
    def get_by_prefix(prefix):

        return session.query(idc_op_ship).filter("prefix=:prefix").params(prefix=prefix).all() 

    @staticmethod
    def get_by_id(id):
        
        return session.query(idc_op_ship).filter("id=:id").params(id=id).all() 

    @staticmethod
    def get_idcs(idc):
        return  session.query(idc_op_ship)




class logic_sys_op_ship(object):


    @staticmethod
    def save(param):
        try:
            new_sys_op_ship=sys_op_ship( asset_id=param['asset_id'], game_id=0 , cluster_id = 0, services_id =0, ip_id = param['ip_id'])
            session.add(new_sys_op_ship)
            session.flush()
            session.commit()

            return new_sys_op_ship.id
        except:
            session.rollback()

    @staticmethod
    def get_by_prefix(prefix):

        return session.query(sys_op_ship).filter("prefix=:prefix").params(prefix=prefix).all() 

    @staticmethod
    def get_by_id(id):
        
        return session.query(sys_op_ship).filter("id=:id").params(id=id).all() 

    @staticmethod
    def get_idcs(idc):
        return  session.query(sys_op_ship)
