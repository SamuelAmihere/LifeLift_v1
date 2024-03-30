#! /usr/bin/env python3
"""This is the update data module
"""
from models import storage
from datetime import datetime
from models.company import Company
from models.ambulance import Ambulance
from models.location import Address
from models.contact import Contact
from models.system_user import Patient, Staff
from models.user import User
from models.hosp_operator import Hospital
from models.incident import Incident
from models.alert import Alert
from models.review import Review
from models.service import Service
from models.ambu_operator import AmbulanceOwner
from models.utils.retrieve_data import get_company, get_company_address, get_hospital
from models.utils.support import data_ok

def update(bals_cls, cls, data, obj_id):
    """This function updates an object"""
    data = data_ok(bals_cls, data)
    if type(obj_id) != str:
        return {"error": "id must be a string"}
    obj = storage.get_one_by(cls, id=obj_id)
    if not obj:
        return {"error": f"{cls.__class__} not found"}
    for key, value in data.items():
        if key in cls.fields_errMSG.keys():
            setattr(obj, key, value)
    obj.updated_at = datetime.utcnow()
    obj.save()
    return obj.to_dict()

# ----------------- Company -----------------
def modify_comp(data, company_id):
    """This function updates a company"""
    return update(Company, Company, data, company_id)

def modify_company_address(data, company_id):
    """This function updates a company address"""
    company = get_company(company_id)
    if 'error' in company:
        return company
    address = get_company_address(company.get('address_id'))
    if 'error' in address:
        return address
    company_add = update(Company, Address, data, address.get('id'))
    return company_add

def modify_company_contact(data, company_id):
    """This function updates a company contact"""
    company = get_company(company_id)
    if 'error' in company:
        return company
    address = get_company_address(company.get('address_id'))
    if 'error' in address:
        return address
    contact = update(Company, Contact, data, address.get('contact_id'))
    return contact

def modify_company_staff(data, company_id):
    """This function updates a company staff"""
    company = get_company(company_id)
    if 'error' in company:
        return company
    staff = update(Company, Staff, data, company.get('staff_id'))
    return staff

# ----------------- Hospital -----------------
def modify_hospital(data, hospital_id):
    """This function updates a hospital"""
    return update(Hospital, Hospital, data, hospital_id)

def modify_hospital_address(data, hospital_id):
    """This function updates a hospital address"""
    hospital = get_hospital(hospital_id)
    if 'error' in hospital:
        return hospital
    company = get_company(hospital.get('company_id'))
    address = modify_company_address(data, company.get('id'))
    if 'error' in address:
        return address
    return address

def modify_hospital_contact(data, hospital_id):
    """This function updates a hospital contact"""
    hospital = get_hospital(hospital_id)
    if 'error' in hospital:
        return hospital
    company = get_company(hospital.get('company_id'))
    contact = modify_company_contact(data, company.get('id'))
    if 'error' in contact:
        return contact
    return contact

# ----------------- User -----------------
def modify_user(data, user_id):
    """This function updates a user"""
    return update(User, User, data, user_id)


# ----------------- Patient -----------------
def modify_patient(data, patient_id):
    """This function updates a patient"""
    return update(Patient, Patient, data, patient_id)


# ----------------- Incident -----------------
def modify_incident(data, incident_id):
    """This function updates an incident"""
    return update(Incident, Incident, data, incident_id)