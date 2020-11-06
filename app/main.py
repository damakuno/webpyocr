from flask import Flask, send_from_directory, flash, request, redirect, jsonify
from werkzeug.utils import secure_filename
import os
# import base64
import magic
import pytesseract as pt
import cv2
import numpy as np

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
            # img = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
            img_ori = img_cv.copy()
            img_gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
            # img_invert = cv2.bitwise_not(img_gray)
            # img_denoise = cv2.medianBlur(img_gray, 5)
            # img_thresh = cv2.threshold(
            #     img_denoise, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
            # kernel = np.ones((5, 5), np.uint8)
            # img = cv2.morphologyEx(img_thresh, cv2.MORPH_OPEN, kernel)
            tessdata_dir_config = r'--tessdata-dir "./app/tessdata"'

            pt.pytesseract.tesseract_cmd = r'/app/.apt/usr/bin/tesseract'

            prediction = pt.image_to_data(img_gray,
                                          lang='eng',
                                          config=tessdata_dir_config,
                                          output_type=pt.Output.DICT)

            d = prediction
            n_boxes = len(d['text'])
            for i in range(n_boxes):
                if int(d['conf'][i]) > 60:
                    (x, y, w, h) = (d['left'][i], d['top']
                                    [i], d['width'][i], d['height'][i])
                    img_ori = cv2.rectangle(
                        img_ori, (x, y), (x + w, y + h), (0, 255, 0), 2)
            bb_image_path = os.path.join(
                './app/public/uploads/images', f'bb_{filename}')
            if os.path.exists(bb_image_path):
                os.remove(bb_image_path)
            cv2.imwrite(bb_image_path, img_ori)
            # while not os.path.isfile(bb_image_path):
            #     pass

            # prediction_invert = pt.image_to_data(img_invert,
            #                                      lang='eng',
            #                                      config=tessdata_dir_config,
            #                                      output_type=pt.Output.DICT)

            response = {
                "mime_type": mime.from_file(filepath),
                "url": f"/public/uploads/images/bb_{filename}",
                "prediction": prediction["text"]  # + prediction_invert["text"]
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
