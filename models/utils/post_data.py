#! /usr/bin/env python3
"""This is the post data module
"""
from models import storage
from datetime import datetime
from models.company import Company
from models.ambulance import Ambulance
from models.location import Address
from models.contact import Contact
from models.system_user import InternalUser, Person, Staff
from models.user import User
from models.hosp_operator import Hospital
from models.incident import Incident
from models.alert import Alert
from models.review import Review
from models.service import Service
from models.ambu_operator import AmbulanceOwner
from models.utils.create_table import CreateCompany
from models.utils.retrieve_data import get_company, get_company_address
from models.utils.support import data_ok

def post(cls, data, validator=None, create=True):
    """This function posts an object"""
    data = data_ok(cls, data)
    obj = storage.get_one_by(cls,  **validator)
    if obj:
        return obj.to_dict()
    if not create:
        return {"error": f"{cls.__class__} not found"}
    obj = cls(**data)
    if not obj:
        return {"error": f"{cls.__class__} not created"}
    obj.save()
    return obj.to_dict()

# ----------------- Company -----------------

def post_company(data):
    """This function posts a company"""
    comp = post(Company, data, {'name': data['name']}, create=False)
    if 'error' not in comp:
        # confirm company by address and contact
        add_contact = {}
        address = post(Address, data, {'street': data['street'],
                                    'city': data['city'],
                                    'state': data['state'],
                                    'zipcode': data['zipcode'],
                                    'country': data['country']},
                                    create=False)
        if 'error' in address:
            add_contact['address'] = address.get('error')
        if address:
            contact = post(Contact, data, {'email': data['email'],
                                        'phone_number': data['phone']},
                                        create=False)
            if 'error' in contact:
                add_contact['contact'] = contact.get('error')
        
        if len(add_contact) < 0:
            # Found company
            return comp
        
    address = post(Address, data, {'street': data['street'],
                                   'city': data['city'],
                                   'state': data['state'],
                                   'zipcode': data['zipcode'],
                                   'country': data['country']})
    print("===================")
    print(address)
    if 'error' in address:
        return address
    data['address_id'] = address.get('id')
    contact = post(Contact, data, {'email': data['email'],
                                   'phone_number': data['phone'],
                                   'address_id': address.get('id')})
    if 'error' in contact:
        return contact
    return post(Company, data, {'address_id': address.get('id')})

# ----------------- CONTACT -----------------
def post_contact(data):
    """This function posts a contact"""

    contact = post(Contact, data, {'email': data['email'],
                               'phone_number': data['phone'],
                               'address_id': data['address_id']})
    if 'error' in contact:
        return contact
    return contact

# ----------------- HOSPITAL -----------------
def post_hospital(data):
    """This function posts a hospital"""
    hosp = CreateCompany().create(Hospital, 'hospital', data)
    return hosp



# ----------------- USER -----------------
def post_person(data):
    """This function posts a person"""
    contact = post_contact(data)
    if 'error' in contact:
        return contact

    person = post(Person, data, {'first_name': data['first_name'],
                                'last_name': data['last_name'],
                                'gender': data['gender'],
                                'contact_id': contact.get('id')})
    if 'error' in person:
        return person
    return person

def post_internal_user(data):
    """This function posts an internal user"""
    person = post_person(data)
    if 'error' in person:
        return person
    data['person_id'] = person.get('id')
    
    internal_user = post(InternalUser, data, {'person_id': data['person_id']})
    return internal_user

def post_staff(data):
    """This function posts a staff"""
    internal_user = post_internal_user(data)
    if 'error' in internal_user:
        return internal_user
    data['internal_user_id'] = internal_user.get('id')
    company = get_company(data['company_id'])
    if 'error' in company:
        return company
    data['company_id'] = company.get('id')
    staff = post(Staff, data, {'staff_number': data['staff_number'],
                            'company_id': data['company_id']})
    return staff

def post_user(data):
    """This function posts a user
    staff:
        internal_user_id:
            person_id:
                contact_id:
        company_id
    """
    staff = post_staff(data)
    if 'error' in staff:
        return staff
    data['staff_id'] = staff.get('id')
    user = post(User, data, {'staff_id': data['staff_id'],
                          'user_name': data['user_name']})
    return user

# ----------------- PATIENT -----------------
def post_patient(data):
    """This function posts a patient"""
    patient = post(Person, data, {'first_name': data['first_name'],
                                  'last_name': data['last_name'],
                                  'email': data['email'],
                                  'phone_number': data['phone_number']})
    return patient