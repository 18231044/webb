from flask import Blueprint, request, session

from module.blog import Blog
from module.comment import Comment
from module.credit import Credit
from module.likes import Likes
from module.users import Users

likes = Blueprint('likes', __name__)

@likes.route("/likes", methods=['POST'])
def addlike():
    commentid = request.form.get('commentid')
    like = Likes()
    credit = Credit()
    if like.find_like(commentid=commentid):
        return 'have-liked'
    if not like.check_limit_like():
        comment = Comment().find_by_commentid(commentid)
        like.insert_like(commentid=commentid)
        credit.insert_exp_user(type='点赞', exp=1, userid=comment.userid)
        Users().update_like_exp(exp=1, userid=comment.userid)
        return 'like-success'
    else:
        like.insert_like(commentid=commentid)
        return 'like-success'


