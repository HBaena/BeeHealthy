from flask import render_template, session, redirect, url_for, request
from settings import app, db
from random import choice, randint
# from numpy.random import randint
from controller import Controller
from model import InfoCodes, MODAL_COLORS, Priorities
from datetime import datetime, timedelta
# from unidecode import  unidecode
# 
# OOPS_IMG =  url_for('static', filename='img/error.png')
# SUCCESS_IMG =  url_for('static', filename='img/success.png')
# E404_IMG =  url_for('static', filename='img/404.png')
# CONTACT_IMG =  url_for('static', filename='img/contact.png')

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
        return zip(range(len(response)), response,
                   [get_random_color() for _ in range(len(response))])
    else:
        return None

def define_appoiments(patiente_id=None, username=None):
    response = list(controller.get_appoiments_unchecked(patiente_id))
    if username:
        response = list(filter(lambda x: x.username == username, response))
    if response:
        return [(
            i, x.id_appointment, x.date, x.description, controller.get_user(x.username).fullname(), 
            *controller.get_patient(x.id_patient).contact()) for i, x in enumerate(response)]
    else:
        return None

def define_appoiments_c(patiente_id=None, username=None):
    response = list(controller.get_appoiments_checked(patiente_id))
    if username:
        response = list(filter(lambda x: x.username == username, response))
    if response:
        return [(
            i, x.id_appointment, x.date, x.description, controller.get_user(x.username).fullname(), 
            *controller.get_patient(x.id_patient).contact()) for i, x in enumerate(response)]
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
    print(controller.get_roots())

    response = controller.add_user('root', 'root@gmail.com', 'rootroot', 'Adán', 'Hernández Baena','4615932940', 
        'Secretary', 'Reception 1', False)
    if response is not InfoCodes.USER_ALREADY_EXIST: controller.save()
    response = controller.add_patient(patiente_id('Andres Manuel', 'López Obrador', '1234567890'), 
        'Andres Manuel', 'López Obrador', '1234567890', 'amlo@gmail.com', 'Male')
    if response is not InfoCodes.USER_ALREADY_EXIST: controller.save()
    response = controller.add_user('Grey', 'grey', 'password', 'Meredit', 'Grey', '0123456789', speciality='Cirugía', workplace='Consultorio 3', doctor=True)
    if response is not InfoCodes.USER_ALREADY_EXIST: controller.save()

    return render_this_page('index.html', 'BeeHealthy')

# @app.route('/')


@app.route('/home')
# @logged_args
def home():
    if 'username' in session:
        # activities, days, init, end = define_schedule()
        appoiments = define_appoiments()
        contacts = define_contacts()
        patients = controller.get_patients()
        doctors = controller.get_doctors()
        if len(doctors):
            doctors = zip(range(len(doctors)), doctors)
        else:
            doctors = None
        if len(patients):
            patients = zip(range(len(patients)), patients)
        else:
            patients = None

        return render_this_page('home.html', 'HOME', 
            contacts=contacts,
            appoiments=appoiments,
            patients=patients,
            doctors=doctors
            )
    else:
        return redirect(url_for('index'))

@app.route('/doctor')
# @logged_args
def doctor():
    # print(list(controller.get_appoiments_unchecked('adhe294532')))
    if 'username' in session:
        # activities, days, init, end = define_schedule()
        appoiments = define_appoiments(username=session['username'])
        today = datetime.today()
        week = timedelta(days=7)
        this_week = list(filter(lambda x:x[2] >= today and x[2] <= (today+week),  appoiments))
        later = list(filter(lambda x:x[2] > (today+week),  appoiments))
        if not len(this_week): this_week=None
        if not len(later): later=None
        return render_this_page('doctor.html', 'Doctor Panel', 
                this_week=this_week,
                later=later, 
            )
    else:
        return redirect(url_for('index'))

# ------------------------------------------------------------------------------------------------- #

# ------------------------------------------------------------------------------------------------- #
#                                        Login methods                                              #
# ------------------------------------------------------------------------------------------------- #

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('doctor', None)
    return redirect(url_for('home'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_this_page('login.html', 'LOGIN')
    else:
        if request.form:
            email = request.form['email'].strip()
            password = request.form['password'].strip()
            response = controller.login(email, password)
            if response == InfoCodes.USER_NOT_FOUND:
                return render_this_page('login.html', 'LOGIN')
            if response == InfoCodes.WRONG_PASSWORD:
                return render_this_page('login.html', 'LOGIN')
            if response == InfoCodes.SUCCESS:
                session['username'] = controller.get_username(email)
                session['doctor'] = controller.get_user(email).doctor
                print(session['doctor'])
            if session['doctor']:
                return redirect(url_for('doctor'))
            else:
                return redirect(url_for('home'))

    return render_this_page('login.html', 'LOGIN')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if 'username' in session or request.method == 'GET':
        return render_this_page('register.html', 'REGISTER')
    elif request.method == 'POST':
        username = request.form['username'].strip()
        # name = request.form['name'].strip()
        # lastname = request.form['lastname'].strip()
        # phone = request.form['phone'].strip()
        email = request.form['email'].strip()
        password = request.form['password'].strip()
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
        patient_id=request.form['id'].strip()
        unchecked = list(controller.get_appoiments_unchecked(patient_id))
        checked = list(controller.get_appoiments_checked(patient_id))    
        print(list(controller.get_appoiments_unchecked(patient_id)))
        print(checked)
        return render_this_page('patient-panel.html', 'APPOINTMENTS', 
            unchecked=zip(range(len(unchecked)), unchecked) if len(unchecked) else None, 
            checked=zip(range(len(checked)), checked) if len(checked) else None
            )

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    # print('hello')
    if request.method == 'GET':
        return render_this_page('contact.html', 'CONTACT')
    else:
        # print(request.form)
        # print('hello')
        
        controller.request_contact(request.form['name'].strip(), request.form['phone'].strip(), 
            request.form['email'].strip(), request.form['question'].strip())
        controller.save()
        return render_this_page('thanks.html', 'CONTACT')

# ------------------------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------------------------- #
#                                          Add methods                                              #
# ------------------------------------------------------------------------------------------------- #

@app.route('/add-patient', methods=['POST'])
def add_patient():
    print(request.form)
    name = request.form['name'].strip()
    lastname = request.form['lastname'].strip()
    gender = request.form['gender'].strip()
    phone = request.form['phone'].strip()
    email = request.form['email'].strip()
    patient_id = patiente_id(name, lastname, phone)
    if not all((name, lastname, gender, phone, email)):
        print('NOPE')
        return render_this_page('error.html', 'UNSPECTED ERROR', img=url_for('static', filename='img/error.png'), msg=None, code=None)

    response = controller.add_patient(patient_id, name, lastname, phone, email, gender)
    if response == InfoCodes.SUCCESS:
        controller.save()
        return render_this_page('error.html', 'SUCCESS', img=url_for('static', filename='img/success.png'), msg='Remember this code it is personal and secret', code=patient_id)
    
    return render_this_page('error.html', 'UNSPECTED ERROR', img=url_for('static', filename='img/error.png'), msg=None, code=None)
    # return render_this_page('404.html', '404'), 404


@app.route('/add-appoiment', methods=['POST'])
def add_appoiment():
    print(request.form)
    patient = request.form['patient'].strip()
    doctor = request.form['doctor'].strip()
    description = request.form['description'].strip()
    date = request.form['date'].strip()
    hour = request.form['hour'].strip()
    date = datetime.strptime(' '.join([date, hour]), '%d-%m-%Y %H:%M')
    if controller.add_appoiment(doctor, patient, date, description) == InfoCodes.SUCCESS:
        controller.save()
        return render_this_page('error.html', 'SUCCESS', img=url_for('static', filename='img/success.png'), msg=None, code=None)


    return render_this_page('error.html', 'Error', img=url_for('static', filename='img/user-email.png'), msg=None, code=None)

@app.route('/add-doctor', methods=['POST'])
def add_doctor():
    name = request.form['name'].strip()
    lastname = request.form['lastname'].strip()
    username = request.form['username'].strip()
    password = request.form['password'].strip()
    password_1 = request.form['password-1'].strip()
    specialty = request.form['specialty'].strip()
    # description = request.form['description'].strip()
    workplace = request.form['workplace'].strip()
    phone = request.form['phone'].strip()
    email = request.form['email'].strip()
    if not all((
            name, lastname, username, password, password_1, 
            specialty, workplace, phone, email)):
        print('Any null')
        return render_this_page('error.html', 'WRONG PASSWORD', img=uDrl_for('static', filename='img/error.png'), msg=None, code=None)
    if password != password_1:
        print('Passwords not don\'t match')
        return render_this_page('error.html', 'WRONG PASSWORD', img=uDrl_for('static', filename='img/error.png'), msg=None, code=None)

    response = controller.add_user(username, email, password, name, lastname, phone, specialty, workplace, True)
    if response == InfoCodes.SUCCESS:
        print('Added' )
        controller.save()
        return render_this_page('error.html', 'SUCCESS', img=url_for('static', filename='img/success-user.png'), msg=None, code=None)
        # return redirect(url_for('home'))

    return render_this_page('error.html', 'Error', img=url_for('static', filename='img/user-email.png'), msg=None, code=None)

# ------------------------------------------------------------------------------------------------- #

# ------------------------------------------------------------------------------------------------- #
#                                        Remove methods                                             #
# ------------------------------------------------------------------------------------------------- #

@app.route('/contact/remove/<string:contact_id>')
def remove_contact(contact_id):
    print(contact_id)
    if 'username' in session:
        if controller.remove_contact(contact_id) == InfoCodes.SUCCESS:
            controller.save()
            return redirect(url_for('home'))

    return render_this_page('404.html', '404'), 404

@app.route('/doctor/remove/<string:doctor_id>')
def remove_doctor(doctor_id):
    print(doctor_id)
    if 'username' in session:
        if controller.remove_user(doctor_id) == InfoCodes.SUCCESS:
            controller.save()
            return redirect(url_for('home'))

    return render_this_page('404.html', '404'), 404

@app.route('/patient/remove/<string:patient_id>')
def remove_patient(patient_id):
    print(patient_id)
    if 'username' in session:
        if controller.remove_patient(patient_id) == InfoCodes.SUCCESS:
            controller.save()
            return redirect(url_for('home'))

    return render_this_page('404.html', '404'), 404

@app.route('/appoiment/remove/<string:appoiment_id>')
def remove_appoiment(appoiment_id):
    print(appoiment_id)

    if 'username' in session:
        if controller.remove_appoiment(appoiment_id) == InfoCodes.SUCCESS:
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

@app.route('/message')
def error_page(title, img):
    return render_this_page('error.html', title, img)


@app.route('/test')
def test():
    # return render_template('home.html')
    return render_this_page('404.html', '404')

# ------------------------------------------------------------------------------------------------- #


if __name__ == '__main__':
    db.create_all()
    app.run(threaded=True, port=5000, debug=True)
    # db.close()
