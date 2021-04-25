import requests
from flask import Flask, render_template, url_for, request, abort, jsonify
from werkzeug.utils import redirect
from data import db_session
from data.users import User
from data.jobs import Jobs
from data.category import Category
from data.departments import Department
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data.login_form import LoginForm
from data.register import RegisterForm
from data.add_job_form import AddJobForm
from data.add_dep_form import AddDepartmentForm
from data import db_session, jobs_api, users_api
from flask import make_response
from requests import get, post, delete

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/users_show/<int:user_id>')
def users_show(user_id):
    if not current_user.is_authenticated:
        redirect("/")

    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": current_user.city_from,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)

    if not response:
        # обработка ошибочной ситуации
        pass

    # Преобразуем ответ в json-объект
    json_response = response.json()
    # Получаем первый топоним из ответа геокодера.
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    # Координаты центра топонима:
    toponym_coodrinates = toponym["Point"]["pos"]
    # Долгота и широта:
    lon, lat = toponym_coodrinates.split(" ")
    response = f"http://static-maps.yandex.ru/1.x/?ll={lon},{lat}&spn=0.002,0.002&l=sat"
    return render_template('Использование API.html', user=current_user, url=response)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
def index():
    return render_template('base.html', title='Главная')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login-form.html',
                               message="Неправильный логин или пароль",
                               form=form, title='Авторизация')
    return render_template('login-form.html', title='Авторизация', form=form)


@app.route('/get_jobs')
def get_jobs():
    if not current_user.is_authenticated:
        return redirect('/')
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    users = [f'{i.name} {i.surname}' for i in db_sess.query(User).all()]
    return render_template('Список работ.html', jobs=jobs, users=users, title='Список работ')


@app.route('/add_job', methods=['GET', 'POST'])
def add_job():
    db_sess = db_session.create_session()
    form = AddJobForm()
    categories = {'': 0}
    for i in db_sess.query(Category).all():
        categories[i.name] = i.id
    form.categories.choices = [i for i in categories.keys()]
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = Jobs()
        job.job = form.job.data
        job.work_size = form.work_size.data
        job.collaborators = form.collaborators.data
        job.team_leader = form.team_leader.data
        job.is_finished = form.is_finished.data
        category = categories[form.categories.data]
        if category:
            category = db_sess.query(Category).filter(Category.id == category).first()
            job.categories.append(category)
        db_sess.add(job)
        db_sess.commit()
        return redirect("/get_jobs")
    return render_template('add_job_form.html', title='Добавление работы', form=form)


@app.route('/edit_job/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    db_sess = db_session.create_session()
    form = AddJobForm()
    categories = {'': 0}
    for i in db_sess.query(Category).all():
        categories[i.name] = i.id
    form.categories.choices = [i for i in categories.keys()]
    if request.method == "GET":
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).filter(
            (Jobs.id == id), (Jobs.user == current_user) | (current_user.id == 1)).first()
        if jobs:
            form.job.data = jobs.job
            form.work_size.data = jobs.work_size
            form.collaborators.data = jobs.collaborators
            form.team_leader.data = jobs.team_leader
            form.is_finished.data = jobs.is_finished
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = db_sess.query(Jobs).filter(
            (Jobs.id == id), (Jobs.user == current_user) | (current_user.id == 1)).first()
        if job:
            job.job = form.job.data
            job.work_size = form.work_size.data
            job.collaborators = form.collaborators.data
            job.team_leader = form.team_leader.data
            job.is_finished = form.is_finished.data
            category = categories[form.categories.data]
            if category:
                category = db_sess.query(Category).filter(Category.id == category).first()
                job.categories.append(category)
            db_sess.commit()
            return redirect('/get_jobs')
        else:
            abort(404)
    return render_template('add_job_form.html', title='Редактирование новости', form=form)


@app.route('/jobs_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def jobs_delete(id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).filter(
        (Jobs.id == id), (Jobs.user == current_user) | (current_user.id == 1)).first()
    if job:
        db_sess.delete(job)
        number = 1
        for job in db_sess.query(Jobs).all():
            job.id = number
            number += 1
        db_sess.commit()
    else:
        abort(404)
    return redirect('/get_jobs')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        users = db_sess.query(User).all()
        id_ = len(users) + 1
        if db_sess.query(User).filter(User.email == form.email.data).all():
            mes = 'Данный адрес электронной почты уже занят'
            return render_template('register_form.html', title='Регистрация', form=form, message=mes)
        post('http://localhost:5000/api/users', json={
            'id': id_,
            'name': form.name.data,
            'surname': form.surname.data,
            'about': form.about.data,
            'city_from': form.city_from.data,
            'email': form.email.data,
            'password': form.password.data
        }
             ).json()
        return redirect("/login")
    return render_template('register_form.html', title='Регистрация', form=form)


@app.route('/get_departments')
def get_deps():
    if not current_user.is_authenticated:
        return redirect('/')
    db_sess = db_session.create_session()
    deps = db_sess.query(Department).all()
    users_id = {}
    for user in db_sess.query(User).all():
        users_id[user.id] = f'{user.surname} {user.name}'
    return render_template('departments_list.html', deps=deps, title='List of Departments', users_id=users_id)


@app.route('/add_department', methods=['GET', 'POST'])
def add_deps():
    if not current_user.is_authenticated:
        return redirect('/')
    form = AddDepartmentForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        dep = Department()
        dep.title = form.title.data
        dep.chief = form.chief.data
        dep.email = form.email.data
        dep.members = form.members.data
        db_sess.add(dep)
        db_sess.commit()
        return redirect("/get_departments")
    return render_template('add_dep.html', title='Adding of department', form=form)


@app.route('/department_delete/<int:id>', methods=['GET', 'POST', 'DELETE'])
@login_required
def dep_delete(id):
    db_sess = db_session.create_session()
    dep = db_sess.query(Department).filter(
        (Department.id == id), (Department.user == current_user) | (current_user.id == 1)).first()
    if dep:
        db_sess.delete(dep)
        number = 1
        for dep in db_sess.query(Department).all():
            dep.id = number
            number += 1
        db_sess.commit()
    else:
        abort(404)
    return redirect('/get_departments')


@app.route('/edit_department/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_dep(id):
    form = AddDepartmentForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        dep = db_sess.query(Department).filter(
            (Department.id == id), (Department.user == current_user) | (current_user.id == 1)).first()
        if dep:
            form.title.data = dep.title
            form.chief.data = dep.chief
            form.members.data = dep.members
            form.email.data = dep.email
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        dep = db_sess.query(Department).filter(
            (Department.id == id), (Department.user == current_user) | (current_user.id == 1)).first()
        if dep:
            dep.title = form.title.data
            dep.email = form.email.data
            dep.members = form.members.data
            dep.chief = form.chief.data
            db_sess.commit()
            return redirect('/get_departments')
        else:
            abort(404)
    return render_template('add_dep.html', title='Editing of Department', form=form)


def main():
    db_session.global_init("db/mars_one.db")
    app.register_blueprint(jobs_api.blueprint)
    app.register_blueprint(users_api.blueprint)
    app.run()


if __name__ == '__main__':
    main()
