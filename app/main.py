from flask import Flask, send_from_directory, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import os

app = Flask(__name__, static_folder='.')


# @app.route('/')
# def root():
#     return "<span>Test</span>"

@app.route('/')
def root():
    return app.send_static_file('index.html')


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'tiff', 'tif', 'bmp'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        if 'image' not in request.files:
            flash('No file')
            return redirect('/')
        file = request.files['image']
        if file.filename == '':
            flash('No file selected')
            return redirect('/')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join('./app/public/uploads/', filename))
            return redirect(f'uploads/{filename}')


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('./public/js', path)


@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('./public/css', path)


@app.route('/uploads/<path:path>')
def send_uploads(path):
    return send_from_directory('./app/public/uploads', path)
