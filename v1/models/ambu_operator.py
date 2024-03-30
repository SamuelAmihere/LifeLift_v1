#! /usr/bin/python3
"""This is the Ambulance Operator module"""
from sqlalchemy import Column, ForeignKey, String
import models
from sqlalchemy.orm import relationship
from models.base_model import Base, BaseModel


class AmbulanceOwner(BaseModel, Base):
    """This is the Ambulance Operator class"""
    fields_errMSG = {
        # to create company
        'name': 'Missing name',
        'email': 'Missing email',
        'phone': 'Missing phone_number',
        'street': 'Missing street',
        'city': 'Missing city',
        'state': 'Missing state',
        'zipcode': 'Missing zipcode',
        'country': 'Missing country',
        'status': 'Missing status'
    }
    if models.storage_type == "db":
        __tablename__ = 'operators'
        company_id = Column(String(60), ForeignKey('companies.id'),
                            nullable=False)
    else:
        company_id = ""