from flask import Blueprint, render_template
from module.blog import Blog
import math

from module.file import File

block = Blueprint("block",__name__)

@block.route('/<type>')
def home(type):
    blog = Blog()
    result = blog.find_by_type(type, 0, 10)
    total = math.ceil(blog.get_count_by_type(type)/10)
    return render_template('block1.html', result=result, page=1, total=total, type=type)

@block.route('/<type>/<int:page>')
def classify(type, page):
    start = (page-1) *10
    blog = Blog()
    result = blog.find_by_type(type, start, 10)
    total = math.ceil(blog.get_count_by_type(type)/10)
    return render_template('block1.html', result=result, page=page, total=total, type=type)

@block.route('/share')
def file():
    file = File()
    result = file.find_limit_with_users(0, 10)
    total = math.ceil(file.get_total_file_count() / 10)
    return render_template('block2.html', result=result, page=1, total=total, type='share')

@block.route('/share/<int:page>')
def f_classify(page):
    file = File()
    start = (page-1) *10
    result = file.find_limit_with_users(start, 10)
    total = math.ceil(file.get_total_file_count() / 10)
    return render_template('block2.html', result=result, page=page, total=total, type='share')