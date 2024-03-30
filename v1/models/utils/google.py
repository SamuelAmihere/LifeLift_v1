# #!/usr/bin/env python
# """ This module contains the functions to interact with the Google Maps API
# """
# import os
# from googleplaces import GooglePlaces, types


# def nearby_hospitals(lat, lng, radius):
#     """
#     This function returns the nearby hospitals within the specified radius
#     lat: latitude of the current location
#     lng: longitude of the current location
#     radius: the radius to search for the hospitals
#     """
#     API_KEY = os.environ.get('GOOGLEMAP_API_KEY')
#     google_places = GooglePlaces(API_KEY)
#     query_result = google_places.nearby_search(
#         lat_lng ={'lat': lat, 'lng': lng},
#         radius = radius,
#         types =[types.TYPE_BANK])
#     print(lat, lng, radius, query_result.has_attributions)
    
#     # If any attributions related with search results print them
#     if query_result.has_attributions == False:
#         return []
#     # Iterate over the search results
#     hospitals = []
#     for place in query_result.places:
#         hospitals.append({
#             "name": place.name,
#             "latitude": place.geo_location['lat'],
#             "longitude": place.geo_location['lng']
#         })
#     return hospitals

# -----------------------------------------------------------------------------------


import os
import requests
import json


def nearby_hospitals(lat, lng, radius):
    URL = "https://discover.search.hereapi.com/v1/discover"
    latitude = lat
    longitude = lng
    api_key = os.environ.get('HERE_API_KEY') # Acquire from developer.here.com
    query = 'hospitals'
    limit = 100

    PARAMS = {
                'apikey':api_key,
                'q':query,
                'limit': limit,
                'at':'{},{}'.format(latitude,longitude)
            } 

    # sending get request and saving the response as response object 
    r = requests.get(url = URL, params = PARAMS) 
    data = r.json()

    with open('hospitals_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


    # hospitalOne = data['items'][0]['title']
    # hospitalOne_address =  data['items'][0]['address']['label']
    # hospitalOne_latitude = data['items'][0]['position']['lat']
    # hospitalOne_longitude = data['items'][0]['position']['lng']

   


    # hospitalTwo = data['items'][1]['title']
    # hospitalTwo_address =  data['items'][1]['address']['label']
    # hospitalTwo_latitude = data['items'][1]['position']['lat']
    # hospitalTwo_longitude = data['items'][1]['position']['lng']

    # hospitalThree = data['items'][2]['title']
    # hospitalThree_address =  data['items'][2]['address']['label']
    # hospitalThree_latitude = data['items'][2]['position']['lat']
    # hospitalThree_longitude = data['items'][2]['position']['lng']


    # hospitalFour = data['items'][3]['title']
    # hospitalFour_address =  data['items'][3]['address']['label']
    # hospitalFour_latitude = data['items'][3]['position']['lat']
    # hospitalFour_longitude = data['items'][3]['position']['lng']

    # hospitalFive = data['items'][4]['title']
    # hospitalFive_address =  data['items'][4]['address']['label']
    # hospitalFive_latitude = data['items'][4]['position']['lat']
    # hospitalFive_longitude = data['items'][4]['position']['lng'] 
    return [data]
    

def read_hospital_data_json(fname):
    """
    This function reads the hospital data from the json file
    """
    with open(fname) as f:
        data = json.load(f)

    hos = []
    for i in range(100):
        hos.append({
            "name": data['items'][i]['title'],
            "address": data['items'][i]['address']['label'],
            "latitude": data['items'][i]['position']['lat'],
            "longitude": data['items'][i]['position']['lng']
        })
    return hos