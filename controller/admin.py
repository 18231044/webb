import math
from flask import Blueprint, request, session, render_template

from module.blog import Blog
from module.comment import Comment
from module.credit import Credit
from module.file import File
from module.users import Users

admin = Blueprint('admin', __name__)

@admin.before_request
def before_comment():
    if session.get('role') != 'admin':
        return '您没有权限进行此操作'

# 用户管理
@admin.route('/admin/users')
def user_manage():
    user = Users()
    result = user.find_all_users(0, 10)
    total = math.ceil(user.get_count() / 10)
    return render_template('admin-users.html', result=result, page=1, total=total, type='no')

@admin.route('/admin/users/<int:page>')
def user_cl(page):
    start = (page - 1) * 10
    user = Users()
    result = user.find_all_users(start, 10)
    total = math.ceil(user.get_count() / 10)
    return render_template('admin-users.html', result=result, page=page, total=total, type='no')

@admin.route('/admin/ban', methods=['POST'])
def ban_user():
    userid = request.form.get('userid')
    user = Users()
    try:
        user.ban_user(userid)
        return 'ban-success'
    except:
        return 'ban-fail'

@admin.route('/admin/cban', methods=['POST'])
def cban_user():
    userid = request.form.get('userid')
    user = Users()
    try:
        user.cban_user(userid)
        return 'cban-success'
    except:
        return 'cban-fail'

# 帖子管理
@admin.route('/admin/blogs')
def blog_manage():
    blog = Blog()
    result = blog.find_all_blog(0, 10)
    total = math.ceil(blog.get_total_blog_count() / 10)
    return render_template('admin-blog.html', result=result, page=1, total=total, type='no')

@admin.route('/admin/blogs/<int:page>')
def blog_cl(page):
    start = (page - 1) * 10
    blog = Blog()
    result = blog.find_all_blog(start, 10)
    total = math.ceil(blog.get_total_blog_count() / 10)
    return render_template('admin-blog.html', result=result, page=page, total=total, type='no')

@admin.route('/admin/del-blog', methods=['POST'])
def hide_blog():
    blogid = request.form.get('blogid')
    blog = Blog()
    try:
        blog.hide_blog(blogid)
        return 'hide-success'
    except:
        return 'hide-fail'

@admin.route('/admin/cdel-blog', methods=['POST'])
def chide_blog():
    blogid = request.form.get('blogid')
    blog = Blog()
    try:
        blog.cancel_hide_blog(blogid)
        return 'chide-success'
    except:
        return 'chide-fail'

# 评论管理
@admin.route('/admin/comments')
def comment_manage():
    comment = Comment()
    result = comment.find_all_comment(0, 10)
    total = math.ceil(comment.get_total_count() / 10)
    return render_template('admin-comment.html', result=result, page=1, total=total, type='no')

@admin.route('/admin/comments/<int:page>')
def comment_cl(page):
    start = (page - 1) * 10
    comment = Comment()
    result = comment.find_all_comment(start, 10)
    total = math.ceil(comment.get_total_count() / 10)
    return render_template('admin-blog.html', result=result, page=page, total=total, type='no')

@admin.route('/admin/del-comment', methods=['POST'])
def delete_comment():
    commentid = request.form.get('commentid')
    comment = Comment()
    comment= comment.find_by_commentid(commentid)
    blogid = comment.blogid
    try:
        comment.delete_comment(commentid)
        Blog().reduce_blog_comment(blogid)
        return 'del-success'
    except:
        return 'del-fail'

# 资源管理
@admin.route('/admin/files')
def file_manage():
    file = File()
    result = file.find_all_file(0, 10)
    total = math.ceil(file.get_total_count() / 10)
    return render_template('admin-file.html', result=result, page=1, total=total, type='no')

@admin.route('/admin/files/<int:page>')
def file_cl(page):
    start = (page - 1) * 10
    file = File()
    result = file.find_all_file(start, 10)
    total = math.ceil(file.get_total_count() / 10)
    return render_template('admin-file.html', result=result, page=page, total=total, type='no')

@admin.route('/admin/del-file', methods=['POST'])
def hide_file():
    fileid = request.form.get('fileid')
    file = File()
    try:
        file.delete_file(fileid)
        return 'hide-success'
    except:
        return 'hide-fail'

@admin.route('/admin/cdel-file', methods=['POST'])
def chide_file():
    fileid = request.form.get('fileid')
    file = File()
    try:
        file.cancel_delete_file(fileid)
        return 'chide-success'
    except:
        return 'chide-fail'

