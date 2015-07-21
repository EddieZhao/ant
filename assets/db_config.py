#!/usr/bin/python
#coding=utf-8

"""
auth:wuqichao
mail:wuqichao@playcrab.com
createtime:2014-7-10下午2:24:30
usege:

"""
from sqlalchemy import create_engine
from sqlalchemy.orm import mapper, sessionmaker

DB_CONNECT_STRING = 'mysql+mysqldb://remote:1q2w3e4r@192.168.56.102/ant?charset=utf8'
engine = create_engine(DB_CONNECT_STRING, echo=False)
DB_Session = sessionmaker(bind=engine)
session = DB_Session()