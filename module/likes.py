from flask import session,request
from sqlalchemy import Table
from common.database import dbconnect
import time
from module.users import Users

dbsession, md, DBase = dbconnect()

class Likes(DBase):
    __table__ = Table("likes", md, autoload=True)

    # 插入一条点赞记录
    def insert_like(self, commentid):
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        like = Likes(userid=session.get('userid'), commentid=commentid, createtime=now)
        dbsession.add(like)
        dbsession.commit()

    # 查询是否点赞过
    def find_like(self, commentid):
        result = dbsession.query(Likes).filter(Likes.userid==session.get('userid'),
                    Likes.commentid==commentid).all()
        if len(result) >= 1:
            return True
        else:
            return False

    # 按照用户id查询今天的点赞记录
    def check_limit_like(self):
        start = time.strftime('%Y-%m-%d 00:00:00')
        end = time.strftime('%Y-%m-%d 23:59:59')
        result = dbsession.query(Likes).filter(Likes.userid == session.get('userid'),
                        Likes.createtime.between(start, end)).all()
        if len(result)>=5:
            return True
        else:
            return False
