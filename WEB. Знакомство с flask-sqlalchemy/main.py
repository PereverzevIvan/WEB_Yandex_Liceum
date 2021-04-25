# <-- Данный файл является шаблоном -->
from data import db_session
from flask import Flask
from data.users import User
from data.jobs import Jobs
from data.departments import Department

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/mars_explorer.db")
    db_sess = db_session.create_session()
    members = db_sess.query(Department).filter(Department.id == 1).first().members.split()
    work_hours = {}
    for i in members:
        jobs = db_sess.query(Jobs).all()
        work_sizes = [j.work_size for j in jobs if i in j.collaborators]
        work_sizes = 0 if not work_sizes else sum(work_sizes)
        work_hours[i] = work_sizes
    for key, value in work_hours.items():
        if value > 25:
            user = db_sess.query(User).filter(User.id == key).first()
            print(user.name, user.surname)
    # app.run()


if __name__ == '__main__':
    main()
