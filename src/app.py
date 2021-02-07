import random
from flask import Flask, render_template, request
from forms import GoalForm
import data


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
                key=lambda x: x['rating'],
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
            context.update(
                {
                    'teachers': data.teachers
                }
            )
        elif form.goal.data == 'the_best':
            context.update(
                {
                    'teachers': [
                        i for i in sorted(
                            data.teachers,
                            key=lambda x: x['rating'],
                            reverse=True
                        )
                    ]
                }
            )
        elif form.goal.data == 'expensive':
            context.update(
                {
                    'teachers': [
                        i for i in sorted(
                            data.teachers,
                            key=lambda x: x['price'],
                            reverse=True
                        )
                    ]
                }
            )
        elif form.goal.data == 'cheap':
            context.update(
                {
                    'teachers': [
                        i for i in sorted(
                            data.teachers,
                            key=lambda x: x['price']
                        )
                    ]
                }
            )
    return render_template('all.html', context=context)


@app.route('/goals/<goal>/')
def choose_goal_view(goal):
    """Page with teachers sorted by the goal"""
    return render_template('goal.html')


@app.route('/profiles/<teacher_id>/')
def teacher_profile_view(teacher_id):
    """Page for current teacher profile"""
    return render_template('profile.html')


@app.route('/request/')
def request_view():
    """Page for teacher selection form"""
    return render_template('request.html')


@app.route('/request_done/')
def request_done_view():
    """Page for redirect after filling in the request form"""
    return render_template('request_done.html')


@app.route('/booking/<teacher_id>/<day>/<time>/')
def booking_view(teacher_id, day, time):
    """Page for booking the teacher for current day and current time"""
    return render_template('booking.html')


@app.route('/booking_done/')
def booking_done_view():
    """Page for redirect after filling in the booking form"""
    return render_template('booking_done.html')


if __name__ == '__main__':
    app.run(debug=True)
