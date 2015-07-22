#!/usr/bin/python
#coding=utf-8

"""
auth:wuqichao
mail:wuqichao@playcrab.com
createtime:2014-7-10下午2:24:30
usege:

"""


from sqlalchemy import create_engine
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import CHAR, Integer, String, DATETIME, DATE
from sqlalchemy.ext.declarative import declarative_base
from db_config import *


BaseModel = declarative_base()


class IDC(BaseModel):
    '''
    机房区域表，机房简称＋区域 唯一
    '''
    __tablename__ = 'idc'
    __table_args__=(
        UniqueConstraint('prefix','name',name='uniq_idc_region'),
        {'mysql_engine': 'InnoDB'}
        )

    id = Column(Integer, primary_key=True)
    name = Column(String(30)) 
    prefix = Column(String(30), nullable=False, unique=True)
    network_type = Column(String(30), nullable=False, default =0)
    is_delete = Column(Integer(), nullable=False, default =0)

class Cabinet(BaseModel):
    '''
    机柜表，它隶属于idc表,用于idc运维使用
    '''
    __tablename__ = 'cabinet'

    
    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False) 
    prefix = Column(String(30), nullable=False)
    idc_id = Column(Integer(), ForeignKey('idc.id'), nullable=False)
    is_delete = Column(Integer(), nullable=False, default =0)


class Game(BaseModel):
    '''
    游戏表，英文代号唯一
    '''
    __tablename__ = 'game'

    
    id = Column(Integer, primary_key=True)
    name = Column(String(30)) 
    prefix = Column(String(30), nullable=False, unique=True)
    types = Column(Integer(), nullable=False) 
    is_delete = Column(Integer(), nullable=False, default =0)

class Cluster(BaseModel):
    '''
    集群表，它隶属于游戏表，用于跟游戏相关的服务器管理使用,游戏＋集群代号 唯一
    '''
    __tablename__ = 'cluster'

    __table_args__=(
        UniqueConstraint('prefix','game_id',name='uniq_game_cluster'),
        #{'mysql_engine': 'InnoDB'}
        )

    id = Column(Integer, primary_key=True)
    name = Column(String(30)) 
    prefix = Column(String(30), nullable=False)
    game_id = Column(Integer(), ForeignKey('game.id'), nullable=False)
    is_delete = Column(Integer(), nullable=False, default =0)




class Services(BaseModel):
    '''
    游戏服务表，它隶属于集群表，用于跟游戏相关的服务器上的服务管理使用(如mysql mongo redis 游戏进程 聊天服务 排行服务)
    '''
    __tablename__ = 'services'

    
    id = Column(Integer, primary_key=True)
    name = Column(String(30)) 
    prefix = Column(String(30), nullable=False)
    types = Column(Integer(), nullable=False) 
    location = Column(String(50), nullable=False)
    port   = Column(Integer(), nullable=True)
    config = Column(String(50), nullable=False)
    data = Column(String(50), nullable=False)
    is_delete = Column(Integer(), nullable=False, default =0)


class Dist(BaseModel):
    '''
    区组表，它隶属于游戏表,用于根游戏相关的数据查询用
    '''
    __tablename__ = 'dist'

    
    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False) 
    prefix = Column(String(30), nullable=False)
    game_id = Column(Integer(), ForeignKey('game.id'), nullable=False)
    is_delete = Column(Integer(), nullable=False, default =0)




class Asset(BaseModel):
    '''
    资产表，sn资产唯一标识，可含有业务含义
    '''
    __tablename__ = 'asset'
    __table_args__=(
        UniqueConstraint('idc_id','sn',name='uniq_idc_sn'),
        {'mysql_engine': 'InnoDB'}
        )

    id = Column(Integer, primary_key=True)
    sn     = Column(String(50), nullable=False, unique=True)
    idc_id = Column(Integer(), ForeignKey('idc.id'), nullable=False)
    is_virtual = Column(Integer(), nullable=False, default =0)
    purchase_date = Column(DATETIME(), nullable=False)
    is_delete = Column(Integer(), nullable=False, default =0)



class IP(BaseModel):
    '''

    '''
    __tablename__ = 'ip'
 

    id = Column(Integer, primary_key=True)
    idc_id = Column(Integer(), ForeignKey('idc.id'), nullable=False)
    inner_ip = Column(String(50))
    outer_ip = Column(String(50), unique=True)
    is_balancer = Column(Integer(), nullable=False, default =0)
    is_delete = Column(Integer(), nullable=False, default =0)


class sys_op_ship(BaseModel):
    '''
    ip属于哪个游戏哪个集群哪种服务，它所对应的资产信息
    '''
    __tablename__ = 'sys_op_ship'
 

    id = Column(Integer, primary_key=True)
    ip_id = Column(Integer(), ForeignKey('ip.id'), nullable=False)

    game_id = Column(Integer, ForeignKey('game.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    cluster_id = Column(Integer, ForeignKey('cluster.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    services_id = Column(Integer, ForeignKey('services.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)

    asset_id = Column(Integer, ForeignKey('asset.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    is_delete = Column(Integer(), nullable=False, default =0)


class idc_op_ship(BaseModel):
    '''
    资产在哪个idc机房 哪个机柜 属于哪个游戏 哪个集群，ip是多少
    '''
    __tablename__ = 'idc_op_ship'
 
    id = Column(Integer, primary_key=True)
    asset_id = Column(Integer(), ForeignKey('asset.id'), nullable=False)

    idc_id = Column(Integer, ForeignKey('idc.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    cabinet_id = Column(Integer, ForeignKey('cabinet.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)

    game_id = Column(Integer, ForeignKey('game.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    cluster_id = Column(Integer, ForeignKey('cluster.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)

    ip_id = Column(Integer, ForeignKey('ip.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    is_delete = Column(Integer(), nullable=False, default =0)






def init_db(engine):
    BaseModel.metadata.create_all(engine)

def drop_db(engine):
    BaseModel.metadata.drop_all(engine)



if __name__ == '__main__':

    drop_db(engine)
    init_db(engine)
    exit()

