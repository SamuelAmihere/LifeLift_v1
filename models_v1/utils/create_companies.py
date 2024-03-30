#! /usr/bin/env python3
"""This is the create companies module
"""
import json
from models import storage
from models.hosp_operator import Hospital
from models.utils.create_table import CreateCompany


def create_hospitals(data_src):
    """This function creates a hospital
    data: a dictionary with the following keys
    return: a dictionary with the hospital id
    """
    with open(data_src) as file:
        data_json = json.load(file)
        loaded = data_json['items']

    contact_data = {}
    address_data = {}

    if loaded:
        i,j = 0,0
        for hos in loaded:
            # create hospital
            temp = {}
            if 'title' in hos:
                temp['name'] = hos['title']
            elif len(hos) > 0:
                temp['name'] = "#"
            else:
                continue
            if 'position' in hos:
                temp['lat'] = hos['position']['lat']
                temp['lng'] = hos['position']['lng']
            temp['status'] = "active"
            
            # create address
            if 'address' in hos:
                if 'street' in hos['address']:
                    address_data['street'] = hos['address']['street']
                else:
                    address_data['street'] = "#"*6
            else:
                address_data['street'] = "#"*6
            address_data['city'] = "Accra"
            address_data['state'] = "Greater Accra"
            address_data['zipcode'] = "00233"
            address_data['country'] = "Ghana"
            # add address to temp
            temp.update(address_data)

            if 'contacts' in hos:
                try:
                    if 'phone' in hos['contacts'][0]:
                        contact_data['phone'] = hos['contacts'][0]['phone'][0]['value'][0]['value']
                    elif 'mobile' in hos['contacts'][0]:
                        contact_data['phone'] = hos['contacts'][0]['mobile'][0]['value']
                    elif 'telephone' in hos['contacts'][0]:
                        contact_data['phone'] = hos['contacts'][0]['telephone'][0]['value']
                    elif 'tel' in hos['contacts'][0]:
                        contact_data['phone'] = hos['contacts'][0]['tel'][0]['value']
                    elif 'fax' in hos['contacts'][0]:
                        contact_data['phone'] = hos['contacts'][0]['fax'][0]['value']
                    else:
                        contact_data['phone'] = '#'*10

                    if 'email' in hos['contacts'][0]:
                        contact_data['email'] = hos['contacts'][0]['email'][0]['value']
                    if 'mail' in hos['contacts'][0]:
                        contact_data['email'] = hos['contacts'][0]['mail'][0]['value']
                    else:
                        contact_data['email'] = '**********@gmail.com'
                except Exception as e:
                    print(e)
            else:
                contact_data['phone'] = '#'*10
                contact_data['email'] = '**********@gmail.com'
            temp.update(contact_data)

            if temp:
                
                hos = CreateCompany().create(Hospital, 'hospital', temp)
                if hos:
                    i += 1
                    print(f"[{i}] Hospital created: {hos.id}")
                    print("******************************************")
                else:
                    j += 1
                    print(f"[{i}] Hospital not created", temp)
                    print("==========================================")

        print(f"Total hospitals created: {i}")
        print(f"Total hospitals not created: {j}")