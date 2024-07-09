from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length
from wtforms_sqlalchemy.fields import QuerySelectField

from task_manager.repositories.status_repository import StatusRepository



class TaskCreateForm(FlaskForm):
    title = StringField('Название задачи', validators=[DataRequired(), Length(1, 100)],
                             render_kw={"placeholder": "Введите название задачи"})
    description = TextAreaField('Описание', render_kw={"placeholder": "Введите описание задачи"})
    status = QuerySelectField('Выберите статус задачи', query_factory=lambda: StatusRepository().get_statuses(), allow_blank=True, get_label='title')
    submit = SubmitField('Создать', render_kw={"class": "btn btn"})

class TaskUpdateForm(FlaskForm):
    title = StringField('Название задачи', validators=[DataRequired(), Length(1, 100)],
                             render_kw={"placeholder": "Введите название задачи"})
    description = TextAreaField('Описание', render_kw={"placeholder": "Введите описание задачи"})
    status = QuerySelectField('Выберите статус задачи', query_factory=lambda: StatusRepository().get_statuses(), allow_blank=True, get_label='title')
    submit = SubmitField('Изменить', render_kw={"class": "btn btn"})


class DeleteForm(FlaskForm):
    pass#submit = SubmitField('Удалить', render_kw={"class": "btn btn"})
