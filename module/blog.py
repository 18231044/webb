import time

from flask import session
from sqlalchemy import Table

from module.favourite import Favorite
from module.users import Users
from common.database import dbconnect

dbsession, md, DBase = dbconnect()

class Blog(DBase):
    __table__ = Table('blog', md, autoload=True)

    # 查询所有帖子
    def find_all(self):
        result = dbsession.query(Blog).all()
        return result

    # 根据帖子id查询
    def find_by_blogid(self, blogid):
        row = dbsession.query(Blog).filter(Blog.blogid == blogid, Blog.hidden == 0).first()
        return row

    # 根据id查询帖子  (Blog, nickname)
    def find_by_id(self, blogid):
        row = dbsession.query(Blog, Users.nickname, Users.exp).join(Users, Users.userid == Blog.userid)\
        .filter(Blog.blogid == blogid, Blog.hidden == 0).first()
        return row

    # 指定分页的limit和offset的参数，同时与用户表做连接查询
    def find_limit_with_users(self, start, count):
        result = dbsession.query(Blog, Users).join(Users, Users.userid == Blog.userid) \
            .filter(Blog.hidden == 0).order_by(Blog.updatetime.desc()).limit(count).offset(start).all()
        return result

    # 查询所有文章并分页
    def find_all_blog(self, start, count):

        result = dbsession.query(Blog).order_by(Blog.blogid.asc()).limit(count).offset(start).all()
        return result

    # 统计文章总数量
    def get_total_count(self):
        count = dbsession.query(Blog).filter(Blog.hidden==0).count()
        return count

    # 统计帖子总数量（包括隐藏）
    def get_total_blog_count(self):
        count = dbsession.query(Blog).count()
        return count

    # 按帖子分区获取
    def find_by_type(self, type, start, count):
        result = dbsession.query(Blog, Users).join(Users, Users.userid == Blog.userid,) \
            .filter(Blog.hidden == 0, Blog.type==type).order_by(Blog.updatetime.desc()).limit(count)\
            .offset(start).all()
        return result

    # 统计相同帖子类型的总数
    def get_count_by_type(self, type):
        count = dbsession.query(Blog).filter(Blog.hidden==0, Blog.type==type).count()
        return count

    # 根据文章标题模糊搜索
    def find_by_headline(self, headline, start, count):
        result = dbsession.query(Blog, Users).join(Users, Users.userid == Blog.userid, )\
            .filter(Blog.hidden == 0, Blog.headline.like('%'+headline+'%')).\
            order_by(Blog.updatetime.desc()).limit(count).offset(start).all()
        return result

    # 统计搜索总数量
    def get_count_by_headline(self, headline):
        count = dbsession.query(Blog).filter(Blog.hidden == 0, Blog.headline.like('%'+headline+'%')).count()
        return count

    # 按用户ID查询其发布的帖子
    def get_blog_by_userid(self):
        result = dbsession.query(Blog).filter(Blog.userid==session.get('userid'), Blog.hidden==0).all()
        return result

    # 删除(隐藏)帖子
    def hide_blog(self, blogid):
        row = dbsession.query(Blog).filter(Blog.blogid==blogid).first()
        row.hidden=1
        dbsession.commit()

    # 恢复显示帖子
    def cancel_hide_blog(self, blogid):
        row = dbsession.query(Blog).filter(Blog.blogid == blogid).first()
        row.hidden = 0
        dbsession.commit()

    # 发布帖子
    def write_blog(self, headline, type, content, level):
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        blog = Blog(headline=headline, content=content, type=type, createtime=now, updatetime=now, level=level,
                    hidden=0, userid=session.get('userid'), replycount=0)
        dbsession.add(blog)
        dbsession.commit()

    # 更新帖子回复数及时间
    def update_blog(self, blogid):
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        result = dbsession.query(Blog).filter_by(blogid=blogid).first()
        result.replycount = result.replycount + 1
        result.updatetime = now
        dbsession.commit()

    # 减少回复数
    def reduce_blog_comment(self, blogid):
        result = dbsession.query(Blog).filter_by(blogid=blogid).first()
        result.replycount = result.replycount - 1
        dbsession.commit()

    # 查询用户今日发帖数
    def check_limit_blog(self):
        start = time.strftime('%Y-%m-%d 00:00:00')
        end = time.strftime('%Y-%m-%d 23:59:59')
        result = dbsession.query(Blog).filter(Blog.userid == session.get('userid'),
                Blog.createtime.between(start, end)).all()
        if len(result) >= 2:
            return True  # 不再增加积分
        else:
            return False

    # 按用户id查找收藏帖子
    def find_favorite_by_userid(self):
        result = dbsession.query(Blog, Users).join(Favorite, Favorite.blogid == Blog.blogid).join(Users,Users.userid == Blog.userid)\
                .filter(Blog.userid == session.get('userid'), Favorite.canceled == 0, Blog.hidden == 0).\
                order_by(Favorite.favoriteid.asc()).all()
        return result

    # 按照回复数排序获取帖子
    def find_blog_by_reply(self):
        result = dbsession.query(Blog, Users.nickname).join(Users, Users.userid == Blog.userid)\
            .order_by(Blog.replycount.desc()).filter(Blog.hidden == 0).all()

        return result
