from flask import render_template, session, redirect, url_for, request
from settings import app, db
from random import choice
# from numpy.random import randint
from controller import Controller
from model import InfoCodes, MODAL_COLORS, Priorities
from datetime import datetime

controller = Controller()

# pyuthon3.6
# def int_to_hours_labels(indx: int) -> str:
#     return f'{"0"*(2 - len(str(indx)))}{indx}:00'


def define_notes():
    response = controller.get_notes(username=session['username'])
    if response:
        activities = []
        for i in range(len(response)):
            r = controller.get_activity_name(response[i].activity_id)
            if r:
                activities.append(r)
            else:
                activities.append('None')

        # return None
        return zip(response,
                   [get_random_color() for _ in range(len(response))],
                   activities)
    else:
        return None


def define_schedule():
    activities = controller.get_activities(session['username'])
    days = {
        'monday': [0]*24,
        'tuesday': [0]*24,
        'wednesday': [0]*24,
        'thursday': [0]*24,
        'friday': [0]*24,
    }
    if activities:
        schedule = []
        for activity in activities:
            response = controller.get_schedule(activity.activity_id)
            if response:
                schedule.extend(response)

        for sch in schedule:
            for day in days.keys():
                if getattr(sch, day):
                    hour, duration = map(int, getattr(
                        sch, day).replace(':00', '').split())
                    title = controller.get_activity_name(
                        activity_id=sch.activity_id)
                    idx = sch.activity_id if sch.activity_id < len(
                        MODAL_COLORS) else int(sch.activity_id/len(MODAL_COLORS))
                    for i in range(duration):
                        days[day][hour+i] = (sch.activity_id,
                                             title, MODAL_COLORS[idx])
        init = 12
        end = 20
        for i in range(12):
            if  any((
                    days['monday'][i],
                    days['tuesday'][i],
                    days['wednesday'][i],
                    days['thursday'][i],
                    days['friday'][i])):
                init = i
                break
        for i in range(23, 12, -1):
            if  any((
                    days['monday'][i],
                    days['tuesday'][i],
                    days['wednesday'][i],
                    days['thursday'][i],
                    days['friday'][i])):
                end = i
                break

        return activities, days, init, end
    else:
        return None, None, None, None


def get_random_color():
    return choice(MODAL_COLORS)


def render_this_page(url, title, **kwargs):
    kwargs = {**logged_args(), **kwargs}
    return render_template(url, title=title, **kwargs)


def logged_args():
    if 'username' not in session:
        status_log = 'Login'
        icon_log = 'account_circle'
        redirect_log = 'login'

        status_account = 'Sign up'
        icon_account = 'person_add'
        redirect_account = 'register'
        user = None
    else:
        status_account = session['username'][:10]
        icon_account = 'account_box'
        # redirect_account = 'profile'

        status_log = 'Logout'
        icon_log = 'exit_to_app'
        redirect_log = 'logout'
        user = controller.get_user(session['username'])

    return locals()


@app.route('/test')
def test():
    # return render_template('home.html')
    return render_this_page('404.html', '404')


@app.route('/')
@app.route('/index')
def index():
    print(controller.get_all_users())
    return render_this_page('index.html', 'BeePlanner')

# @app.route('/')


@app.route('/home')
# @logged_args
def home():
    notes = None
    if 'username' in session:
        activities, days, init, end = define_schedule()
        notes = define_notes()
        return render_this_page('home.html', 'HOME', notes=notes,
                                activities=activities,
                                days=days, init=init, end=end)
    else:
        return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_this_page('login.html', 'LOGIN')
    else:
        if request.form:
            email = request.form['email']
            password = request.form['password']
            response = controller.login(email, password)
            if response == InfoCodes.USER_NOT_FOUND:
                return render_this_page('login.html', 'LOGIN')
            if response == InfoCodes.WRONG_PASSWORD:
                return render_this_page('login.html', 'LOGIN')
            if response == InfoCodes.SUCCESS:
                session['username'] = controller.get_username(email)
                return redirect(url_for('home'))

    return render_this_page('login.html', 'LOGIN')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if 'username' in session or request.method == 'GET':
        return render_this_page('register.html', 'REGISTER')
    elif request.method == 'POST':
        username = request.form['username']
        # name = request.form['name']
        # lastname = request.form['lastname']
        # phone = request.form['phone']
        email = request.form['email']
        password = request.form['password']
        if not all([username, 
            # name, lastname, phone, 
            email, password]):
            return render_this_page('register.html', 'REGISTER')
        else:
            response = controller.add_user(username, email, password,
                                           '', '', '')
            if response == InfoCodes.USER_ALREADY_EXIST:
                return render_this_page('register.html', 'REGISTER')
            else:
                controller.save()
                session['username'] = controller.get_username(email)
                return redirect(url_for('home'))
    return render_this_page('register.html', 'REGISTER')


@app.route('/schedule')
def schedule():
    return render_template('schedule.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))


@app.route('/activity')
def act():
    return render_template('404.html'), 404


@app.route(('/activity/<string:description>/'
            '<string:priority>/<string:location>/'
            '<string:title>/<string:monday>/'
            '<string:tuesday>/<string:wednesday>/'
            '<string:thursday>/<string:friday>/'))
def activity(description, priority=None, location=None,
             title=None, monday=None, tuesday=None,
             wednesday=None, thursday=None, friday=None):
    monday, tuesday, wednesday, thursday, friday = map(
        lambda s: '' if 'null' in s else s, [monday, tuesday,
                                             wednesday, thursday,
                                             friday])
    if 'username' in session:
        response = controller.add_activity(session['username'], description,
                                           priority, location, title)
        if response == InfoCodes.ACTIVITY_ALREADY_EXIST:
            return redirect(url_for('home'))

        controller.add_schedule(monday, tuesday, wednesday, thursday,
                                friday, response)
        controller.save()
        return redirect(url_for('home'))

    return render_template('404.html'), 404


@app.route('/activity/remove/<string:title>')
def remove_activity(title):
    if 'username' in session:
        if controller.remove_activity(title) == InfoCodes.SUCCESS:
            controller.save()
            return redirect(url_for('home'))

    return render_template('404.html'), 404


@app.route('/note/remove/<int:id>')
def remove_note(id):
    if 'username' in session:
        if controller.remove_note(id) == InfoCodes.SUCCESS:
            controller.save()
            return redirect(url_for('home'))

    return render_template('404.html'), 404


@app.route('/note/<string:content>/<string:priority>/<string:due_date>/<string:title>')
def note(content=None, priority=None, due_date=None, title=None):
    if 'username' in session:
        creation_date = datetime.today()
        username = session['username']
        if content == 'undefined':
            return render_template('404.html'), 404

        if 'None' not in due_date:
            due_date = datetime.strptime(due_date, '%d-%m-%Y').date()
        else:
            due_date = None
        if title:
            activity_id = controller.get_activity_id(title)
        else:
            activity_id = 0
        controller.add_note(content, priority, due_date,
                            creation_date, username, activity_id)
        controller.save()
        return redirect(url_for('home'))

    return render_template('404.html'), 404

@app.route('/about')
def about():
    return render_this_page('about.html', 'about us')


@app.errorhandler(404)
def error_404(e):
    return render_this_page('404.html', '404'), 404


if __name__ == '__main__':
    db.create_all()
    app.run(threaded=True, port=5000, debug=True)
    # db.close()
