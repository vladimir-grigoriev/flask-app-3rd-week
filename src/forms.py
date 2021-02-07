from flask_wtf import FlaskForm
from wtforms import SelectField


class GoalForm(FlaskForm):
    goal = SelectField(
        label='',
        choices=[
            ('random', 'В случайном порядке'),
            ('the_best', 'Сначала лучшие по рейтингу'),
            ('expensive', 'Сначала дорогие'),
            ('cheap', 'Сначала недорогие')
        ]
    )
