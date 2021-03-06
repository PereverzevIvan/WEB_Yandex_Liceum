from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, IntegerField, BooleanField, SelectField
from wtforms.validators import DataRequired


class AddJobForm(FlaskForm):
    job = StringField('Название работы', validators=[DataRequired()])
    work_size = StringField('Продолжительность', validators=[DataRequired()])
    collaborators = StringField('Участники', validators=[DataRequired()])
    is_finished = BooleanField('Закончена ли')
    team_leader = IntegerField('Лидер команды', validators=[DataRequired()])
    categories = SelectField('Категория')
    submit = SubmitField('Submit')
