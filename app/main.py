from flask import Flask, send_from_directory, flash, request, redirect, jsonify
from werkzeug.utils import secure_filename
import os
# import base64
import magic
import pytesseract as pt
import cv2

mime = magic.Magic(mime=True)

app = Flask(__name__, static_folder='.', static_url_path='')


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
            filepath = os.path.join('./app/public/uploads/images', filename)
            file.save(filepath)
            # return redirect(f'uploads/{filename}')
            img_cv = cv2.imread(filepath)
            img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
            tessdata_dir_config = r'--tessdata-dir "./app/tessdata"'

            pt.pytesseract.tesseract_cmd = r'/app/.apt/usr/bin/tesseract'

            prediction = pt.image_to_string(img_rgb,
                                            lang='eng',
                                            config=tessdata_dir_config)

            response = {
                "mime_type": mime.from_file(filepath),
                "url": f"/public/uploads/images/{filename}",
                "prediction": prediction
            }
            # with open(filepath, "rb") as image:
            #     encodedbase64 = base64.b64encode(image.read()).decode('utf-8')
            #     response["base64raw"] = encodedbase64
            #     response["base64uri"] = f"data:{response['mime_type']}; \
            #         {encodedbase64}"

            return jsonify(response)


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('./public/js', path)


@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('./public/css', path)


# @app.route('/uploads/<path:path>')
# def send_uploads(path):
#     print(os.getcwd())
#     return send_from_directory('./app/public/uploads', path)
