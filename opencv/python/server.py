import os
from flask import Flask, url_for, redirect, render_template, request, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

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
        import detect
        detect.main('{}/uploads/{}'.format(BASE_DIR,secure_filename(f.filename)))
    return 'success'

@app.route('/uploads/<filename>')
def get_uploaded(filename):
    return send_from_directory('{}/uploads/'.format(BASE_DIR),filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)