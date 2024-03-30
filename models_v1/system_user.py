#!/usr/bin/python3
"""This is the user class"""
import models
from models.ambulance import Ambulance
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Enum, String
from sqlalchemy import ForeignKey
from sqlalchemy import Column, String
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from models import storage_type
from models.company import Company
from models.contact import Contact
from models.incident import Incident


class Person(BaseModel, Base):
    """This is the class for Person
    """
    fields_errMSG = {
        'fname': 'Missing first name',
        'lname': 'Missing last name',
        'gender': 'Missing',
        # to create contact
        **Contact.fields_errMSG,
    }

    if storage_type == "db":
        __tablename__ = "persons"
        first_name = Column(String(128), nullable=False)
        last_name = Column(String(128), nullable=False)
        gender = Column(String(128), nullable=False)
        contact_id = Column(String(60), ForeignKey('contacts.id'), nullable=False)
    else:
        first_name = ""
        last_name = ""
        gender = ""
        contact_id = ""


class Patient(BaseModel, Base):
    """This is the Patient class"""
    fields_errMSG = {
        'relative_phone': 'Missing relative phone',
        # to create person
        **Person.fields_errMSG,
        # to create incident
        **Incident.fields_errMSG,
    }
    if storage_type == "db":
        __tablename__ = 'patients'
        person_id = Column(String(60), ForeignKey('persons.id'), nullable=False)
        relative_phone = Column(String(20), nullable=True)
        incident_id = Column(String(60), ForeignKey('incidents.id'),
                             nullable=True)
    else:
        person_id = ""
        relative_phone = ""
        incident_id = ""


class InternalUser(BaseModel, Base):
    """This is the class for the internal user
    """
    fields_errMSG = {
        # to create person
        **Person.fields_errMSG,
    }

    if storage_type == "db":
        __tablename__ = "internal_users"
        person_id = Column(String(60), ForeignKey('persons.id'), nullable=False)
    else:
        person_id = ""


class Staff(BaseModel, Base):
    """This is the class defining a staff
    """
    fields_errMSG = {
        'staff_number': 'Missing staff number',
        'status': 'Missing status',
        # to create internal user
        **InternalUser.fields_errMSG,
        # to create company
        **Company.fields_errMSG,
    }
    if storage_type == "db":
        __tablename__ = "staff"
        internal_user_id = Column(String(60), ForeignKey('internal_users.id'),
                                  nullable=False)
        staff_number = Column(String(128), nullable=False)
        status = Column(Enum("Active", "Inactive"), default="Active")
        company_id = Column(String(60), ForeignKey('companies.id'), nullable=False)
        company = relationship("Company", back_populates="staff")
    else:
        internal_user_id = ""
        staff_number = ""
        status = ""

class AmbulanceStaff(BaseModel, Base):
    """This is the class for the ambulance staff
    """
    fields_errMSG = {**Staff.fields_errMSG,
                     **Ambulance.fields_errMSG

    }
    if storage_type == "db":
        __tablename__ = "ambulance_staff"
        staff_id = Column(String(60), ForeignKey('staff.id'), nullable=False)
        ambulance_id = Column(String(60), ForeignKey('ambulances.id'),
                              nullable=False)
        ambulance = relationship("Ambulance", back_populates="ambulance_staff")
    else:
        staff_id = ""
        ambulance_id = ""

class Driver(BaseModel, Base):
    """This is the Driver class"""
    fields_errMSG = {
        'license_number': 'Missing license number',
        **Staff.fields_errMSG,
    }
    if models.storage_type == "db":
        __tablename__ = 'drivers'
        staff_id = Column(String(60), ForeignKey('staff.id'), nullable=False)
        license_number = Column(String(50), unique=True)
    else:
        staff_id = ""
        license_number = ""


class Dispatcher(BaseModel, Base):
    """This is the class for dispatcher
    """
    fields_errMSG = {
        **Staff.fields_errMSG
    }
    if storage_type == "db":
        __tablename__ = "dispatchers"
        staff_id = Column(String(60), ForeignKey('staff.id'), nullable=False)
    else:
        staff_id = ""

    def dispatch_ambulance(self, incident_id, hospital_id):
        """This is the method to dispatch ambulance"""
        pass