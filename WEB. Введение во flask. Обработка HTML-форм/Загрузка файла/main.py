from flask import Flask, url_for, render_template, request, redirect

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('base.html')
    elif request.method == 'POST':
        file = request.files['file']
        if file:
            file_name = f'img/{file.filename}'
            file.save(f'static/{file_name}')
            return render_template('base.html', file_name=file_name)
        return redirect('/')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
