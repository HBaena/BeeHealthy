from settings import db
from model import Model, InfoCodes


class Controller:
    """docstring for Controller"""

    def __init__(self):
        self.model = Model(session=db.session)

    def __del__(self):
        self.model.close_session()

    def undo(self):
        self.model.undo_changes()

    def save(self):
        self.model.save_changes()

    def login(self, token, password):
        return self.model.verify_user(token, password)

    def add_user(self, username, email, password, name, lastname, phone):
        if self.model.read_user(username=username) or \
                self.model.read_user(email=email):
            return InfoCodes.USER_ALREADY_EXIST
        self.model.create_user(username, email, password,
                               name, lastname, phone)
        return InfoCodes.SUCCESS
    def get_user(self, username):
        return self.model.read_user(username=username)

    def get_username(self, email):
        return self.model.read_user(email=email).username

    def get_all_users(self):
        return self.model.read_users()

    def get_activity_name(self, activity_id):
        response =  self.model.read_activity(activity_id=activity_id)
        if response:
            return response.title
        else:
            return InfoCodes.ERROR


    def get_activity_id(self, title):
        response = self.model.read_activity(title=title)
        if response:
            return response.activity_id
        else:
            return InfoCodes.ERROR

    def add_activity(self, username, description, priority, location, title):
        activity = self.model.read_activity(title=title)
        if activity:
            return InfoCodes.ACTIVITY_ALREADY_EXIST
        self.model.create_acitivity(title, description,
                                    priority, location, username)
        return self.get_activity_id(title)

    def get_schedule(self, activity_id):
        schedule =self.model.read_schedule(activity_id)
        if schedule:
            return schedule
        else:
            return InfoCodes.ERROR            

    def add_schedule(self, monday, tuesday, wednesday, thursday,
                     friday, activity_id):
        self.model.create_schedule(monday, tuesday, wednesday,
                                   thursday, friday, activity_id)


    def get_activities(self, username):
        activities = self.model.read_activities(username)
        if activities:
            return activities
        else:
            return InfoCodes.ERROR

    def remove_user(self, username):
        response = self.model.read_user(username)
        if response == InfoCodes.USERNAME_NOT_FOUND:
            return response
        self.model.delete_user(response)
        return InfoCodes.SUCCESS

    def remove_activity(self, title):
        response = self.model.read_activity(title=title)
        if response == InfoCodes.ERROR:
            return response
        self.model.delete_activity(response)
        return InfoCodes.SUCCESS

    def add_note(self, content, priority, due_date,
                 creation_date, username,
                 activity_id,):
        self.model.create_note(content, priority, due_date,
                               creation_date, username, activity_id)
        return InfoCodes.SUCCESS

    def get_notes(self, username=None, title=None):
        if username:
            return self.model.read_notes(username=username)
        elif title:
            activity_id = self.model.read_activity(title=title).activity_id
            return self.model.read_notes(activity_id=activity_id)

    def remove_note(self, note_id):
        note = self.model.read_note_id(note_id)
        if note:
            self.model.delete_note(note)
            return InfoCodes.SUCCESS
        else:
            return InfoCodes.ERROR
