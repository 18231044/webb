from flask import session,request
from sqlalchemy import Table
from common.database import dbconnect
import time

from module.blog import Blog
from module.likes import Likes
from module.users import Users

dbsession, md, DBase = dbconnect()

class Comment(DBase):
    __table__ = Table("comment", md, autoload=True)

    # 添加评论
    def insert_comment(self, blogid, content):
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        comment = Comment(userid=session.get('userid'),blogid=blogid,content=content,
                          createtime=now, likes=0, replyid=0)
        dbsession.add(comment)

        dbsession.commit()

    # 根据帖子编号查询评论
    def find_by_blogid(self, blogid):
        result = dbsession.query(Comment).filter_by(blogid=blogid, replyid=0).all()
        return result

    # 按照评论id查找
    def find_by_commentid(self, commentid):
        result = dbsession.query(Comment).filter(Comment.commentid==commentid).first()
        return result

    # 根据用户编号和日期查询今日是否已发五条评论
    def check_limit_comment(self):
        start = time.strftime('%Y-%m-%d 00:00:00')
        end = time.strftime('%Y-%m-%d 23:59:59')
        result = dbsession.query(Comment).filter(Comment.userid==session.get('userid'),
                    Comment.createtime.between(start, end)).all()
        if len(result) >= 5:
            return True     # 不再增加积分
        else:
            return False

    def find_comment_with_user(self, blogid, start, count):
        result = dbsession.query(Comment, Users).join(Users, Users.userid == Comment.userid)\
            .filter(Comment.blogid == blogid).order_by(Comment.commentid.asc())\
            .limit(count).offset(start).all()
        return result

    # 删除评论
    def delete_comment(self, commentid):
        result = dbsession.query(Comment).filter(Comment.commentid==commentid).first()
        dbsession.delete(result)

        dbsession.commit()

    def comment_with_like(self, blogid):
        result = dbsession.query(Comment).join(Likes, Likes.commentid == Comment.commentid) \
            .filter(Comment.blogid == blogid, Likes.userid == session.get('userid')).all()
        return result

    # 增加likes
    def update_like(self, commentid):
        result = dbsession.query(Comment).filter(Comment.commentid == commentid).first()
        result.likes+=1
        dbsession.commit()

    # 新增回复
    def insert_reply(self, blogid, commentid, content):
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        comment = Comment(userid=session.get('userid'),blogid=blogid,content=content,createtime=now,
                          replyid=commentid, likes=0)
        dbsession.add(comment)
        dbsession.commit()

    # 查询所有评论并分页
    def find_all_comment(self, start, count):
        result = dbsession.query(Comment).order_by(Comment.commentid.asc()).limit(count).offset(start).all()
        return result

    # 统计文章总数量
    def get_total_count(self):
        count = dbsession.query(Comment).count()
        return count
