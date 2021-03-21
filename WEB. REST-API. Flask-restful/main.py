from flask import Flask, render_template, url_for, jsonify
from werkzeug.utils import redirect
from data.users import User
from flask_login import LoginManager, login_user
from data import db_session, news_resources, users_resource
from flask import make_response
from flask_restful import reqparse, abort, Api, Resource


app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

# для списка объектов
api.add_resource(news_resources.NewsListResource, '/api/v2/news')
# для одного объекта
api.add_resource(news_resources.NewsResource, '/api/v2/news/<int:news_id>')
# для списка объектов
api.add_resource(users_resource.UsersListResource, '/api/v2/users')
# для одного объекта
api.add_resource(users_resource.UsersResource, '/api/v2/users/<int:user_id>')


def main():
    db_session.global_init("db/blogs.db")
    app.run()


if __name__ == '__main__':
    main()
