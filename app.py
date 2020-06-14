from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, abort
import os
import pymysql



pymysql.install_as_MySQLdb()

app = Flask(__name__,template_folder='templates',static_url_path='/',static_folder='static')
app.config['SECRET_KEY'] = os.urandom(24)

# 使用集成方法处理SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:root@localhost:3306/web?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_MAX_OVERFLOW'] = 1000

# 初始化db对象
db = SQLAlchemy(app)

# 定义分区函数
# {{blog_type[blog.type | string]}}
# 可用于优化导航栏 22快结束
@app.context_processor
def gettype():
    type = {
        '1': '讨论区',
        '2': '课程推荐',
        '3': '校园周边',
        '4': '资源共享',
        '5': '刷题区'
    }
    return dict(blog_type=type)




if __name__ == '__main__':
        from controller.index import *
        app.register_blueprint(index)

        from controller.block import *
        app.register_blueprint(block)

        from controller.user import *
        app.register_blueprint(user)

        from controller.blog import *
        app.register_blueprint(blog)

        from controller.favorite import *
        app.register_blueprint(favorite)

        from controller.comment import *
        app.register_blueprint(comment)

        from controller.likes import *
        app.register_blueprint(likes)

        from controller.file import *
        app.register_blueprint(file)

        from controller.admin import *
        app.register_blueprint(admin)

        app.run(host='0.0.0.0')