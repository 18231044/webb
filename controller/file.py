import time

from flask import Blueprint, render_template, request, session, redirect, abort, send_from_directory

from module.file import File


file = Blueprint("file",__name__)

@file.route('/preupload')
def show_upload():
    return render_template('upload-file.html')

@file.route('/upload', methods=['POST'])
def upload_file():
    headline = request.form.get('headline')
    content = request.form.get('content')
    content = content.replace('\n', '<br/>')
    upfile = request.files.get('upfile')

    if len(headline)>20:
        return 'headline-error'

    if len(content)>150:
        return 'content-error'

    suffix = upfile.filename.split('.')[-1]

    if suffix.lower() not in ['jpg', 'jpeg', 'png', 'rar', 'zip', 'xls', 'txt', 'gif', 'doc', 'docx']:
        return 'invalid'

    name = str(int(time.time())) + '.' + suffix

    upfile.save('D:/sujun/Documents/WeChat Files/wxid_t5xuzy8q1b8i22/FileStorage/File/2020-06/webb/upload/' + name)
    file1 = File()
    file1.insert_file(filename=name, headline=headline, content=content )
    return 'upload-success'

@file.route('/download/<path:filename>')
def download_file(filename):
    return send_from_directory('D:/sujun/Documents/WeChat Files/wxid_t5xuzy8q1b8i22/FileStorage/File/2020-06/webb/upload/', filename, as_attachment=True)