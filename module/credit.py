from flask import session,request
from sqlalchemy import Table
from common.database import dbconnect
import time


dbsession, md, DBase = dbconnect()

class Credit(DBase):
    __table__ = Table("credit", md, autoload=True)

    # 添加一条经验记录
    def insert_exp(self, type, exp):
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        credit = Credit(userid=session.get('userid'),type=type, createtime=now, exp=exp)
        dbsession.add(credit)
        dbsession.commit()

    # 添加经验记录——
    def insert_exp_user(self, exp, type, userid):
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        credit = Credit(userid=userid, type=type, createtime=now, exp=exp)
        dbsession.add(credit)
        dbsession.commit()
