#! /usr/bin/env python3
"""This module contains the Alert class"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Table
from sqlalchemy import ForeignKey, Enum
from sqlalchemy.orm import relationship
from models import storage_type
from models.incident import Incident


if storage_type == "db":
    alert_hospital = Table('alert_hospital', Base.metadata,
                           Column('alert_id', String(60),
                                  ForeignKey('alerts.id'),
                                  primary_key=True,
                                  nullable=False),
                           Column('hospital_id', String(60),
                                  ForeignKey('hospitals.id'),
                                  primary_key=True,
                                  nullable=False)
                           )
    alert_site = Table('alert_site', Base.metadata,
                       Column('alert_id', String(60),
                              ForeignKey('alerts.id'),
                              primary_key=True,
                              nullable=False),
                       Column('site_id', String(60),
                              ForeignKey('sites.id'),
                              primary_key=True,
                              nullable=False)
                       )

class Alert(BaseModel, Base):
    """This is the Alert class"""
    fields_errMSG = {
        'alert_type': 'Missing alert type',
        'alert_status': 'Missing alert status',
        **Incident.fields_errMSG,
    }
    if storage_type == "db":
        __tablename__ = 'alerts'
        alert_type = Column(String(100), nullable=False)
        alert_status = Column(Enum('comfirmed', 'pending', 'resolved'),
                              nullable=False)

        incident_id = Column(String(60), ForeignKey('incidents.id'),
                             nullable=False)
        incident = relationship("Incident", back_populates="alerts")
        sites = relationship("Site", secondary=alert_site,
                             back_populates="alerts")
        hospitals = relationship("Hospital", secondary=alert_hospital,
                                 back_populates="alerts")
    else:
        alert_type = ""
        alert_status = ""
        incident_id = ""
        sites = []
        hospitals = []

        @property
        def sites(self):
            """This is the getter method for sites"""
            if len(self.sites) > 0:
                return []
            return self.sites
        
        @property
        def hospitals(self):
            """This is the getter method for hospitals"""
            if len(self.hospitals) > 0:
                return []
            return self.hospitals
        
        @sites.setter
        def sites(self, value):
            """This is the setter method for sites"""
            if type(value) == list:
                self.sites.append(value)

        @hospitals.setter
        def hospitals(self, value):
            """This is the setter method for hospitals"""
            if type(value) == list:
                self.hospitals.append(value)