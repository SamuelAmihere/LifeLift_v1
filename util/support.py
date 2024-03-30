# #! /usr/bin/env python3
# """This is the module for support functions"""


# from datetime import datetime

# import models
# from models import storage
# from models.company import Company
# from models.hosp_operator import Hospital


# def is_valid_date(date):
#     """This function checks if the date is valid"""
#     try:
#         datetime.strptime(date, '%Y-%m-%d')
#         return True
#     except ValueError:
#         return False
    
# def distance(lat1, lon1, lat2, lon2):
#     """This function calculates the distance between two points"""
#     from math import sin, cos, sqrt, atan2, radians

#     # approximate radius of earth in km
#     R = 6373.0

#     lat1 = radians(lat1)
#     lon1 = radians(lon1)
#     lat2 = radians(lat2)
#     lon2 = radians(lon2)

#     dlon = lon2 - lon1
#     dlat = lat2 - lat1

#     a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
#     c = 2 * atan2(sqrt(a), sqrt(1 - a))

#     distance = R * c

#     return distance

# def get_current_lat_lon():
#     """This function gets the current latitude and longitude of
#      an ambulance based on gps
#     """
#     import  requests
#     try:
#         response = requests.get('http://ipinfo.io')
#         data = response.json()
#         return [float(i) for i in data['loc'].split(',')]
#     except Exception as e:
#         print(e)
#         return [0, 0]
    

# def authenticate_inputs(*args):
#     """This function authenticates the inputs"""
#     for i in args:
#         if i == "" or i == None:
#             return ("Missing input")


# def get_hospitals_db():
#     results = []
#     data_hospitals = storage.all(Hospital)
#     for obj in data_hospitals.values():
#         name = storage.get_one_by(Company, id=obj.company_id).name
#         obj.name = name
#         results.append(obj.to_dict())
#     # hospitals = list(obj.to_dict() for obj in data_hospitals.values())
#     return results
