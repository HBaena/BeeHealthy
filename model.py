from settings import db
from sqlalchemy import desc, asc

def send_email(email_in, email_out, text):
    pass



MODAL_COLORS = (
    ' lime',
    ' cyan darken-1',
    'lime accent-1 ',
    'orange accent-4',
    'yellow',
    'deep-orange accent-1',
    'cyan darken-2 ',
    'cyan',
    ' amber accent-3',
    ' amber',
    'orange lighten-1',
    ' red lighten-2 ',
    'red accent-2 ',
    'light-blue darken-4',
    ' green darken-3',
    'yellow accent-2',
    'teal accent-3 ',
    'purple accent-2',
    'light-green accent-3',
    'light-green darken-4',
    'pink darken-1 ',
    ' pink darken-3',
    ' purple lighten-2',
    ' teal lighten-1',
    ' purple accent-1 ',
    ' deep-purple accent-1 ',
    'indigo lighten-1 ',
    ' blue lighten-4 ',
    ' orange darken-4',
    ' blue-grey darken-1',
    'brown lighten-2',
    ' orange lighten-1',
    '  light-green accent-4',
    'teal',
    'red darken-4',
    ' red lighten-3',   'amber darken-4',
    'teal darken-1',
    ' light-blue accent-1 ',

)


class Priorities:
    NONE = 0
    HIGH = 1
    MEDIUM = 2
    LOW = 3


class InfoCodes:
    """docstring for InfoCodes"""
    ERROR = 0
    USER_NOT_FOUND = -1
    USERNAME_NOT_FOUND = -2
    EMAIL_NOT_FOUND = -3
    WRONG_PASSWORD = -4
    SUCCESS = -5
    USER_ALREADY_EXIST = -6
    ACTIVITY_ALREADY_EXIST = -7


class Model:
    """docstring for Model"""

    def __init__(self, session=db.session):
        self.__session = session

# ------------------------------------------------------------------------------------------------- #
#                                          db methods                                               #
# ------------------------------------------------------------------------------------------------- #

    def save_changes(self):
        # If there are modifica
        # tions without be added to the tables returns True
        if self.__session.dirty:
            # Update tables
            self.__session.new
        self.__session.commit()

    def undo_changes(self):
        self.__session.rollback()

    def close_session(self):
        self.__session.close()



# ------------------------------------------------------------------------------------------------- #
#                                            Contact                                                #
# ------------------------------------------------------------------------------------------------- #

    def create_contact(self, name, phone, email, question):
        self.__session.add(Contact(name=name, phone=phone, email=email, question=question))

    def read_contact(self, contact_id):
        return self.__session.query(Contact).filter(
                Contact.contact_id == contact_id).first()

    def read_contacts(self):
        return self.__session.query(Contact).all()

    def delete_contact(self, contact):
        self.__session.delete(contact)


# ------------------------------------------------------------------------------------------------- #
#                                             User                                                  #
# ------------------------------------------------------------------------------------------------- #

    def create_appoiment(self, id_doctor, id_patient, date, description, weight=0, height=0, temperature=0, heart_rate=0, done=False):
        self.__session.add(Appointment(
            username=id_doctor, id_patient=id_patient, date=date, 
            description=description, weight=weight, height=height, 
            temperature=temperature, heart_rate=heart_rate, done=done))
        self.save_changes()

    def read_appoiment(self, _filter):
        return self.__session.query(Appointment).filter(_filter).first()

    def read_appoiments(self, _filter=None):
            return self.__session.query(Appointment).filter(_filter if not _filter else Appointment).all()

    def read__all_appoiments(self):
            return self.__session.query(Appointment).order_by(asc(Appointment.date)).all()

    def delete_appoiment(self, appointment):
        self.__session.delete(appointment)

# ------------------------------------------------------------------------------------------------- #
#                                             User                                                  #
# ------------------------------------------------------------------------------------------------- #

    def create_patient(self, id_patient, name, lastname, phone, email, gender, weight=-1, height=-1, temperature=-1, heart_rate=-1):
        self.__session.add(Patient(
            id_patient=id_patient, name=name, 
            lastname=lastname, phone=phone, 
            email=email, gender=gender, 
            weight=weight, height=height, 
            temperature=temperature, 
            heart_rate=heart_rate))

    def read_patient(self, _filter):
        return self.__session.query(Patient).filter(_filter).first()

    def read_patients(self,):
            return self.__session.query(Patient).all()

    def delete_patient(self, patient):
        self.__session.delete(patient)

# ------------------------------------------------------------------------------------------------- #
#                                             User                                                  #
# ------------------------------------------------------------------------------------------------- #

    def create_user(self, username, email, password, name, lastname, phone, speciality, workplace, doctor):
        self.__session.add(User(
            username=username, email=email, password=password, 
            name=name, lastname=lastname,phone=phone, 
            speciality=speciality, workplace=workplace, doctor=doctor))

    def read_user(self, _filter):
        return self.__session.query(User).filter(_filter).first()


    def read_users(self, _filter=None):
            return self.__session.query(User).filter(_filter if not _filter else User).all()

    def update_user(self, user, username=None, email=None, password=None, name=None, lastname=None, 
                                phone=None, speciality=None, workplace=None, doctor=None):
        if not user:
            return False
        if username:
            if self.read_user(username=username):
                return False
            if email:
                if self.read_user(email=email):
                    return False
            user.email = email
            user.username = username
        if password:
            user.password = password
        if name:
            user.name = name
        if lastname:
            user.lastname = lastname
        if phone:
            user.phone = phone
        if speciality:
            user.speciality = speciality
        if workplace:
            user.workplace = workplace
        if doctor:
            user.doctor = doctor


        return user
    def delete_user(self, user):
        self.__session.delete(user)

    def verify_user(self, token, password):
        user = self.__session.query(User).filter(
            (User.username == token) | (User.email == token)).first()
        if not user:
            return InfoCodes.USER_NOT_FOUND
        if not user.password == password:
            return InfoCodes.WRONG_PASSWORD
        else:
            return InfoCodes.SUCCESS


# ------------------------------------------------------------------------------------------------- #
#                                             Models                                                #
# ------------------------------------------------------------------------------------------------- #


class User(db.Model):
    """docstring for User"""

    __tablename__ = "User"
    username = db.Column(db.String(30), nullable=False, primary_key=True)
    email = db.Column(db.String(30), nullable=True)
    password = db.Column(db.String(10), nullable=False)
    name = db.Column(db.String(30), nullable=False)
    lastname = db.Column(db.String(30), nullable=False)
    phone = db.Column(db.String(12), nullable=True)
    speciality = db.Column(db.Text(length=None), nullable=False)
    workplace = db.Column(db.String(20), nullable=True)
    doctor = db.Column(db.Boolean(),nullable=True)
    # db.relationship must      be in the parent table
    appointment = db.relationship(
        'Appointment', backref='User', cascade="all, delete-orphan")
    

    def __repr__(self):
        return '{},{},{},{},{},{}'.format(self.username, self.email,
                                          self.password, self.name,
                                          self.lastname, self.phone,
                                          self.speciality, self.workplace,
                                          self.doctor)
    def fullname(self):
        return '{} {}'.format(self.name, self.lastname)


class Appointment(db.Model):
    """docstring for Appointment"""

    __tablename__ = "Appointment"
    id_appointment = db.Column(db.Integer, nullable=False, primary_key=True)
    date = db.Column(db.DateTime(), nullable=False)
    description = db.Column(db.Text(length=None), nullable=False, )
    weight = db.Column(db.Float(), nullable=True)
    height = db.Column(db.Float(), nullable=True)
    temperature = db.Column(db.Float(), nullable=True)
    heart_rate = db.Column(db.Float(), nullable=True)
    done = db.Column(db.Boolean(), nullable=False)
    username = db.Column(db.String(30),db.ForeignKey(
               'User.username'),nullable=False )
    id_patient = db.Column(db.Integer,db.ForeignKey(
               'Patient.id_patient'),nullable=False )
    
    def __repr__(self):
        return '{},{},{},{},{},{},{}, {}, {}, {}|'.format(self.id_appointment, self.date,
                                            self.description, self.weight,
                                            self.height, self.temperature,
                                            self.heart_rate, self.done,
                                            self.username, self.id_patient)

class Patient(db.Model):
    """docstring for Patient"""

    __tablename__ = "Patient"
    id_patient = db.Column(db.String(10), nullable=True, primary_key=True)
    name = db.Column(db.String(300), nullable=False)
    lastname = db.Column(db.String(30), nullable=False)
    phone = db.Column(db.String(12), nullable=False)
    email = db.Column(db.String(40), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    weight = db.Column(db.Float(), nullable=False)
    height = db.Column(db.Float(), nullable=False)
    temperature = db.Column(db.Float(), nullable=False)
    heart_rate = db.Column(db.Float(), nullable=False)
    # db.relationship must      be in the parent table
    appointment = db.relationship(
        'Appointment', backref='Patient', cascade="all, delete-orphan")
         
    def __repr__(self):
        return '{},{},{},{},{},{}'.format(self.id_patient, self.name,
                                          self.lastname, self.phone,
                                          self.gender, self.weight,
                                          self.height, self.temperature,
                                          self.heart_rate)
    def fullname(self):
        return '{} {}'.format(self.name, self.lastname)

    def contact(self):
        return '{} {}'.format(self.name, self.lastname), self.phone



class Contact(db.Model):
    """docstring for Contact"""
    __tablename__ = "Contact"
    contact_id = db.Column(db.Integer , primary_key=True , autoincrement=True)
    name = db.Column(db.String(30), nullable=True)
    phone = db.Column(db.String(12), nullable=True)
    email = db.Column(db.String(30), nullable=False)
    question = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '{}, {}, {}, {}|'.format(
            self.name,
            self.phone,
            self.email,
            self.question,
            )