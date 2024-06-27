from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length
from wtforms_sqlalchemy.fields import QuerySelectMultipleField



class TaskCreateForm(FlaskForm):
    title = StringField('Название задачи', validators=[DataRequired(), Length(1, 100)],
                             render_kw={"placeholder": "Введите название задачи"})
    description = TextAreaField('Описание', render_kw={"placeholder": "Введите описание задачи"})
    submit = SubmitField('Создать', render_kw={"class": "btn btn"})

class TaskUpdateForm(FlaskForm):
    title = StringField('Название задачи', validators=[DataRequired(), Length(1, 100)],
                             render_kw={"placeholder": "Введите название задачи"})
    description = TextAreaField('Описание', render_kw={"placeholder": "Введите описание задачи"})
    submit = SubmitField('Изменить', render_kw={"class": "btn btn"})


class DeleteForm(FlaskForm):
    submit = SubmitField('Удалить', render_kw={"class": "btn btn"})