from flask import Flask

app = Flask(__name__, static_folder='.', root_path='/home/runner')


@app.route('/')
def root():
    return app.send_static_file('index.html')
