import os
from flask import Flask, url_for, redirect, render_template, request, send_from_directory, jsonify
from werkzeug.utils import secure_filename
import requests

import detect

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
url = 'http://192.168.1.26/'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dist/<file>')
def get_static(file):
    return redirect(url_for('static',filename='dist/{}'.format(file)))

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save('{}/uploads/'.format(BASE_DIR) + secure_filename(f.filename))
        return jsonify( detect.main('{}/uploads/{}'.format(BASE_DIR,secure_filename(f.filename))) )
    return 'success'

@app.route('/cam')
def cam():
    print('start')
    r = requests.get(url, allow_redirects=True)
    open('uploads/capture.jpg', 'wb').write(r.content)
    return jsonify( detect.main('{}/uploads/capture.jpg'.format(BASE_DIR)) )

@app.route('/control/<direct>')
def ctl(direct):
    r = requests.get('{}{}'.format(url,direct), allow_redirects=True)
    return 'ok'

@app.route('/uploads/<filename>')
def get_uploaded(filename):
    return send_from_directory('{}/uploads/'.format(BASE_DIR),filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)