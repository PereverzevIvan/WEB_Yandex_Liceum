from flask import Flask, url_for, render_template, request, redirect

app = Flask(__name__)


@app.route('/carousel', methods=['GET', 'POST'])
def index():
    return render_template('base.html')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
