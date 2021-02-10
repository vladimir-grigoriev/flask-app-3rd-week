from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, RadioField, IntegerField
from wtforms import validators
import data


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


class RequestForm(FlaskForm):
    goal = RadioField(
        label='Какая цель занятий?',
        validators=[
            validators.input_required(message='Выберите цель занятий')
        ],
        choices=[
            (i['goal'], i['description']) for i in data.goals
        ]
    )
    time = RadioField(
        label='Сколько времени есть?',
        validators=[
            validators.input_required(
                message='Выберите количество свободного времени'
            )
        ],
        choices=[
            ('1-2', '1-2 часа в неделю'),
            ('3-5', '3-5 часов в неделю'),
            ('5-7', '5-7 часов в неделю'),
            ('7-10', '7-10 часа в неделю')
        ]
    )
    name = StringField(
        label='Вас зовут',
        validators=[
            validators.input_required(message='123'),
            validators.regexp(
                r'[a-zA-Zа-яА-ЯёЁ]{2,}',
                message='Поле может содержать только буквы русского\
                         и английского алфавита должно быть не короче\
                         двух символов'
            )
        ]
    )
    phone = StringField(
        label='Ваш телефон',
        validators=[
            validators.input_required(message='123'),
            validators.regexp(
                r'[0-9\+]{3,}',
                message='Поле должно быть не короче трех символов,\
                         может содержать только цифры и знак "+"'
            )
        ]
    )


class BookingForm(FlaskForm):
    name = StringField(
        label='Вас зовут',
        validators=[
            validators.DataRequired(
                message='Введите имя'
            ),
            validators.regexp(
                r'[a-zA-Zа-яА-ЯёЁ]{2,}',
                message='Поле может содержать только буквы русского\
                         и английского алфавита должно быть не короче\
                         двух символов'
            )
        ]
    )
    phone = StringField(
        label='Ваш телефон',
        validators=[
            validators.input_required(message='123'),
            validators.regexp(
                r'[0-9\+]{3,}',
                message='Поле должно быть не короче трех символов,\
                         может содержать только цифры и знак "+"'
            )
        ]
    )
    day = StringField(
        label='День'
    ),
    time = StringField(
        label='Время'
    )
    teacher = IntegerField(
        label='ID учителя',
        validators=[
            validators.NumberRange(
                min=0,
                max=len(data.teachers)-1,
                message='Значение вне диапазона'
            )
        ]
    )
