#!/usr/bin/env python3
"""This is the module for support functions for interacting
"""
from models.incident import Incident
from models.location import Address
from models.system_user import Patient, Person


class SignUp:
    """
    This is the class for sign up
    """
    address_fields = Address.fields_errMSG.keys()
    person_fields = Person.fields_errMSG.keys()
    incident_fields = Incident.fields_errMSG.keys()
    patient_fields = Patient.fields_errMSG.keys()

    def __init__(self, data):
        """This is the constructor for the class
        data: dictionary of the data on person, address, patient, incident
        """
        self.person = self.prepare_data(Person.fields_errMSG)
        self.address = self.prepare_data(Address.fields_errMSG)
        self.patient = self.prepare_data(Patient.fields_errMSG)
        self.incident = self.prepare_data(Incident.fields_errMSG)

    def prepare_data(self, obj_fileds):
        """This function gets the person"""
        final_data = {}
        for k, v in obj_fileds.items():
            final_data[k] = v
        return final_data
    
    def get_data(self):
        """This function gets the data"""
        tmp = {}
        # merge the data from the person, address, patient, incident
        tmp.update(self.person)
        tmp.update(self.address)
        tmp.update(self.patient)
        tmp.update(self.incident)
        return tmp



    
        


