import time

from flask import session
from sqlalchemy import Table
from module.users import Users
from common.database import dbconnect

dbsession, md, DBase = dbconnect()

class Favorite(DBase):
    __table__ = Table('favorite', md, autoload=True)

    # 插入文章收藏数据
    def insert_favorite(self, blogid):
        row = dbsession.query(Favorite).filter_by(blogid=blogid, userid=session.get('userid')).first()
        if row is not None:
            row.canceled = 0
        else:
            # now = time.strftime('%Y-%m-%d %H:%M:%S')
            favorite = Favorite(blogid=blogid, userid=session.get('userid'), canceled=0)
            dbsession.add(favorite)
        dbsession.commit()

    # 取消收藏
    def cancel_favorite(self, blogid):
        row = dbsession.query(Favorite).filter_by(blogid=blogid, userid=session.get('userid')).first()
        row.canceled = 1
        dbsession.commit()

    # 判断是否已被收藏
    def check_favorite(self, blogid):
        row = row = dbsession.query(Favorite).filter_by(blogid=blogid, userid=session.get('userid')).first()
        if row is None:
            return False
        elif row.canceled == 1:
            return False
        else:
            return True



