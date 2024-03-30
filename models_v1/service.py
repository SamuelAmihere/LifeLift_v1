#! /usr/bin/env python3
""" This module contains the Service class """
from datetime import datetime
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, DateTime, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from models import storage_type


class Service(BaseModel, Base):
    """This is the Service class.
    It contains services provided by the system
    to patients
    """
    if storage_type == "db":
        __tablename__ = "services"
        status = Column(Enum('Pending', 'ongoing', 'Resolved', 'Cancelled'),
                        default='Pending',
                        nullable=False)
        # status update by ambulance at dispatch (ongoing),
        # at patient (Resolved), at hospital (Resolved),
        # by dispatcher (Cancelled

        incident_id = Column(String(60), ForeignKey('incidents.id'),
                             nullable=False)
        ambulance_id = Column(String(60), ForeignKey('ambulances.id'),
                              nullable=False) # update by dispatcher
        alert_id = Column(String(60), ForeignKey('alerts.id'), nullable=False)
        request_time = Column(DateTime, nullable=False)
        accepted_time = Column(DateTime, default=datetime.utcnow,
                            nullable=False)
        dispatch_time = Column(DateTime, nullable=True) # update by ambulance at dispatch
        arrival_time_pat = Column(String(128), nullable=True) # update by ambulance at patient
        arrival_time_hos = Column(String(128), nullable=True) # update by ambulance at hospital
        review_services = relationship("ReviewService", back_populates="service", cascade="delete")
    else:
        status = ""
        incident_id = ""
        ambulance_id = ""
        alert_id = ""
        request_time = ""
        accepted_time = ""
        dispatch_time = ""
        arrival_time_pat = ""
        arrival_time_hos = ""
        all_reviews = []
        @property
        def reviews(self):
            """Getter for reviews"""
            for rev in models.storage.all("ReviewService").values():
                if rev.service_id == self.id and rev not in self.all_reviews:
                    self.all_reviews.append(rev)
            return self.all_reviews

        @reviews.setter
        def reviews(self, value):
            """Setter for reviews"""
            if type(value) == str and value not in self.all_reviews:
                self.all_reviews.append(value)