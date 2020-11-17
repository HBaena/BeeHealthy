from settings import db
from model import Model, InfoCodes


class Controller:
    """docstring for Controller"""

    def __init__(self):
        self.model = Model(session=db.session)

    def __del__(self):
        self.model.close_session()

# ------------------------------------------------------------------------------------------------- #
#                                        db moethods                                                #
# ------------------------------------------------------------------------------------------------- #

    def undo(self):
        self.model.undo_changes()

    def save(self):
        self.model.save_changes()

# ------------------------------------------------------------------------------------------------- #
#                                        Contacts                                                   #
# ------------------------------------------------------------------------------------------------- #
    def request_contact(self, name, phone, email, question):
        self.model.create_contact(name, phone, email, question)

    def get_contacts(self):
        return self.model.read_contacts()

    def remove_contact(self, contact_id):
        self.model.delete_contact(self.model.read_contact(contact_id))
        return InfoCodes.SUCCESS

# ------------------------------------------------------------------------------------------------- #
#                                             User                                                  #
# ------------------------------------------------------------------------------------------------- #


    def add_user(self, username, email, password, name, lastname, phone, speciality, workplace, doctor):
        # if self.model.read_user(username=username) or \
        #         self.model.read_user(email=email):
        if self.model.read_user(username=username) or \
                self.model.read_user(email=email):
            return InfoCodes.USER_ALREADY_EXIST
        self.model.create_user(username, email, password, name, lastname, phone, speciality, workplace, doctor)
        return InfoCodes.SUCCESS
    def get_user(self, username):
        return self.model.read_user(username)

    def get_username(self, email):
        return self.model.read_user(email)


    def get_all_users(self):
        return self.model.read_users()

    def remove_user(self, username):
        response = self.model.read_user(username)
        if response == InfoCodes.USERNAME_NOT_FOUND:
            return response
        self.model.delete_user(response)
        return InfoCodes.SUCCESS

    def login(self, token, password):
        return self.model.verify_user(token, password)
