#! /usr/bin/env python3
"""This is the module for support functions for interacting
with the database
"""
from datetime import datetime
from models import storage
from models import storage_type
from models.alert import Alert
from models.incident import Incident
from models.location import Address
from models.system_user import InternalUser, Patient, Person
from models.user import User


def login_user(email, pwd):
    """This function logs in a user"""
    # check data type
    if not isinstance(email, str):
        return 0
    user = storage.get_one_by(User, user_name=email)
    if user is None:
        return 1
    if not user.is_valid_password(pwd):
        return 2
    return (user.to_dict())

def check_by_email(email):
    """This function checks if a user exists by email"""
    # check data type
    if not isinstance(email, str):
        return 0
    user = storage.get_one_by(User, user_name=email)
    if user:
        return user.to_dict()
    return None

def check_address(data):
    """This function checks if an address exists"""
    # check data type
    if not isinstance(data, dict):
        return 0
    street = data.get('street')
    city = data.get('city')
    state = data.get('state')
    zipcode = data.get('zipcode')
    country = data.get('country')
    address = storage.get_one_by(Address, street=street, city=city,
                                 state=state, zipcode=zipcode, country=country)
    if address:
        return address.to_dict()
    return None


class CreateUser:
    """
    This class creates users
    1. create Person: first_name,last_name,gender,phone_number,email
    2. create User: user_name, password
    """
    required_fields = {'Person': ['fname', 'lname', 'gender', 'phone',
                                  'email'],
                       'User': ['user_name', 'password', 'userType']
                       }
    
    def __init__(self, data):
        self.data = data if self.data_ok(data) else None
        self.user = None
        self.person = None
        self.internal_user = None

    def data_ok(self, data):
        """
        This method checks the data type and returns a dictionary
        """
        if not isinstance(data, dict) or not data or data is None or len(data) == 0:
            return None
        # check if the data is complete
        for key, val  in CreateUser.required_fields.items():
            for field in val:
                if field in data.keys() == False:
                    return None
        return data

    def create_person(self):
        """
        This method creates a person before a user is created
        """
        if self.data is None:
            return None

        first_name = self.data.get(CreateUser.required_fields['Person'][0])
        last_name = self.data.get(CreateUser.required_fields['Person'][1])
        gender = self.data.get(CreateUser.required_fields['Person'][2])
        phone_number = self.data.get(CreateUser.required_fields['Person'][3])
        email = self.data.get(CreateUser.required_fields['Person'][4])

        person = check_by_email(email)

        if person == 0:
            # invalid data type
            return None
        elif  person:
            # Exists
            return person
        else:
            # create person
            self.person = Person(first_name=first_name, last_name=last_name,
                                gender=gender, phone_number=phone_number,
                                    email=email)
            self.person.save()
            return self.person.to_dict()
            
    
    def create_user(self):
        """
        This method creates a user
        """
        # create person
        person = self.create_person().id

        if isinstance(person, str):
            return person
        # create user
        user_name = self.data[CreateUser.required_fields['Person'][4]]
        user_type = self.data[CreateUser.required_fields['User'][-1]]
        pwd = self.data[CreateUser.required_fields['User'][1]]

        user = User(user_name=user_name, user_type=user_type)
        if user:
            user.generate_salt()
            user.set_password(pwd)
            user.save()
            return (user.to_dict())
        return None
    

class CreateExternalUser(CreateUser):
    """
    This class creates external users
    1. create Person: first_name,last
    """
    required_fields_pat = {'Person': CreateUser.required_fields['Person'],
                        'Address': ['street', 'city', 'state', 'zipcode',
                                    'country'],
                        'Patient': ['relative_phone']
                        }

    def __init__(self, data):
        super().__init__(data)
        self.user = None
        self.person = None
        self.address = None

    
    def create_address(self):
        """
        This method creates an address
        """

        add = check_address(self.data)
        if isinstance(add, str):
            return add
    
        # create address
        self.address = Address(street=self.data['street'],
                          city=self.data['city'],
                          state=self.data['state'],
                          zipcode=self.data['zipcode'],
                          country=self.data['country'])
        if self.address:
            self.address.save()
            return self.address.to_dict()
        return None
    
    def create_patient(self):
        """
        This method creates a patient
        """
        address = self.create_address()
        if isinstance(address, str) == False:
            return None
         # create person
        person = self.create_person()
        if isinstance(person, str) == False:
            return None
        
        # create patient
        self.user = Patient(person_id=self.person.id,
                          address_id=self.address.id,
                          relative_phone=self.data['relative_phone'])
        if self.user:
            self.user.save()
            return self.user.to_dict()
        return None

    def create_alert(self):
        """
        This method creates an alert
        """
        # create patient
        patient = self.create_patient()
        if isinstance(patient, str) == False:
            return None
        # create alert
        alert = Alert(patient_id=patient.id, alert_type="Emergency",
                      alert_status="Pending")
        if alert:
            alert.save()
            return alert.to_dict()
        return None