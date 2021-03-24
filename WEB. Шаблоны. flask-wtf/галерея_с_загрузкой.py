from flask import Flask, url_for, render_template, request, redirect
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
def index():
    return render_template('base.html')


@app.route('/galery', methods=['GET', 'POST'])
def galery():
    if request.method == 'GET':
        list_img = [i for i in os.listdir('static/img') if 'mars_' in i]
        return render_template('галерея_с_загрузкой.html', list_img=list_img)
    elif request.method == 'POST':
        file = request.files['file']
        if file:
            file_name = len([int(i.split('_')[1][0]) for i in os.listdir('static/img') if 'mars_' in i]) + 1
            file.save(f'static/img/mars_{file_name}.jpg')
        return redirect('/galery')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
