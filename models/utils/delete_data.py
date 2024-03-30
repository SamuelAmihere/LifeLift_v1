#! /usr/bin/env python3
"""This is the delete data module
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
from models.utils.retrieve_data import get, get_company, get_company_address, get_company_contact
from models.utils.support import data_ok


def delete_obj(cls, obj_id= None):
    """This function deletes an object"""
    if type(obj_id) != str:
        return {"error": "id must be a string"}
    if obj_id:
        obj = storage.get_one_by(cls, id=obj_id)
        if not obj:
            return {"error": f"{cls.__class__} not found"}
        obj.delete()
        storage.save()
    else:
        objs = storage.all(cls).values()
        if not objs:
            return {"error": f"{cls.__class__} not found"}
        for obj in objs:
            obj.delete()
        storage.save()
    return {}

# ----------------- Company -----------------
def delete_company(company_id):
    """This function deletes a company"""
    staff = get(Staff)
    if 'error' in staff:
        return staff
    for person in staff:
        if person.get('company_id') == company_id:

            # Delete InternalUser
            internaluser = get(InternalUser, person.get('internal_user_id'))
            personid = internaluser.get('person_id')
            # delete user
            delete_obj(User, person.get('id'))
            # delete staff
            delete_obj(Staff, person.get('id'))
            # delete internal user
            delete_obj(InternalUser, person.get('internal_user_id'))
            # delete person
            delete_obj(Person, personid)
    return delete_obj(Company, company_id)

def delete_company_address(company_id):
    """This function deletes a company address"""
    company = get_company(company_id)
    if 'error' in company:
        return company
    address = get_company_address(company.get('address_id'))
    if 'error' in address:
        return address
    return delete_obj(Address, address.get('id'))

def delete_company_contact(company_id=None, contact_id= None):
    """This function deletes a company contact"""
    company = get_company(company_id)
    if 'error' in company:
        return company
    contact = get_company_contact(company.get('address_id'))
    if 'error' in contact:
        return contact
    return delete_obj(Contact, id= contact.get('id'))

# ----------------- Hospital -----------------
# TODO: delete hospital address

# ----------------- User -----------------
def delete_user(user_id):
    """This function deletes a user"""
    return delete_obj(User, user_id)

# ----------------- Patient -----------------
def delete_patient(patient_id):
    """This function deletes a patient"""
    return delete_obj(Person, patient_id)

# ----------------- Incident -----------------
def delete_incident(incident_id):
    """This function deletes an incident"""
    return delete_obj(Incident, incident_id)