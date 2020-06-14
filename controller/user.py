import re
import time

from flask import Blueprint, render_template, request, session, redirect, abort

from module.blog import Blog
from module.credit import Credit
from module.favourite import Favorite
from module.users import Users

user = Blueprint("user",__name__)

@user.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('login.html', type='no')
    user = Users()
    credit = Credit()
    username = request.form.get('username')
    password = request.form.get('password')
    repassword = request.form.get('repassword')
    email = request.form.get('email')

    if username == '' or password == '' or email == '':
        return 'ep-err'

    # 检验用户名或邮箱是否被注册
    result = user.find_by_username(username)
    if result:
        return 'username-exist'
    result = user.find_by_email(email)
    if result:
        return 'email-exist'

    # 验证邮箱正确性
    if not re.match('.+@.+\..+', email) :
        return 'email-error'

    # 检验密码合法性
    if password != repassword:
        return 'password-d'
    if len(password) < 6 or len(password) > 16:
        return 'password-error'

    if '%' in password or ' ' in password or '  ' in password or '*' in password \
        or '%' in username or ' ' in username or '  ' in username or '*' in username \
        or '%' in repassword or ' ' in repassword or '  ' in repassword or '*' in repassword \
        or '%' in email or ' ' in email or '  ' in email or '*' in email or '@' in username:
        return 'input-error'

    result = user.addUser(username=username, password=password, email=email)
    session['islogin'] = 'true'
    session['username'] = username
    session['nickname'] = result.nickname
    session['role'] = result.role
    session['userid'] = result.userid
    session['ban'] = result.ban
    if not user.check_login():
        credit.insert_exp(exp=10, type='登录')
        Users().update_exp(10)
    session['exp'] = result.exp
    level = int(int(session.get('exp')) / 100)
    session['level']=level
    return 'reg-success'

@user.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', type='no')
    user = Users()
    credit = Credit()
    username = request.form.get('username')
    password = request.form.get('password')

    result = user.find_by_username(username)
    if result and result.password == password:
        session['islogin'] = 'true'
        session['username'] = username
        session['nickname'] = result.nickname
        session['role'] = result.role
        session['userid'] = result.userid
        session['ban'] = result.ban
        if not user.check_login():
            credit.insert_exp(exp=10, type='登录')
            Users().update_exp(10)
        session['exp'] = result.exp
        level = int(int(session.get('exp')) / 100)
        session['level'] = level
        return 'login-success'
    result = user.find_by_email(username)
    if result and result[0].password == password:
        session['islogin'] = 'true'
        session['username'] = username
        session['nickname'] = result.nickname
        session['role'] = result.role
        session['userid'] = result.userid
        session['ban'] = result.ban
        if not user.check_login():
            credit.insert_exp(exp=10, type='登录')
            Users().update_exp(10)
        session['exp'] = result.exp
        level = int(int(session.get('exp')) / 100)
        session['level'] = level
        return 'login-success'
    else:
        return 'login-fail'

@user.route('/signout')
def signout():
    session.clear()
    return redirect('/')

# 修改密码
@user.route('/chgpw', methods=['POST'])
def changePassword():
    user = Users()
    oldpassword = request.form.get('oldpassword')
    newpassword = request.form.get('newpassword')
    repassword = request.form.get('repassword')
    user = user.find_by_username(session.get('username'))
    if oldpassword != user.password:
        return 'old-new-diff'
    if newpassword != repassword:
        return 're-diff'
    if len(newpassword) < 6 or len(newpassword) > 16:
        return 'new-len-error'
    if '%' in newpassword or ' ' in newpassword or '  ' in newpassword or '*' in newpassword:
        return 'illegal-error'
    try:
        user.update_password(newPassword=newpassword)
        return 'change-success'
    except:
        return 'change-fail'

# 用户主页
@user.route('/home/<int:userid>')
def user_home(userid):
    if session.get('islogin') != 'true':
        abort(404)
    user = Users().find_by_userid(session.get('userid'))
    level = int(int(session.get('exp'))/100)
    exp_ = int(session.get('exp'))-level*100
    birthday = user.birthday
    nickname = user.nickname
    sex = user.sex
    return render_template("user-home.html", user=user, birthday=birthday, sex=sex, level=level, exp_=exp_
                           , nickname=nickname, type='user')

# 用户修改密码页
@user.route('/home/<int:userid>/chgpw')
def homecp(userid):
    user = Users().find_by_userid(session.get('userid'))
    if session.get('islogin') != 'true':
        abort(404)
    return render_template("chgpw.html", user=user, type='user')

# 修改个人资料
@user.route('/user/updateinfo', methods=['POST'])
def updateinfo():
    birthday = request.form.get('birthday')
    sex = request.form.get('sex')
    nickname = request.form.get('nickname')
    user = Users()
    if session.get('islogin') != 'true':
        abort(404)
    if len(nickname) > 15:
        return 'nickname-error'
    try:
        user.update_info(sex=sex, birthday=birthday, nickname=nickname)
        return 'update-success'
    except:
        return 'update-fail'

# 显示收藏页面
@user.route('/home/<int:userid>/favorite')
def show_favortite(userid):
    user = Users().find_by_userid(session.get('userid'))
    if session.get('islogin') != 'true':
        abort(404)
    blog = Blog()
    result = blog.find_favorite_by_userid()
    return render_template("user-favorite.html", result=result, user=user, type='user')

# 显示我的帖子
@user.route('/home/<int:userid>/myblog')
def show_myblog(userid):
    user = Users().find_by_userid(session.get('userid'))
    if session.get('islogin') != 'true':
        abort(404)
    blog = Blog()
    result = blog.get_blog_by_userid()
    return render_template("user-myblog.html", result=result, user=user, type='user')

@user.route('/user/avatar', methods=['POST'])
def upload_avatar():
    avatar = request.files.get('avatar')
    suffix = avatar.filename.split('.')[-1]

    if suffix.lower() not in ['jpg', 'jpeg', 'png']:
        return 'invalid'

    name = str(int(time.time()))+'.'+suffix

    avatar.save('C:/Users/94406/PycharmProjects/webb/static/img/avatar/' + name)
    user = Users()
    user.update_avatar(name)
    return 'upload-success'


