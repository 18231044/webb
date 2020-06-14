from flask import session,request
from sqlalchemy import Table
from common.database import dbconnect
import time

from module.blog import Blog
from module.likes import Likes
from module.users import Users

dbsession, md, DBase = dbconnect()

class File(DBase):
    __table__ = Table("file", md, autoload=True)

    # 插入一条文件记录
    def insert_file(self, filename, headline, content):
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        file = File(userid=session.get('userid'), filename=filename, content=content,
                          uploadtime=now, headline=headline, hidden=0)
        dbsession.add(file)
        dbsession.commit()

    # 查找所有文件
    def find_all(self):
        result = dbsession.query(File).filter(File.hidden==0).all()
        return result

    # 按文件名查找文件资源
    def find_by_file(self, filename):
        result = dbsession.query(File).filter(File.filename==filename).first()
        return result

    def find_limit_with_users(self, start, count):
        result = dbsession.query(File, Users).join(Users, Users.userid == File.userid)\
            .filter(File.hidden==0).order_by(File.uploadtime.desc()).limit(count).offset(start).all()
        return result

    # 删除（隐藏）一个文件资源
    def delete_file(self, fileid):
        row = dbsession.query(File).filter(File.fileid==fileid).first()
        row.hidden = 1
        dbsession.commit()

    # 恢复一个文件资源
    def cancel_delete_file(self, fileid):
        row = dbsession.query(File).filter(File.fileid==fileid).first()
        row.hidden = 0
        dbsession.commit()


    # 统计文件总数量
    def get_total_file_count(self):
        count = dbsession.query(File).filter(File.hidden == 0).count()
        return count

    # 统计文件总数量（包括隐藏）
    def get_total_count(self):
        count = dbsession.query(File).count()
        return count

    # 查询所有文件并分页
    def find_all_file(self, start, count):
        result = dbsession.query(File).order_by(File.fileid.asc()).limit(count).offset(start).all()
        return result
