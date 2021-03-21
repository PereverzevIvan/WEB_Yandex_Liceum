from flask import jsonify
from flask_restful import abort, Resource

from data import db_session
from data.users import User
from data.users_reqparse import parser


def errors_with_users(user_id):
    session = db_session.create_session()
    users = session.query(User).get(user_id)
    if not users:
        abort(404, message=f"Users {user_id} not found")


class UsersResource(Resource):
    def get(self, user_id):
        print(user_id)
        if type(user_id) != int:
            print('Bad request')
            return jsonify({'error': 'Bad request'})
        errors_with_users(user_id)
        session = db_session.create_session()
        users = session.query(User).get(user_id)
        return jsonify({'user': users.to_dict(
            only=('id', 'surname', 'name', 'age', 'position', 'speciality', 'email',
                  'hashed_password', 'address', 'modified_date'))})

    def delete(self, user_id):
        if type(user_id) != int:
            return jsonify({'error': 'Bad request'})
        errors_with_users(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({'users': [item.to_dict(
            only=('id', 'surname', 'name', 'age', 'position', 'speciality', 'email',
                  'hashed_password', 'address', 'modified_date')) for item in users]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        user = User(
            id=args['id'],
            surname=args['surname'],
            name=args['name'],
            age=args['age'],
            position=args['position'],
            speciality=args['speciality'],
            email=args['email'],
            address=args['address'])
        user.set_password(args['hashed_password'])
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})
