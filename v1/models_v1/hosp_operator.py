#! /usr/bin/env python
"""This is the Hospital Operator module"""
import models
from models.base_model import Base, BaseModel
from sqlalchemy import Column, ForeignKey, String, Float
from sqlalchemy.orm import relationship
from models.company import Company
from models.alert import alert_hospital
from models.system_user import Staff

if models.storage_type == "db":
    from models.location import location_hospitals

class HealthTopic(BaseModel, Base):
    """This is the Health Topic class"""
    fields_errMSG = {
        'topic': 'Missing health topic',
    }
    if models.storage_type == "db":
        __tablename__ = 'health_topics'
        topic = Column(String(100), nullable=False)
    else:
        topic = ""


class HealthMessage(BaseModel, Base):
    """This is the Health Topic message class"""
    fields_errMSG = {
        'message': 'Missing health message',
    }
    if models.storage_type == "db":
        __tablename__ = 'health_messages'
        health_topic_id = Column(String(60), ForeignKey('health_topics.id'),
                                 nullable=False)
        hospital_staff_id = Column(String(60), ForeignKey('hospital_staff.id'),
                          nullable=False)
        hospital_staff = relationship("HospitalStaff", back_populates="health_messages")
        message = Column(String(2000), nullable=False)


class HospitalStaff(BaseModel, Base):
    """This is the Hospital Staff class"""
    fields_errMSG = {
        **Staff.fields_errMSG,
        **HealthMessage.fields_errMSG
    }
    if models.storage_type == "db":
        __tablename__ = 'hospital_staff'
        staff_id = Column(String(60), ForeignKey('staff.id'), nullable=False)
        hospital_id = Column(String(60), ForeignKey('hospitals.id'), nullable=False)
        health_messages = relationship("HealthMessage", back_populates="hospital_staff",
                                       cascade="delete")
    else:
        staff_id = ""
        health_messages = []

        @property
        def health_messages(self):
            """This method returns a list of all health messages
            for this staff member
            """
            if len(self.health_messages) > 0:
                return self.health_messages
            return None

        @health_messages.setter
        def health_messages(self, value):
            """This method sets the list of all health messages
            for this staff member
            """
            if value not in self.health_messages:
                self.health_messages = value


class Hospital(BaseModel, Base):
    """This is the Hospital Operator class"""
    fields_errMSG = {
        'lat': 'Missing latitude',
        'lng': 'Missing longitude',
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
        __tablename__ = 'hospitals'
        company_id = Column(String(60), ForeignKey('companies.id'),
                            nullable=False)
        latitude = Column(Float, nullable=False)
        longitude = Column(Float, nullable=False)
        alerts = relationship("Alert", secondary=alert_hospital,
                             back_populates="hospitals")
        locations = relationship("Location", secondary=location_hospitals, back_populates="hospitals")
        staff = relationship("HospitalStaff", back_populates="hospitals",
                             cascade="delete")
    else:
        company_id = ""
        latitude = ""
        longitude = ""
        active_alerts = []
        current_locations = []

        @property
        def alerts(self):
            """This method returns a list of all alerts"""
            if len(self.active_alerts) > 0:
                return self.active_alerts
            return None
        @property
        def locations(self):
            """This method returns a list of all temporal locations
            the hospital is in
            """
            if len(self.current_locations) > 0:
                return self.current_locations
            return None

        @alerts.setter
        def alerts(self, value):
            """This method sets the list of all alerts"""
            if type(value) == str and value not in self.active_alerts:
                self.alerts.append(value)

        @locations.setter
        def locations(self, value):
            """This method sets the list of all alerts"""
            if type(value) == str and value not in self.current_locations:
                self.current_locations.append(value)

    def accept_alert(self):
        """This method accepts an alert"""
        # TODO: Implement this method
        pass