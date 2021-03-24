# <-- Данный файл является шаблоном -->
from data import db_session
from flask import Flask, url_for, render_template, request, redirect
from data.users import User
from data.jobs import Jobs
from data.register import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
def index():
    return render_template('base.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = User()
        user.surname = form.surname.data
        user.name = form.name.data
        user.age = form.age.data
        user.position = form.position.data
        user.speciality = form.speciality.data
        user.email = form.email.data
        user.address = form.address.data
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect("/")
    return render_template('register_form.html', title='Регистрация', form=form)


def main():
    db_session.global_init("db/mars_explorer.db")
    db_sess = db_session.create_session()
    app.run()


if __name__ == '__main__':
    main()
