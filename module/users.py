from flask import session
from sqlalchemy import Table

from common.database import dbconnect
import time

from module.credit import Credit

dbsession, md, DBase = dbconnect()

class Users(DBase):
    __table__ = Table('users', md, autoload=True)


    # 添加用户
    def addUser(self, username, password, email):
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        nickname = username
        user = Users(username=username, password=password, email=email, nickname=nickname,
                      createtime=now, exp=0, role='user', avatar='1.png', ban=0, birthday='2000-01-01')
        dbsession.add(user)
        dbsession.commit()
        return user

    # 按用户名查找
    def find_by_username(self, username):
        result = dbsession.query(Users).filter_by(username=username).first()
        return result

    # 按用户id查找
    def find_by_userid(self, userid):
        result = dbsession.query(Users).filter_by(userid=userid).first()
        return result

    # 按邮箱查找
    def find_by_email(self, email):
        result = dbsession.query(Users).filter_by(email=email).first()
        return result

    # 增加经验
    def update_exp(self, exp):
        result = dbsession.query(Users).filter_by(username=session.get('username')).first()
        result.exp += exp
        dbsession.commit()

    def update_like_exp(self, exp, userid):
        result = dbsession.query(Users).filter_by(userid=userid).first()
        result.exp += exp
        dbsession.commit()

    # 根据用户编号和日期查询今日是否已经登录
    def check_login(self):
        start = time.strftime('%Y-%m-%d 00:00:00')
        end = time.strftime('%Y-%m-%d 23:59:59')
        result = dbsession.query(Credit).filter(Credit.userid == session.get('userid'),
                    Credit.createtime.between(start, end), Credit.type=='登录').all()
        if len(result) >= 1:
            return True  # 不再增加积分
        else:
            return False

    # 修改用户密码
    def update_password(self, newPassword):
        row = dbsession.query(Users).filter_by(userid=session.get('userid')).first()
        row.password = newPassword
        dbsession.commit()

    # 修改用户个人信息
    def update_info(self, sex, birthday, nickname):
        row = dbsession.query(Users).filter_by(userid=session.get('userid')).first()
        row.nickname = nickname
        dbsession.commit()
        row.sex = sex
        dbsession.commit()
        row.birthday = birthday
        dbsession.commit()

    # 修改用户头像
    def update_avatar(self, avatar):
        row = dbsession.query(Users).filter_by(userid=session.get('userid')).first()
        row.avatar = avatar
        dbsession.commit()

    # 查询所有用户并分页
    def find_all_users(self, start, count):
        result = dbsession.query(Users).order_by(Users.userid.asc()).limit(count).offset(start).all()
        return result

    # 用户总数
    def get_count(self):
        count = dbsession.query(Users).count()
        return count

    # 禁言用户
    def ban_user(self, userid):
        row = dbsession.query(Users).filter_by(userid=userid).first()
        row.ban = 1
        dbsession.commit()

    # 解除禁言
    def cban_user(self, userid):
        row = dbsession.query(Users).filter_by(userid=userid).first()
        row.ban = 0
        dbsession.commit()
