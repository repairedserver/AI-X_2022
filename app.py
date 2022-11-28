from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import test
import json

app = Flask (__name__)

@app.route('/') 
def hello():
    return 'YEE /upload'

@app.route('/upload', methods = ['GET', 'POST'])
def render_file():
    return render_template('upload.html')

@app.route('/fileUpload', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save('static/images/' + secure_filename('original.png'))
        return '파일 업로드 성공!'

@app.route('/intUpload/<int:post_id>')
def upload_int(post_id):
    test.run(post_id)
    return '차종 받기 완료!'

@app.route('/image_0') 
def image_0():
    return render_template('image_0.html')

@app.route('/image_1') 
def image_1():
    return render_template('image_1.html')

@app.route('/image_2') 
def image_2():
    return render_template('image_2.html')

@app.route('/image_3') 
def image_3():
    return render_template('image_3.html')

@app.route('/printed')
def printed():
    with open('static/images/printed.json', 'r') as f:
        data = json.load(f)
    return jsonify(data)

if __name__ == "__main__": 
    app.run(host='0.0.0.0', port='5001', debug=True)