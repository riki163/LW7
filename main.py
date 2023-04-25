from PIL import Image
import json
from flask import Flask, Response, request, render_template, redirect, jsonify

app = Flask(__name__)

def check_image(filename):
    if filename:
        with Image.open(filename) as img:
            img.load()
            print(img.size[0], img.size[1])
            return {'width': img.size[0], 'height': img.size[1]}

@app.route('/')
@app.route('/about')
def homepage():
    return Response(json.dumps({'message': '@Vladislav'}), mimetype='application/json')

@app.route('/size2json', methods=['GET', 'POST'])
def size2json():
    if request.method == 'POST':
        
        attached_file = request.files.get('file')

        if not attached_file or not allowed_file(attached_file.filename):
            return jsonify({'result': 'invalid filetype'})

        path_to_image = './' + attached_file.filename
        attached_file.save(path_to_image)
        
        img_params_tuple = check_image(path_to_image)

        if img_params_tuple is None:
            return jsonify({'result': 'invalid file'})
        
        message = f'Параметры изображения: {img_params_tuple}'
        print(attached_file, message, img_params_tuple)
        return jsonify({'width': img_params_tuple['width'], 'height': img_params_tuple['height']}, )
    
    else:
        message = 'Загрузить файл'
    return render_template('upload.html', message=message)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg', 'png', 'gif'}


@app.route('/login')
def login():
            return jsonify({"author": "213028"})

if __name__ == '__main__':
    app.run('0.0.0.0', 8080, debug=True)
