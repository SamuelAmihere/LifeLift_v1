#! /usr/bin/python3
"""This is the Ambulance module"""
from datetime import datetime
import models
from models.alert import Alert
from models.base_model import Base, BaseModel
from sqlalchemy import Column, Float, Integer, String, Enum, Table
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from models.company import Company
from models.hosp_operator import Hospital
from models.location import Site
from models.utils.algorithms import get_current_lat_lon


if models.storage_type == "db":
    from models.incident import incident_ambulances


class Ambulance(BaseModel, Base):
    """This is the Ambulance class"""
    fields_errMSG = {
        'registration_number': 'Missing registration number',
        'model': 'Missing model',
        'capacity': 'Missing capacity',
        'status': 'Missing status',
        # # to create site
        # **Site.fields_errMSG,
        # # to create company
        # **Company.fields_errMSG,
    }
    if models.storage_type == "db":
        __tablename__ = 'ambulances'
        registration_number = Column(String(20), nullable=False)
        model = Column(String(50), nullable=True)
        capacity = Column(Integer, nullable=True, default=0)
        status = Column(Enum('Available', 'Busy', 'Out of Service'),
                        default='Available')
        site_id = Column(String(60), ForeignKey('sites.id'),nullable=False)
        company_id = Column(String(60), ForeignKey('companies.id'), nullable=False)
        site = relationship("Site", back_populates="ambulances", cascade="delete")
        company = relationship("Company", back_populates="ambulances", cascade="delete")
        ambulance_staff = relationship("AmbulanceStaff", back_populates="ambulance", cascade="delete")
        incidents = relationship("Incident", secondary=incident_ambulances,
                                 back_populates="ambulances", cascade="delete")
    else:
        registration_number = ""
        model = ""
        capacity = 0
        status = ""
        ambu_owner_id = 0
        staff = []

        @property
        def staff(self):
            """Getter for staff"""
            if len(self.staff) > 0:
                return self.staff
            return None
        
        @staff.setter
        def staff(self, value):
            """Setter for staff"""
            if value not in self.staff:
                self.staff.append(value)
        

class ActiveAmbulance(BaseModel, Base):
    """This is the ActiveAmbulance class
    1. It inherits from the Ambulance class
    2. Tasks:
        a. Update service.dispatch_time
        b. Update service.arrival_time_pat
        c. Update service.arrival_time_hos
        d. Update service.status
        e. Updates status
        f. Update alert at hospital

    """
    fields_errMSG = {
        'lat': 'Missing latitude',
        'lng': 'Missing longitude',
        # **Ambulance.fields_errMSG,
        # **Alert.fields_errMSG,
        # **Hospital.fields_errMSG,
    }
    if models.storage_type == "db":
        __tablename__ = 'active_ambulances'
        ambulance_id = Column(String(60), ForeignKey('ambulances.id'), nullable=False)
        alert_id = Column(String(60), ForeignKey('alerts.id'), nullable=False)
        latitude = Column(Float, nullable=False)
        longitude = Column(Float, nullable=False)
        destination = Column(String(60), ForeignKey('hospitals.id'), nullable=False)
    else:
        ambulance_id = ""
        alert_id = ""
        current_lat = 0
        current_lon = 0

        @property
        def current_lat(self):
            """Getter for current_lat"""
            lat = get_current_lat_lon()[0]
            if lat:
                return lat
            return 0

        @property
        def current_lon(self):
            """Getter for current_lon"""
            lon = get_current_lat_lon()[1]
            if lon:
                return lon
            return 0

        @property
        def destination(self):
            """Getter for hospital_id"""
            for hosp in models.storage.all("Hospital").values():
                if self.destination == hosp.id:
                    return [hosp.latitude, hosp.longitude]
            return None


    def update_service_dispatch(self, service):
        """Updates the service"""
        if type(service) != str:
            return False
        incidents = models.storage.all("Incident").values()
        services = models.storage.all("Service").values()

        if incidents and services:
            service_obj = [serv for serv in services if serv.id == service][0]
            
            # Check if ambulance is assigned to the incident
            for incident in incidents:
                if self.id in incident.ambulances:
                    # Check if the service is ongoing or pending
                    if incident.id == service_obj.incident_id and\
                        (service_obj.status == "Ongoing" or service_obj.status == "Pending"): 
                        # Update the service
                        service_obj.dispatch_time = datetime.utcnow()
                        service_obj.status = "Ongoing"
                        service_obj.save()
                        return True
        return False

    def update_service_arrival_pat(self, service, location):
        """Updates the service"""
        if type(service) != str or type(location) != str:
            return False
        services = models.storage.all("Service").values()

        service_obj = [serv for serv in services if serv.id == service][0]

        # Check if the service is ongoing
        if self.id == service_obj.ambulance_id and\
            service_obj.status == "Ongoing":
                # Update the service: status, arrival_time_pat 
                service_obj.arrival_time_pat = datetime.utcnow()
                service_obj.status = "Ongoing"
                service_obj.save()
                return True
        return False

    def update_service_arrival_hosp(self, service):
        """Updates the service"""
        if type(service) != str:
            return False
        services = models.storage.all("Service").values()

        service_obj = [serv for serv in services if serv.id == service][0]

        # Check if the service is ongoing
        if self.id == service_obj.ambulance_id and\
            service_obj.status == "Ongoing":
            
            dest = []
            try:
                # Get the destination
                dest = [float(i) for i in self.destination]
            except Exception as e:
                print(e)

            dest_lat, dest_lon = dest if len(dest) > 0 else [0, 0]
            # Check if the ambulance is within 50m of the hospital
            if distance(self.current_lat, self.current_lon,
                        dest_lat, dest_lon) < 0.05:
                # Update the service
                service_obj.arrival_time_hos = datetime.utcnow()
                service_obj.status = "Ongoing"

                
                service_obj.save()
                return True
        return False
    
    def update_service_depart_hosp(self, service):
        """Updates the service"""
        if type(service) != str:
            return False
        services = models.storage.all("Service").values()
        alerts = models.storage.all("Alert").values()

        service_obj = [serv for serv in services if serv.id == service][0]
   
        # Check if the service is ongoing
        if self.id == service_obj.ambulance_id and\
            service_obj.status == "Ongoing":
            # Update the service: status, alert status
            service_obj.status = "Resolved"
            for alert in alerts:
                if alert.id == service_obj.alert_id:
                    alert.alert_status = "Resolved"
                    alert.save()
            service_obj.save()
            return True
        return False