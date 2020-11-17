from flask import render_template, session, redirect, url_for, request
from settings import app, db
from random import choice, randint
# from numpy.random import randint
from controller import Controller
from model import InfoCodes, MODAL_COLORS, Priorities
from datetime import datetime
# from unidecode import  unidecode

controller = Controller()

# pyuthon3.6
# def int_to_hours_labels(indx: int) -> str:
#     return f'{"0"*(2 - len(str(indx)))}{indx}:00'

# ------------------------------------------------------------------------------------------------- #
#                                        Miscelanious                                               #
# ------------------------------------------------------------------------------------------------- #

# ------------------------------------------------------------------------------------------------- #

def define_contacts():
    response = controller.get_contacts()
    if response:
        return zip(response,
                   [get_random_color() for _ in range(len(response))])
    else:
        return None

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

def patiente_id(name, lastname, phone):
    _dict = str.maketrans({
            'á':'a',
            'é':'e',
            'í':'i',
            'ó':'o',
            'í':'u',
            'ñ':'n',
        })

    return ''.join([name[:2], lastname[:2], str(phone[-4:-1]), str(randint(100, 999))]).lower().translate(_dict)


# ------------------------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------------------------- #
#                                        Home methods                                               #
# ------------------------------------------------------------------------------------------------- #

@app.route('/')
@app.route('/index')
def index():
    print(controller.get_all_users())
    print(controller.get_contacts())
    response = controller.add_user('HBaena', 'hbaena2adan@gmail.com', '', 'Adán', 'Hernández Baena','4615932940', 
        'Secretary', 'Reception 1', False)
    print(response)
    if response is not InfoCodes.USER_ALREADY_EXIST:
        controller.save()

    return render_this_page('index.html', 'BeePlanner')

# @app.route('/')


@app.route('/home')
# @logged_args
def home():
    print(controller.get_patients())
    if 'username' in session:
        # activities, days, init, end = define_schedule()
        contacts = define_contacts()
        appoiments = None
        patients = controller.get_patients()
        return render_this_page('home.html', 'HOME', 
            contacts=contacts,
            appoiments=appoiments,
            patients=patients)
    else:
        return redirect(url_for('index'))

# ------------------------------------------------------------------------------------------------- #

# ------------------------------------------------------------------------------------------------- #
#                                        Login methods                                              #
# ------------------------------------------------------------------------------------------------- #

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

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

# ------------------------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------------------------- #
#                                       Client methods                                              #
# ------------------------------------------------------------------------------------------------- #


@app.route('/patient', methods=['GET', 'POST'])
def patient():
    if request.method == 'GET':
        return render_this_page('patient.html', 'PATIENT')
    else:
        return render_this_page('appointments.html', 'APPOINTMENTS', id=request.form['id'])

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    # print('hello')
    if request.method == 'GET':
        return render_this_page('contact.html', 'CONTACT')
    else:
        # print(request.form)
        # print('hello')
        
        controller.request_contact(request.form['name'], request.form['phone'], 
            request.form['email'], request.form['question'])
        controller.save()
        return render_this_page('thanks.html', 'CONTACT')

# ------------------------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------------------------- #
#                                          Add methods                                              #
# ------------------------------------------------------------------------------------------------- #

@app.route('/add-patient', methods=['POST'])
def add_patient():
    print(request.form)
    name = request.form['name']
    lastname = request.form['lastname']
    gender = request.form['gender']
    phone = request.form['phone']
    email = request.form['email']
    patient_id = patiente_id(name, lastname, phone)
    if not all((name, lastname, gender, phone, email)):
        return redirect(url_for('home'))
    response = controller.add_patient(patient_id, name, lastname, phone, email, gender)
    if response == InfoCodes.SUCCESS:
        controller.save()
        return redirect(url_for('home'))
    
    return render_this_page('404.html', '404'), 404


@app.route('/add-appoiment', methods=['POST'])
def add_appoiment():
    print('Add appoiment')
    print(request.form)
    return redirect(url_for('home'))

@app.route('/add-doctor', methods=['POST'])
def add_doctor():
    # print(request.form)
    print(request.form)
    name = request.form['name']
    lastname = request.form['lastname']
    username = request.form['username']
    password = request.form['password']
    password_1 = request.form['password-1']
    specialty = request.form['specialty']
    description = request.form['description']
    workplace = request.form['workplace']
    phone = request.form['phone']
    email = request.form['email']
    if not all((
            name, lastname, username, password, password_1, 
            specialty, description, workplace, phone, email)):
        return redirect(url_for('home'))
    if password != password_1:
        return redirect(url_for('home'))

    return redirect(url_for('home'))

# ------------------------------------------------------------------------------------------------- #

# ------------------------------------------------------------------------------------------------- #
#                                        Remove methods                                             #
# ------------------------------------------------------------------------------------------------- #

@app.route('/contact/remove/<string:title>')
def remove_contact(title):
    # print('Hello')
    if 'username' in session:
        if controller.remove_contact(title) == InfoCodes.SUCCESS:
            controller.save()
            return redirect(url_for('home'))

    return render_this_page('404.html', '404'), 404
# ------------------------------------------------------------------------------------------------- #

# ------------------------------------------------------------------------------------------------- #
#                                        Other pages                                                #
# ------------------------------------------------------------------------------------------------- #

@app.route('/about')
def about():
    return render_this_page('about.html', 'about us')


@app.errorhandler(404)
def error_404(e):
    return render_this_page('404.html', '404'), 404

@app.route('/test')
def test():
    # return render_template('home.html')
    return render_this_page('404.html', '404')

# ------------------------------------------------------------------------------------------------- #


if __name__ == '__main__':
    db.create_all()
    app.run(threaded=True, port=5000, debug=True)
    # db.close()
