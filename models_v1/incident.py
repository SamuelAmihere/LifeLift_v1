#! /usr/bin/env python3
"""
This module contains the Incident class
"""
from models.base_model import BaseModel
from sqlalchemy import Column, ForeignKey, Enum, String, Float, Table
from sqlalchemy.orm import relationship
import models
from models.base_model import Base


if models.storage_type == "db":
    incident_ambulances = Table('incident_ambulances', Base.metadata,
                                    Column('ambulance_id', String(60),
                                            ForeignKey('ambulances.id'),
                                            primary_key=True,
                                            nullable=False),
                                    Column('incident_id', String(60),
                                            ForeignKey('incidents.id'),
                                            primary_key=True,
                                            nullable=False)
                                    )

class Incident(BaseModel, Base):
    """This is the Incident class"""
    # Fields to retrieve external data
    fields_errMSG = {
        'incident_type': 'Missing incident',
        'incident_description': 'Missing description',
        'lat': 'Missing latitude',
        'lng': 'Missing longitude',
        'status': 'Missing status'
    }
    if models.storage_type == "db":
       __tablename__ = 'incidents'
       incident_type = Column(String(50), nullable=False)
       latitude = Column(Float, nullable=False)
       longitude = Column(Float, nullable=False)
       incident_status = Column(Enum('Pending', 'Resolved', 'Cancelled'),
                                   default='Pending')
       incident_description = Column(String(100), nullable=False)
       patients = relationship("Patient", backref="incidents",
                               cascade="delete")
       ambulances = relationship("Ambulance", secondary=incident_ambulances,
                                back_populates="incidents", cascade="delete")
       alerts = relationship("Alert", back_populates="incident",
                             cascade="delete")
    else:
       incident_type = ""
       latitude = 0.0
       longitude = 0.0
       incident_status = ""
       incident_description = ""
       available_patients = []
       current_ambulances = []
       available_alerts = []

       @property
       def patients(self):
           """Getter for patients"""
           for pat in models.storage.all("Patient_119").values():
               if pat.incident_id == self.id and pat not in self.available_patients:
                   self.available_patients.append(pat)
           return self.available_patients
       
       @property
       def ambulances(self):
           """Getter for ambulances"""
           for amb in models.storage.all("Ambulance").values():
               if self.id in amb.incidents and amb not in self.current_ambulances:
                   self.current_ambulances.append(amb)
           return self.current_ambulances

       @property
       def alerts(self):
           """Getter for alerts"""
           for alert in models.storage.all("Alert").values():
               if alert.incident_id == self.id and alert not in self.available_alerts:
                   self.available_alerts.append(alert)
           return self.available_alerts

       @alerts.setter
       def alerts(self, value):
           """Setter for alerts"""
           if isinstance(value, str) and value not in self.available_alerts:
               self.available_alerts.append(value)
           
       available_alerts
       @patients.setter
       def patients(self, value):
           """Setter for patients"""
           if isinstance(value, str) and value not in self.available_patients:
               self.available_patients.append(value)

       @ambulances.setter
       def ambulances(self, value):
           """Setter for ambulances"""
           if isinstance(value, str) and value not in self.current_ambulances:
               self.current_ambulances.append(value)