from flask import Blueprint, render_template, abort, request, flash, session
from module.blog import Blog, Users
import math

from module.comment import Comment
from module.credit import Credit
from module.favourite import Favorite

blog = Blueprint("blog",__name__)

@blog.route('/blog/<int:blogid>')
def read(blogid):
    try:
        result = Blog().find_by_id(blogid)
        if result is None:
            abort(404)
    except:
        abort(404)



    is_favorite = Favorite().check_favorite(blogid)

    # 显示评论
    comment_user = Comment().find_comment_with_user(blogid, 0, 50)


    level1 = int(result.exp/100)

    type = result[0].type


    return render_template('blog.html', result=result, is_favorite=is_favorite, comment_user=comment_user,
                           level1=level1, type=type)

@blog.route('/blog/write', methods=['GET','POST'])
def write():
    if request.method == 'GET':
        return render_template('write-blog.html', type='no')
    blog = Blog()
    credit = Credit()
    headline = request.form.get('headline')
    content = request.form.get('content')
    content = content.replace('\n', '<br/>')
    type = request.form.get('type')
    level = request.form.get('level')
    if level == '1级':
        level=1
    elif level == '2级':
        level=2
    elif level == '3级':
        level=3
    elif level == '4级':
        level=4
    elif level == '5级':
        level=5
    if session.get('ban') == 1:
        return 'banned'
    if len(content) > 1000:
        return 'content-len-error'
    if len(headline) > 15:
        return 'headline-len-error'
    if session.get('islogin') != 'true':
        return 'not-login'
    if int(session.get('exp')) < int(level)*100:
        return 'level-error'
    try:

        if not blog.check_limit_blog():
            blog.write_blog(headline=headline, content=content, type=type, level=level)
            credit.insert_exp('发布帖子', 5)
            Users().update_exp(5)
            return 'write-success'
        else:
            blog.write_blog(headline=headline, content=content, type=type, level=level)
            return 'write-success'
    except:
        return 'write-fail'

# 删除帖子
@blog.route('/blog/del/<int:blogid>', methods=['DELETE'])
def del_blog(blogid):
    blog = Blog()
    row = blog.find_by_blogid(blogid)
    if session.get('role')=='admin' or row.userid==session.get('userid'):
        row.hide_blog(blogid)
        return 'del-success'
    else:
        return 'have-no-right'
