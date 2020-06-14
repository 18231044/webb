from flask import Blueprint, request, session

from module.blog import Blog
from module.comment import Comment
from module.credit import Credit
from module.users import Users

comment = Blueprint('comment', __name__)

@comment.before_request
def before_comment():
    if session.get('islogin') != 'true':
        return 'not-login'


@comment.route('/comment', methods=['POST'])
def addc():
    blogid = request.form.get('blogid')
    content = request.form.get('content')
    content = content.replace('\n', '<br/>')
    print(content)
    if len(content) > 530:
        return 'len-error'
    blog = Blog()
    comment = Comment()
    credit = Credit()
    if session.get('ban') == '1':
        return 'comment-banned'
    if not comment.check_limit_comment():
        try:
            comment.insert_comment(blogid, content)
            blog.update_blog(blogid)
            credit.insert_exp(type='评论', exp=2)
            Users().update_exp(2)
            return 'add-success'
        except:
            return 'add-fail'
    else:
        comment.insert_comment(blogid, content)
        blog.update_blog(blogid)
        return 'add-success'

@comment.route('/comment/del', methods=['POST'])
def delc():
    commentid = request.form.get('commentid')
    userid = request.form.get('userid')
    blogid = request.form.get('blogid')
    comment = Comment()
    if session.get('userid') == userid or session.get('role') == 'admin':
        try:
            comment.delete_comment(commentid=commentid)
            Blog().reduce_blog_comment(blogid)
            return 'del-success'
        except:
            return 'del-fail'
    else:
        return 'del-fail'

@comment.route('/comment/reply', methods=['POST'])
def reply():
    commentid = request.form.get('commentid')
    blogid = request.form.get('blogid')
    content = request.form.get('content')

    if len(content) > 530:
        return 'len-error'

    comment = Comment()
    blog = Blog()
    credit = Credit()
    if session.get('ban') == 1:
        return 'comment-banned'
    if not comment.check_limit_comment():
        try:
            comment.insert_reply(blogid=blogid, commentid=commentid, content=content)
            blog.update_blog(blogid)
            credit.insert_exp(type='评论', exp=2)
            Users().update_exp(2)
            return 'add-success'
        except:
            return 'add-fail'
    else:
        comment.insert_reply(blogid=blogid, commentid=commentid, content=content)
        blog.update_blog(blogid)
        return 'add-success'
