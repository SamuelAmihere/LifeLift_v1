#!/usr/bin/python3
"""This is the user class"""
from sqlalchemy.ext.declarative import declarative_base
from models import storage_type
from models.system_user import Staff


class Dispatcher(Staff):
    """This is the class for dispatcher
    """
    if storage_type == "db":
        __tablename__ = "dispatchers"
    else:
        pass

    def dispatch_ambulance(self, incident_id, hospital_id):
        """This is the method to dispatch ambulance"""
        pass