#! /usr/bin/env python3
"""This is the module for support functions"""


from datetime import datetime
import json

from flask import redirect, url_for



def is_valid_date(date):
    """This function checks if the date is valid"""
    try:
        datetime.strptime(date, '%Y-%m-%d')
        return True
    except ValueError:
        return False
    

def authenticate_inputs(*args):
    """This function authenticates the inputs"""
    for i in args:
        if i == "" or i == None:
            return ("Missing input")
        
def redirect_usertype(user_type):
    """This function redirects the user based on user type"""
    if user_type == "admin":
        return redirect(url_for("admin"))
    elif user_type == "company":
        return redirect(url_for("company"))
    elif user_type == "nurse":
        return redirect(url_for("health_tip"))
    elif user_type == "driver":
        return redirect(url_for("driver"))
    else:
        return redirect(url_for("home"))

def data_ok(actual_cls, data):
    """
    This method checks the data type and returns a dictionary
    data: dictionary of the data
    """
    print("==============================")
    print(f"Data is {type(data)}")
    if type(data) != dict or not data or len(data) == 0:
        print(f"Data is not a dictionary {data}")
        return None
    # check if the data is complete
    fields_flag = True
    # for field in data.keys():
    print(actual_cls.fields_errMSG.keys(), "====>")
    for field in actual_cls.fields_errMSG.keys():
        if field not in data.keys():
            print(f"Field [[{field}]] is not in {data.keys()}")
            fields_flag = False
    if not fields_flag:
        print(actual_cls.fields_errMSG.keys(), "====>")
        print(f"Field(s) for {actual_cls.__name__} not in {data.keys()}")
        return None
    return data

def validate_distance_loc(cls, distance, lat, lng):
    """This function validates the distance between two locations"""
    errs = {}
    # if cls not in [Hospital, Site, Ambulance, ActiveAmbulance, Location]:
        # errs['cls'] = f'Invalid class: [{cls}]'
    if not lat:
        errs['lat'] = 'Missing latitude'
    if not lng:
        errs['lng'] = 'Missing longitude'
    if type(lat) != float or type(lat) != int or lat < -90 or lat > 90:
        errs['lat'] = 'Invalid latitude'
    if type(lng) != float or type(lng) != int or lng < -180 or lng > 180:
        errs['lng'] = 'Invalid longitude'
    if distance:
        if type(distance) != float or type(distance) != int or distance < 0:
            errs['distance'] = 'Invalid distance'
    return errs

def update_location(obj:dict, lat=None, lng=None):
    """This function updates the location of a patient
    obj: object whose location is to be updated
    lat: latitude of the new location
    lng: longitude of the new location
    """
    if not obj:
        return {f"error: {obj.get('id')} not found"}
    if not lat or not lng:
        return {f"error": "Missing latitude or longitude"}
    obj["latitude"] = lat
    obj["longitude"] = lng
    return obj

def distance(lat1, lon1, lat2, lon2):
    """This function calculates the distance between two points"""
    from math import sin, cos, sqrt, atan2, radians

    # approximate radius of earth in km
    R = 6373.0

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return distance