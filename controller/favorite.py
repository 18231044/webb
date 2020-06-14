from flask import Blueprint, request, session

from module.favourite import Favorite

favorite = Blueprint('favorite', __name__)

@favorite.route('/favorite', methods=['POST'])
def add_favorite():
    blogid = request.form.get('blogid')
    if session.get('islogin') is None:
        return 'not-login'
    else:
        try:
            Favorite().insert_favorite(blogid)
            return 'favorite-pass'
        except:
            return 'favorite-fail'

@favorite.route('/favorite/<int:blogid>', methods=['DELETE'])
def cancel_favorite(blogid):
    try:
        Favorite().cancel_favorite(blogid)
        return 'cancel-pass'
    except:
        return 'cancel-fail'

