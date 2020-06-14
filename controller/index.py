import time

from flask import Blueprint, render_template, abort, request, flash
from module.blog import Blog, Users
import math

index = Blueprint("index",__name__)


@index.route('/')
def home():
    blog = Blog()
    result = blog.find_blog_by_reply()

    return render_template('index.html', result=result, type='index')



@index.route('/search/<int:page>-<keyword>')
def search(page, keyword):
    keyword =keyword.strip()
    if keyword is None or keyword == '' or '%' in keyword or len(keyword)>16:
        abort(404)
    start = (page-1)*1
    blog = Blog()
    result = blog.find_by_headline(keyword, start, 1)
    total = math.ceil(blog.get_count_by_headline(keyword)/1)

    return render_template('search.html', result=result, page=page, total=total, keyword=keyword, type='no')


