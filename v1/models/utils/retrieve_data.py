#! /usr/bin/env python3
"""This is the create companies module
"""

from datetime import datetime
import json
from models import storage
from models.ambulance import ActiveAmbulance, Ambulance
from models.company import Company
from models.contact import Contact
from models.hosp_operator import Hospital
from models.incident import Incident
from models.location import Address, Location, Site
from models.system_user import Patient
from models.user import User
from models.utils.algorithms import find_closest
from models.utils.support import data_ok, update_location, validate_distance_loc
from models.utils.support import distance

def get(cls, obj_id=None):
    """This function gets an object"""
    if obj_id:
        if type(obj_id) != str:
            return {"error": "id must be a string"}
        obj = storage.get_one_by(cls, id=obj_id)
        if not obj:
            return {"error": f"{cls.__name__} not found"}
        return obj.to_dict()
    else:
        objs = storage.all(cls).values()
        if not objs:
            return {"error": f"{cls.__name__} not found"}
        objs_list = []
        for obj in objs:
            objs_list.append(obj.to_dict())
        return objs_list

def get_by_address(id):
    """This function gets an object"""
    obj = storage.get_one_by(Contact, address_id=id)
    if not obj:
        return {"error": f"Contact not found"}
    return obj.to_dict()

def get_by_location(cls, lat, lng):
    """This function gets an object"""
    # verify params
    errs = {}
    if cls not in [Hospital, Site, Ambulance, ActiveAmbulance, Location]:
        errs['cls'] = f'Invalid class: [{cls}]'
    if not lat:
        errs['lat'] = 'Missing latitude'
    if not lng:
        errs['lng'] = 'Missing longitude'
    if type(lat) != float or type(lat) != int or lat < -90 or lat > 90:
        errs['lat'] = 'Invalid latitude'
    if type(lng) != float or type(lng) != int or lng < -180 or lng > 180:
        errs['lng'] = 'Invalid longitude'
    if len(errs) > 0:
        return errs
    
    obj = storage.get_one_by(cls, latitude=lat, longitude=lng)
    if not obj:
        return {"error": f"{cls.__name__} not found"}
    return obj.to_dict()

def get_by_distance(cls, distance_required, lat, lng):
    """This function gets all objects within a distance
    cls: class
    distance: distance
    lat: latitude - reference point
    lng: longitude - reference point
    """
    # verify paramsHospital
    errs = validate_distance_loc(cls, distance_required, lat, lng)
    if len(errs) > 0:
        return errs
    objs = storage.all(cls).values()
    # determine the objects within the distance
    objs_list = []
    for obj in objs:
        dist = distance(float(objs.latitude), float(objs.longitude),
                        lat, lng)
        if dist <= distance_required:
            obj.distance = dist
            objs_list.append(obj.to_dict())
    # sort the objects by distance
    objs_list.sort(key=lambda x: x['distance'])
    return objs_list

def get_nearby(obj_cls, lat, lng):
    """This function gets all objects within a distance
    cls: class
    lat: latitude - reference point
    lng: longitude - reference point
    """
    # verify params
    # errs = validate_distance_loc(cls, None, lat, lng)
    # if len(errs) > 0:
    #     return errs
    objs = storage.all(obj_cls).values()
    # determine the objects nearby
    objs_list = []
    for obj in objs:
        # find the distance between the reference point and
        # the object using the distance method
        dist = distance(float(objs.latitude), float(objs.longitude),
                        lat, lng)
        obj.distance = dist
        objs_list.append(obj.to_dict())
    # sort the objects by distance
    objs_list.sort(key=lambda x: x['distance'])
    return objs_list
        

# ------------ COMPANIES ------------
def get_company(id=None):
    """This function gets company(s)"""
    if not id:
        return get(Company)
    return get(Company, id)

def get_company_address(company_id=None):
    """This function gets company address(s)"""
    if not company_id:
        return {"error": "company_id is missing"}
    company = get_company(company_id)
    if 'error' in company:
        return company
    adddress = get(Address, company.get('address_id'))
    if 'error' in adddress:
        return adddress
    return adddress

def get_company_contact(company_id=None):
    """This function gets company contact(s)"""
    if not company_id:
        return {"error": "company_id is missing"}
    company = get_company(company_id)
    print("===================")
    print(company)
    if 'error' in company:
        return company
    contact = get_by_address(company.get('address_id'))
    return contact


# ------------ CONTACTS ------------
def get_contact(id=None):
    """This function gets contact(s)"""
    if not id:
        contact = get(Contact)
    else:
        contact = storage.get_one_by(Contact, id=id)
        if not contact:
            return {"error": "Contact not found"}
    return contact

def get_contact_by(id):
    """This function gets contact(s) by data"""
    return get_by_address(id)

# ------------ HOSPITAL ------------
def get_hospital(id=None):
    """This function gets company(s)"""
    results = []
    data_hospitals = storage.all(Hospital)
    for obj in data_hospitals.values():
        comp = storage.get_one_by(Company, id=obj.company_id)
        obj.name = comp.name
        contact = storage.get_one_by(Contact, address_id=comp.address_id)
        if contact is None:
            obj.contact = '+2330000000000'
        else:
            obj.contact = contact.phone_number
        results.append(obj.to_dict())
    if not id:
        return results
    for result in results:
        if result.get('id') == id:
            return result
    return {"error": "Hospital not found"}

def get_hospital_address(hospital_id=None):
    """This function gets hospital address(s)"""
    if not hospital_id:
        return {"error": "hospital_id is missing"}
    hospital = get_hospital(hospital_id)
    if 'error' in hospital:
        return hospital
    adddress = get(Address, hospital.get('address_id'))
    if 'error' in adddress:
        return adddress
    return adddress

def get_hospital_by_location(id):
    """This function gets hospital(s) by location (lat, long)"""
    location = get(Location, id)
    if 'error' in location:
        return location
    return get_hospital(location.get('id'))

# ------------ LOCATIONS ------------
def get_location(id=None):
    """This function gets address(s)"""
    if not id:
        return get(Location)
    return get(Location, id)


# ------------ SITES ------------


# ------------ USERS ------------
def get_user(id=None):
    """This function gets user(s)"""
    if not id:
        return get(User)
    return get(User, id)

def get_user_by_email(email):
    """This function gets user(s) by email"""
    user = storage.get_one_by(User, email=email)
    if not user:
        return {"error": "User not found"}
    return user.to_dict()

# ------------ Patient Request ------------
def get_patient_request(id=None):
    """This function gets patient request(s)"""
    if not id:
        objs = storage.all(Patient).values()
        pat = []
        i = 0
        for obj in objs:
            incident = storage.get_one_by(Incident, id=obj.incident_id)
            if incident:
                i += 1
                obj.reason = incident.incident_description
                obj.latitude = incident.latitude
                obj.longitude = incident.longitude
                obj.No = i
                diff = datetime.utcnow() - obj.created_at
                sec = diff.total_seconds()
                minutes = sec / 60
                hours = minutes / 60
                days = hours / 24

                time = ""
                if days > 1:
                    time = "{} day{}".format(int(days), "s" if int(days) > 1 else "")
                elif hours > 1:
                    time = "{} hr{}".format(int(hours), "s" if int(hours) > 1 else "")
                elif minutes > 1:
                    time = "{} mn{}".format(int(minutes), "s" if int(minutes) > 1 else "")
                else:
                    time = "{} sec{}".format(int(sec), "s" if int(sec) > 1 else "")

                obj.time = time
                pat.append(obj.to_dict())
        return pat
    return get(Patient, id)

def get_patient_incident(patient_id=None):
    """This function gets patient incident"""
    if not patient_id:
        return {"error": "patient_id is missing"}
    patient = storage.get_one_by(Patient, id=patient_id)
    if not patient:
        return {"error": "Patient not found"}
    incident = storage.get_one_by(Incident, id=patient.incident_id)
    if not incident:
        return {"error": "Incident not found"}
    return incident.to_dict()

# ------------ INCIDENT ------------
def get_incident(id=None):
    """This function gets incident(s)"""
    if not id:
        return get(Incident)
    return get(Incident, id)

def close_hosp(patient_id=None, lat=None, lng=None, hosp=None, top=3, incident=False):
    """Close a hospital
    patient_id: patient id
    lat: latitude
    lng: longitude
    top: number of hospitals to return
    """
    patients_hosps = {}
    patients = get_patient_request(patient_id)
    if hosp is None:
        hosp = get_hospital()

    # if a patient_id is not provided, get all patients and
    # find the closest hospitals to them
    if not patient_id and not incident:
        patients = get_patient_request(patient_id)
        for p in patients:
            if not lat or not lng:
                lat = get_incident(id=p.get("incident_id")).get("latitude")
                lng = get_incident(id=p.get("incident_id")).get("longitude")
            p = update_location(p, lat, lng)
            clos_hosps = find_closest(float(p.get['latitude']),
                                      float(p.get['longitude']),
                                      hosp, top)
            patients_hosps[p.get("id")] = clos_hosps[0:3]
        
        
        return patients_hosps
    
    


    # if patient_id is provided, find the closest hospitals
    # to the patient
    
    if not incident:
        p = get_patient_request(patient_id)
        if not lat and not lng:
            p_lat = get_incident(id=p.get("incident_id")).get("latitude")
            p_lng = get_incident(id=p.get("incident_id")).get("longitude")
        
        p = update_location(p, p_lat, p_lng)

        clos_hosps = find_closest(float(p['latitude']),
                              float(p['longitude']), hosp, top)
        patients_hosps[patients.get("id")] = clos_hosps[0:3]
        return patients_hosps
    else:
        clos_hosps = find_closest(float(lat),
                                float(lng), hosp, top)
        patients_hosps["hospitals"] = clos_hosps[0:3]
        return patients_hosps