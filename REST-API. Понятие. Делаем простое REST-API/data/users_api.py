import flask
from flask import jsonify, request
from . import db_session
from .users import User

blueprint = flask.Blueprint('users_api', __name__, template_folder='templates')


@blueprint.route('/api/users')
def get_users():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    return jsonify(
        {
            'users':
                [item.to_dict(only=('id', 'name', 'surname', 'about',
                                    'email', 'city_from', 'created_date'))
                 for item in users]
        }
    )


@blueprint.route('/api/users/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'user': user.to_dict(only=('id', 'name', 'surname', 'about',
                                       'email', 'city_from', 'created_date'))
        }
    )


@blueprint.route('/api/users', methods=['POST'])
def create_user():
    db_sess = db_session.create_session()
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['id', 'name', 'surname', 'about',
                  'email', 'city_from', 'password']):
        return jsonify({'error': 'Bad request'})
    user = db_sess.query(User).filter(User.id == request.json['id']).first()
    if user is not None:
        user.name = request.json['name']
        user.surname = request.json['surname']
        user.about = request.json['about']
        user.email = request.json['email']
        user.city_from = request.json['city_from']
    else:
        user = User(
            id=request.json['id'],
            name=request.json['name'],
            surname=request.json['surname'],
            about=request.json['about'],
            city_from=request.json['city_from'],
            email=request.json['email'],
        )
        user.set_password(request.json['password'])
        db_sess.add(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    db_sess.delete(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})
