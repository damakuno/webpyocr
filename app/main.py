from flask import Flask, send_from_directory

app = Flask(__name__)  # , static_folder='.')


@app.route('/')
def root():
    return "<span>Test</span>"

# @app.route('/')
# def root():
#     return app.send_static_file('index.html')

# Serves javascript files


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('./public/js', path)

# Serves css style sheets


@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('./public/css', path)
