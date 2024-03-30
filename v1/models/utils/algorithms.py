#! /usr/bin/env python3
"""This is the module for algorithms and support"""

# from models.utils.retrieve_data import get_hospital, get_patient_request


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

def get_current_lat_lon():
    """This function gets the current latitude and longitude of
     an ambulance based on gps
    """
    import  requests
    try:
        response = requests.get('http://ipinfo.io')
        data = response.json()
        return [float(i) for i in data['loc'].split(',')]
    except Exception as e:
        print(e)
        return [0, 0]

def find_closest(lat:float, lng:float, dest:dict,  top=3)->list:
    """Find the closest hospital to a patient
    lat: patient Latitude
    lng: patient Longitude
    dest: list of possible destinations (e.g. hospitals) in object form
    top: Best number of hospitals with shortest distances from the patient

    Returns[]: hospitals
    """
    pat_hosp_dist = []
    i = 0
    for h in dest:
        i += 1
        # calculate the distance and add to the object of destination
        h['distance'] = distance(lat, lng, float(h['latitude']),
                                    float(h['longitude']))
        pat_hosp_dist.append(h)
    clos_dist = sorted(pat_hosp_dist, key=lambda x: x.get('distance'))[0:top]
    return clos_dist