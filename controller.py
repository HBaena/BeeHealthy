from settings import db
from model import Model, InfoCodes, User, Patient, Appointment


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
#                                        Appoiments                                                  #
# ------------------------------------------------------------------------------------------------- #
    def add_appoiment(self, id_doctor, id_patient, date, description):
        self.model.create_appoiment(id_doctor, id_patient, date, description, weight=0, height=0, temperature=0, heart_rate=0, done=False)
        return InfoCodes.SUCCESS

    def get_appoiments(self, id_patient=None):
        if id_patient:
            return filter(lambda x: x.id_patient == id_patient, self.get_appoiments())
        else:
            return self.model.read__all_appoiments()

    def get_appoiments_checked(self, id_patient=None):
        if id_patient:
            return filter(lambda x: x.done == True and x.id_patient == id_patient, self.get_appoiments())
        else:
            return filter(lambda x: x.done == True, self.get_appoiments())

    def get_appoiments_unchecked(self, id_patient=None):
        if id_patient:
            return filter(lambda x: x.done == False and x.id_patient == id_patient, self.get_appoiments())
        else:
            return filter(lambda x: x.done == False, self.get_appoiments())

    def get_appoiment(self, appoiment_id):
        return self.model.read_appoiment(Appointment.id_appointment == appoiment_id)

    def remove_appoiment(self, appoiment_id):
        self.model.delete_contact(self.get_appoiment(appoiment_id))
        return InfoCodes.SUCCESS

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
#                                        Contacts                                                   #
# ------------------------------------------------------------------------------------------------- #
    def add_patient(self, id_patient, name, lastname, phone, email, gender, weight=-1, height=-1, temperature=-1, heart_rate=-1):
        if self.get_patient(email):
            return InfoCodes.ERROR

        self.model.create_patient(
            id_patient=id_patient, name=name, 
            lastname=lastname, phone=phone, 
            email=email, gender=gender, 
            weight=weight, height=height, 
            temperature=temperature, 
            heart_rate=heart_rate)

        return InfoCodes.SUCCESS

    def get_patient(self, id_patient):
        response = self.model.read_patient(Patient.id_patient == id_patient)
        # print(id_patient)
        if not response:
            return InfoCodes.ERROR
        else:
            return response

    def get_patients(self):
        return self.model.read_patients()

    def remove_patient(self, id_patient):
        response = self.get_patient(id_patient)
        if not response:
            return InfoCodes.ERROR
        self.model.delete_patient(response)        
        return InfoCodes.SUCCESS

# ------------------------------------------------------------------------------------------------- #
#                                             User                                                  #
# ------------------------------------------------------------------------------------------------- #


    def add_user(self, username, email, password, name, lastname, phone, speciality='Secretary', workplace='Seception', doctor=False):
        if self.model.read_user((User.username == username)) or \
                self.model.read_user((User.email == email)):
            return InfoCodes.USER_ALREADY_EXIST
        self.model.create_user(username, email, password, name, lastname, phone, speciality, workplace, doctor)
        return InfoCodes.SUCCESS

    def get_user(self, username):
        return self.model.read_user((User.username == username) | (User.email == username))

    def get_username(self, email):
        # print(User.email == email)
        response = self.model.read_user(User.email == email)
        if not response:
            return email
        return response.username

    def get_all_users(self):
        return self.model.read_users()

    def remove_user(self, username):
        response = self.model.read_user((User.username == username) | (User.email == username))
        if response == InfoCodes.USERNAME_NOT_FOUND:
            return response
        self.model.delete_user(response)
        return InfoCodes.SUCCESS

    def login(self, token, password):
        return self.model.verify_user(token, password)

    def get_doctors(self):
        return self.model.read_users(User.doctor == True)
    
    def get_roots(self):
        return self.model.read_users(User.doctor == False)
