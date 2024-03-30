#! /usr/bin/env python3
"""This is the module for support functions for interacting
with the database
"""
from models import storage
from models.alert import Alert
from models.company import Company
from models.contact import Contact
from models.hosp_operator import Hospital
from models.incident import Incident
from models.location import Address
from models.system_user import InternalUser, Patient, Person, Staff
from models.user import User
from models.utils.support import data_ok


def auth_user(email, pwd):
    """This function logs in a user"""
    # check data type
    if not isinstance(email, str):
        return 0
    user = storage.get_one_by(User, user_name=email)
    if user is None:
        return 1
    if not user.is_valid_password(pwd):
        return 2
    return (user)

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


class CreateCompany:
    """This class creates companies
    """
    def __init__(self):
        self.companies = []

    def create(self,cls_comp, category, data):
        """
        This function creates companies
        cls_comp: the class to create
        category: the category of the company
        data: a dictionary with the following keys
        return: a dictionary with the company id
        """
        data = CreateUser.data_ok(cls_comp, data)
        if not data:
            return None
        co_data = {}
        
        for field in cls_comp.fields_errMSG.keys():
            if field in data:
                co_data[field] = data[field]
       
        # create Contact
        user = CreateUser()
        contact = user.create_contact(co_data)

        if not contact:
            return None

        address = storage.get_one_by(Address,
                                    street=co_data['street'],
                                    city=co_data['city'],
                                    state=co_data['state'],
                                    zipcode=co_data['zipcode'],
                                    country=co_data['country'])
        if not address:
            return None

        company = storage.get_one_by(Company,
                                     address_id=address.id,
                                     name=co_data['name'])
        if not company:

            company = Company(name=co_data['name'],
                              address_id=address.id,
                              status=co_data['status'])
            if company:
                company.save()

        if category == "hospital":
            hosp = storage.get_one_by(Hospital,
                                      company_id=company.id)
            if hosp:
                return hosp.to_dict()
            
            hosp = cls_comp(
            company_id=company.id,
            latitude=co_data['lat'],
            longitude=co_data['lng'])
            if hosp:
                hosp.save()
                return hosp.to_dict()
            return None
        elif category == "ambulance":
            ambu = storage.get_one_by(cls_comp,
                                      company_id=company.id)
            if ambu:
                return ambu.to_dict()
            
            ambu = cls_comp(company_id=company.id)
            if ambu:
                ambu.save()
                return ambu.to_dict()
            return None
        return None

class CreateUser:
    """
    This class creates users
    1. create Person: first_name,last_name,gender,phone_number,email
    2. create User: user_name, password
    """
    
    def __init__(self):
        pass

    @classmethod
    def data_ok(cls, actual_cls, data):
        """
        This method checks the data type and returns a dictionary
        data: dictionary of the data
        """
        if not isinstance(data, dict) or not data or len(data) == 0:
            print(f"Data is not a dictionary {data}")
            return None
        # check if the data is complete
        fields_flag = True
        # for field in data.keys():
        print(actual_cls.fields_errMSG.keys(), "====>")
        for field in actual_cls.fields_errMSG.keys():
            if field not in data.keys():
                print(f"Field [[{field}]] is not in {data.keys()}")
                fields_flag = False
        if not fields_flag:
            print(actual_cls.fields_errMSG.keys(), "====>")
            print(f"Field(s) for {actual_cls.__name__} not in {data.keys()}")
            return None
        return data

    def create_address(self, data, data_flag=False):
        """
        This method creates an address
        data: dictionary of the address
        data_flag: boolean to check if the data is ok

        returns: address id
        """
        if data_flag:
            data = CreateUser.data_ok(Address, data)
        if not data:
           return None
        # create address
        address_data = {}
        for field in Address.fields_errMSG.keys():
            if field in data:
                address_data[field] = data[field]

        if len(data) <= 0:
            return None

        address = storage.get_one_by(Address,
                                     street=address_data['street'],
                                     city=address_data['city'],
                                     state=address_data['state'],
                                     zipcode=address_data['zipcode'],
                                     country=address_data['country'])
        
        
        if address:
            return address.to_dict()               
        address = Address(street=address_data['street'],
                          city=address_data['city'],
                          state=address_data['state'],
                          zipcode=address_data['zipcode'],
                          country=address_data['country'])
        if address:
            address.save()
            return address.to_dict()
        return None

    def create_contact(self, data, data_flag=False):
        """
        This method creates a contact
        data: dictionary of the contact
        """
        if data_flag:
            data = CreateUser.data_ok(Contact, data)
        if not data:
            return None
        
        contact_data = {}
        for field in Contact.fields_errMSG.keys():
            if field in data:
                contact_data[field] = data[field]

        if len(contact_data) <= 0:
            return None
        contact = storage.get_one_by(Contact,
                                    email=contact_data['email'],
                                    phone_number=contact_data['phone'])
        if contact:
            return contact.to_dict()
 
        address = self.create_address(contact_data)

        if not address:
            return None
        contact = Contact(email=contact_data['email'],
                          phone_number=contact_data['phone'],
                          address_id=address.get('id'))
        if contact:
            contact.save()
            return contact.to_dict()
        return None

    def create_person(self, data, data_flag=False):
        """
        This method creates a person before a user is created
        data: dictionary of the person
        data_flag: boolean to check if the data is ok
        """
        if data_flag:
            data = data if CreateUser.data_ok(Person, data) else None
        if not data:
            return None
        person_data = {}
        for field in Person.fields_errMSG.keys():
            if field in data:
                person_data[field] = data[field]

        contact = self.create_contact(person_data)
        if not contact:
            return None
        person = storage.get_one_by(Person,
                                    first_name=person_data['fname'],
                                    last_name=person_data['lname'],
                                    gender=person_data['gender'],
                                    contact_id=contact.get('id'))
        if person:
            return person.to_dict()
        contact = self.create_contact(person_data)
        # create person
        person = Person(first_name=person_data['fname'],
                        last_name=person_data['lname'],
                        gender=person_data['gender'],
                        contact_id=contact.get('id'))
        if person:
            person.save()
            return person.to_dict()
        return None
    
    def create_internal_user(self, data):
        """
        This method creates an internal user
        data: dictionary of the internal user
        """
        data = data if CreateUser.data_ok(InternalUser, data) else None
        if data == None:
            return None
        
        user_data = {}
        for field in InternalUser.fields_errMSG.keys():
            if field in data:
                user_data[field] = data[field]
        
        # person
        person = self.create_person(user_data)
        if person == None:
            return None
        
        # check if user exists
        int_user = storage.get_one_by(InternalUser, person_id=person.get('id'))
        if int_user:
            return int_user.to_dict()
        # create internal user
        int_user = InternalUser(person_id=person.get('id'))
        if int_user:
            int_user.save()
            return (int_user.to_dict())
        return None
    
    def creat_staff(self, data):
        """
        This method creates a staff
        cls_comp: the class to create
        category: the category of the company
        data: dictionary of the staff
        """

        data = data if data_ok(Staff, data) else None
        if data == None:
            return None
        staff_data = {}
        
        for field in Staff.fields_errMSG.keys():
            if field in data:
                staff_data[field] = data[field]
        print("=========================Staff --- data====================================")
        print(staff_data)
        print(f"========================={'company_id' in staff_data} == {staff_data.get('company_id')}====================================")
        staff = storage.get_one_by(Staff,
                                   staff_number=staff_data['staff_number'],
                                   company_id=staff_data.get('company_id'))
        if staff:
            return staff.to_dict()

        # create internal user
        int_user = self.create_internal_user(staff_data)
        if not int_user:
            return None
        staff = Staff(staff_number=staff_data['staff_number'],
                      internal_user_id=int_user.get('id'),
                      status=staff_data['status'],
                      company_id=staff_data.get('company_id'))
        if staff:
            staff.save()
            return staff.to_dict()
        return None

    def create_user(self, data):
        """
        This method creates a user
        data: dictionary of the user
        """
        # create person
        data = data if data_ok(User, data) else None
        if data == None:
            return None
        # print("=========================1. Before User --- data====================================")
        # print(data)
        user_data = {}
        userFields = User.fields_errMSG
        userFields.update(**Staff.fields_errMSG)
        for field in userFields.keys():
            if field in data:
                user_data[field] = data[field]

        # check if user exists
        user = storage.get_one_by(User, user_name=user_data['user_name'])
        if user:
            return user.to_dict()
        # print("=========================2. User --- data====================================")
        # print(user_data)
        # create staff
        staff = self.creat_staff(user_data)
        
        if not staff:
            return None
        # create user
        user = User(user_name=user_data['email'],
                    user_type=user_data['user_type'],
                    staff_id=staff.get('id'))
        if user:
            user.generate_salt()
            user.set_password(user_data['password'])
            user.save()
            return user.to_dict()
        return None
    

class CreateExternalUser(CreateUser):
    """
    This class creates external users
    1. create Person: first_name,last
    """
    def __init__(self):
        super().__init__()
        pass

    def create_patient(self, data):
        """
        This method creates a patient
        data: dictionary of the patient
        """
        data = CreateUser.data_ok(Patient, data)
        
        
        if data == None:
            return None
        
        pat_data = {}
        for field in Patient.fields_errMSG.keys():
            if field in data:
                pat_data[field] = data[field]
        # create person
        person = self.create_person(pat_data)
        if person == None:
            return None
        # create incident
        incident = storage.get_one_by(Incident,
                                      incident_type=pat_data['incident_type'],
                                      latitude=pat_data['lat'],
                                      longitude=pat_data['lng'])
        if incident:
            return None
        # create Incident
        incident = Incident(incident_type=pat_data['incident_type'],
                            latitude=pat_data['lat'],
                            longitude=pat_data['lng'],
                            incident_description=pat_data['incident_description'],
                            incident_status=pat_data['status'])
        if not incident:
            return None
        incident.save()
        alert = self.create_alert(incident.id, pat_data)
        if not alert:
            return None
        # create patient
        patient = Patient(person_id=person.get('id'),
                          incident_id=incident.id,
                          relative_phone=pat_data['relative_phone'])
        if patient:
            patient.save()
            # Add patient to incidents
            return patient.to_dict()
        return None

    def create_alert(self, incident_id, data):
        """
        This method creates an alert
        """
        data = CreateUser.data_ok(Alert, data)
        if data == None:
            return None
        alert_data = {}
        for field in Alert.fields_errMSG.keys():
            if field in data:
                alert_data[field] = data[field]
        alert = storage.get_one_by(Alert, incident_id=incident_id)
        if alert:
            return alert.to_dict()
        # create alert
        alert = Alert(alert_type=alert_data['alert_type'],
                      alert_status=alert_data['alert_status'],
                      incident_id=incident_id)
        if alert:
            alert.save()
            return alert.to_dict()
        return None