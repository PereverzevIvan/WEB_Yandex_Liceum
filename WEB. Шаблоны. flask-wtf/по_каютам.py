from flask import Flask, url_for, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
def index():
    return render_template('base.html')


@app.route('/distribution')
def distribution():
    spisok = ['Иван', 'Гайзен', 'Сатору', 'Марк']
    return render_template('по_каютам.html', spisok=spisok)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
