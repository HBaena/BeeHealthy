from settings import db

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
    # ------------------------- #
    #       GENERAL METHODS     #
    # ------------------------- #

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

    # ------------------------- #
    #       USER METHODS        #
    # ------------------------- #

    def create_user(self, username, email, password, name, lastname, phone):
        self.__session.add(User(username=username, email=email,
                                password=password, name=name,
                                lastname=lastname, phone=phone,))

    def read_user(self, username=None, email=None):
        if username:
            response = self.__session.query(User).filter(
                User.username == username).first()
            if response:
                return response
            else:
                return InfoCodes.ERROR
        elif email:
            response = self.__session.query(User).filter(
                User.email == email).first()
            if response:
                return response
            else:
                return InfoCodes.ERROR
        return InfoCodes.ERROR

    def read_users(self):
        return self.__session.query(User).all()

    def update_user(self, user, username=None, email=None,
                    password=None, name=None, lastname=None, phone=None):
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

    # ------------------------- #
    #       ACTIVITY METHODS    #
    # ------------------------- #
    def create_schedule(self, monday, tuesday, wednesday, thursday,
                        friday, activity_id):
        self.__session.add(Schedule(monday=monday, tuesday=tuesday,
                                    wednesday=wednesday, thursday=thursday,
                                    friday=friday, activity_id=activity_id))

    def read_schedule(self, activity_id):
        return self.__session.query(Schedule).join(Activity).filter(
            Activity.activity_id == activity_id).all()

    def create_acitivity(self,  title, description,
                         priority, location, username, ):
        self.__session.add(Activity(description=description,
                                    title=title, priority=priority,
                                    location=location, username=username,))

    def read_activity(self, title=None, activity_id=None):
        if title:
            response = self.__session.query(Activity).filter(
                Activity.title == title).first()
        else:
            response = self.__session.query(Activity).filter(
                Activity.activity_id == activity_id).first()

        if response:
            return response
        else:
            return InfoCodes.ERROR

    def read_activities(self, username=None):
        return self.__session.query(Activity).join(
            User).filter(User.username == username).all()

    def delete_activity(self, activity):
        self.__session.delete(activity)

    def create_note(self, content, priority, due_date,
                    creation_date, username,
                    activity_id,):
        self.__session.add(Note(content=content, priority=priority,
                                due_date=due_date,
                                creation_date=creation_date,
                                username=username,
                                activity_id=activity_id,))

    def read_notes(self, username=None, activity_id=None):
        if username:
            return self.__session.query(Note).join(
                User).filter(User.username == username).all()
        elif activity_id:
            return self.__session.query(Note).join(
                Activity).filter(Activity.activity_id == activity_id).all()

    def read_note(self, username, activity_id, content):
        return self.__session.query(Note).filter(
            Note.username == username & Note.activity_id == activity_id &
            Note.content == content).first()

    def read_note_id(self, note_id):
        return self.__session.query(Note).filter(
            Note.note_id == note_id).first()

    def delete_note(self, note):
        self.__session.delete(note)

class User(db.Model):
    """docstring for User"""

    __tablename__ = "User"
    username = db.Column(db.String(30), nullable=False, primary_key=True)
    email = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    name = db.Column(db.String(30), nullable=False)
    lastname = db.Column(db.String(30), nullable=False)
    phone = db.Column(db.String(12), nullable=False)
    # db.relationship must      be in the parent table
    activity = db.relationship(
        'Activity', backref='User', cascade="all, delete-orphan")

    def __repr__(self):
        return '{},{},{},{},{}'.format(self.username,
                                       self.password, self.email,
                                       self.name, self.lastname)


class Activity(db.Model):
    """docstring for Activity"""

    __tablename__ = "Activity"
    activity_id = db.Column(db.Integer, nullable=True, primary_key=True)
    description = db.Column(db.String(300), nullable=False)
    title = db.Column(db.String(30), nullable=False)
    priority = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(30), db.ForeignKey(
        'User.username'), nullable=False)
    # db.relationship must      be in the parent table
    note = db.relationship('Note', backref='Activity',
                           cascade="all, delete-orphan")
    schedule = db.relationship(
        'Schedule', backref='Activity', cascade="all, delete-orphan")

    def __repr__(self):
        return ('{}, {}, {}'.format(self.title, self.location, self.username))


class Note(db.Model):
    """docstring for Note"""

    __tablename__ = "Note"
    note_id = db.Column(db.Integer, nullable=False, primary_key=True)
    content = db.Column(db.String(25), nullable=False)
    priority = db.Column(db.String(30), nullable=False, )
    due_date = db.Column(db.DateTime, nullable=True)
    creation_date = db.Column(db.DateTime, nullable=False)
    username = db.Column(db.String(30), db.ForeignKey(
        'User.username'), nullable=False)
    activity_id = db.Column(db.Integer, db.ForeignKey(
        'Activity.activity_id'), nullable=False)


class Schedule(db.Model):
    """docstring for Schedule"""

    __tablename__ = "Schedule"
    schedule_id = db.Column(db.Integer, nullable=False, primary_key=True)
    monday = db.Column(db.String(25), nullable=True)
    tuesday = db.Column(db.String(25), nullable=True)
    wednesday = db.Column(db.String(25), nullable=True)
    thursday = db.Column(db.String(25), nullable=True)
    friday = db.Column(db.String(25), nullable=True)
    activity_id = db.Column(db.Integer, db.ForeignKey(
        'Activity.activity_id'), nullable=False)

    def __repr__(self):
        return '{}, {}, {}, {}, {}|'.format(
            self.monday,
            self.tuesday,
            self.wednesday,
            self.thursday,
            self.friday
            )
