from flask import Flask, render_template, url_for, jsonify
from werkzeug.utils import redirect
from data import db_session
from data.users import User
from flask_login import LoginManager, login_user
from data import db_session, jobs_api
from flask import make_response


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


def main():
    db_session.global_init("db/mars_one.db")
    app.register_blueprint(jobs_api.blueprint)
    app.run()


if __name__ == '__main__':
    main()
