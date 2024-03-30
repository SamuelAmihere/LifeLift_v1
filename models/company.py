#!/usr/bin/python3
"""This is the user class"""
import datetime
from sqlalchemy.ext.declarative import declarative_base
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Enum, ForeignKey, String
from models import storage_type
from sqlalchemy.orm import relationship


class Company(BaseModel, Base):
    """This is the class for institution/company
    """
    fields_errMSG = {
        'name': 'Missing name',
        # to create address
        'email': 'Missing email',
        'phone': 'Missing phone_number',
        'street': 'Missing street',
        'city': 'Missing city',
        'state': 'Missing state',
        'zipcode': 'Missing zipcode',
        'country': 'Missing country',

        'status': 'Missing status'
    }
    if storage_type == "db":
        __tablename__ = "companies"
        name = Column(String(128), nullable=False)
        address_id = Column(String(60), ForeignKey('addresses.id'), nullable=False)
        status = Column(Enum('active', 'inactive'), default='active')
        staff = relationship("Staff", back_populates="company", cascade="delete")
        ambulances = relationship("Ambulance", back_populates="company", cascade="delete")
    else:
        name = ""
        address_id = ""
        status = ""
        available_staff = []
        available_ambulances = []

        @property
        def staff(self):
            """This method returns a list of all staff
            working for this company
            """
            if len(self.available_staff) > 0:
                return self.available_staff
            else:
                return None
        @staff.setter
        def staff(self, value):
            """This method sets the list of all staff
            working for this company
            """
            if value not in self.available_staff:
                self.available_staff.append(value)

        @property
        def ambulances(self):
            """This method returns a list of all ambulances
            owned by this company
            """
            if len(self.available_ambulances) > 0:
                return self.available_ambulances
            else:
                return None
            
        @ambulances.setter
        def ambulances(self, value):
            """This method sets the list of all ambulances
            owned by this company
            """
            if value not in self.available_ambulances:
                self.available_ambulances.append(value)

            
    def assign_staff_to_ambulance(self, staff_id:str,
                                   ambulance_id:str):
        """This method adds staff to an ambulance"""
        data = models.storage.all()
        ambus = {}
        for key, value in data.items():
            if 'Ambulance.' in key:
                ambus[key] = value
        ambu = ambus.get('Ambulance.'+ambulance_id)
        if ambu is not None:
            ambu.staff_id = staff_id
            ambu.updated_at = datetime.utcnow()
        ambus['Ambulance.'+ambulance_id] = ambu
    
        if ambu is not None:
            data.update(ambus)
            models.storage.save()
        return False
    
    def remove_staff_from_ambulance(self, staff_id:str,
                                    ambulance_id:str):
        """This method removes staff from an ambulance"""
        data = models.storage.all()
        ambus = {}
        for key, value in data.items():
            if 'Ambulance.' in key:
                ambus[key] = value
        ambu = ambus.get('Ambulance.'+ambulance_id)
        if ambu is not None:
            ambu.pop('staff_id', None)
            ambu['updated_at'] = datetime.utcnow()
        else:
            return False
        ambus['Ambulance.'+ambulance_id] = ambu

        data.update(ambus)
        models.storage.save()

        return True