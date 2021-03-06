import random
import json

from flask import Flask, render_template, request, redirect, url_for, session

import src.data as data
import src.constants as constants
from src.forms import GoalForm, RequestForm, BookingForm


app = Flask(__name__)
app.secret_key = 'j08134gjrg894-rg[8rh[g`80=[h84390h`hp9gp9438h43r9'


@app.route('/')
def main_view():
    """Main page"""

    context = {
        'goals': data.goals,
        'teachers': [
            i for i in sorted(
                data.teachers,
                key=lambda teacher: teacher['rating'],
                reverse=True
            )
        ][:5]
    }
    return render_template('index.html', context=context)


@app.route('/all/', methods=['GET', 'POST'])
def all_teachers_view():
    """Page with all the teachers profiles"""

    form = GoalForm()

    context = {
        'teachers': data.teachers,
        'form': form
    }

    if request.method == 'POST':
        if form.goal.data == 'random':
            random.shuffle(data.teachers)
            context['teachers'] = data.teachers
        elif form.goal.data == 'the_best':
            context['teachers'] = [
                i for i in sorted(
                    data.teachers,
                    key=lambda teacher: teacher['rating'],
                    reverse=True
                )
            ]
        elif form.goal.data == 'expensive':
            context['teachers'] = [
                i for i in sorted(
                    data.teachers,
                    key=lambda teacher: teacher['price'],
                    reverse=True
                )
            ]
        elif form.goal.data == 'cheap':
            context['teachers'] = [
                i for i in sorted(
                    data.teachers,
                    key=lambda teacher: teacher['price']
                )
            ]

    return render_template('all.html', context=context)


@app.route('/goals/<goal>/')
def choose_goal_view(goal):
    """Page with teachers sorted by the goal"""

    context = {
        'goal': list(filter(
            lambda list_of_goals: list_of_goals['goal'] == goal,
            data.goals,
        ))[0],
        'teachers': [i for i in data.teachers if goal in i['goals']]
    }

    return render_template('goal.html', context=context)


@app.route('/profiles/<int:teacher_id>/')
def teacher_profile_view(teacher_id):
    """Page for current teacher profile"""

    context = {
        'days': constants.days
    }

    with open('src/db/teachers.json', 'r') as f:
        teacher = json.load(f)[teacher_id]
        goals = list(
            filter(
                lambda goals: goals['goal'] in teacher['goals'],
                data.goals
            )
        )
        context['teacher'] = teacher
        context['goals'] = goals

    return render_template('profile.html', context=context)


@app.route('/request/', methods=['GET', 'POST'])
def request_view():
    """Page for teacher selection form"""

    form = RequestForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            session['data'] = form.data
            return redirect(url_for('request_done_view'))

    return render_template('request.html', form=form)


@app.route('/request_done/')
def request_done_view():
    """Page for redirect after filling in the request form"""

    goal = list(
        filter(
            lambda goals: goals['goal'] == session['data']['goal'],
            data.goals
        )
    )[0]

    context = {
        'data': session['data'],
        'goal': goal
    }

    return render_template('request_done.html', context=context)


@app.route('/booking/<int:teacher_id>/<day>/<time>/', methods=['GET', 'POST'])
def booking_view(teacher_id, day, time):
    """Page for booking the teacher for current day and current time"""

    with open('src/db/teachers.json') as f:
        teacher = list(
            filter(
                lambda x: x['id'] == teacher_id,
                json.load(f)
            )
        )[0]

    form = BookingForm(
        teacher=teacher_id,
        day=day,
        time=time
    )

    if request.method == 'POST':
        if form.validate_on_submit():
            session['day'] = constants.days[form.day.data]
            session['time'] = form.time.data
            session['name'] = form.name.data
            session['phone'] = form.phone.data
            return redirect(url_for('booking_done_view'))

    context = {
        'teacher': teacher,
        'day': constants.days[day],
        'time': time,
        'form': form
    }

    return render_template('booking.html', context=context)


@app.route('/booking_done/')
def booking_done_view():
    """Page for redirect after filling in the booking form"""

    context = {
        'day': session['day'],
        'time': session['time'],
        'name': session['name'],
        'phone': session['phone']
    }

    return render_template('booking_done.html', context=context)


if __name__ == '__main__':
    app.run()
