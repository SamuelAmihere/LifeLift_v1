#! /usr/bin/env python3
"""This is the create companies module
"""
import json
from models import storage
from models.company import Company
from models.contact import Contact
from models.hosp_operator import Hospital
from models.location import Address
from models.utils.create_table import CreateCompany
from models.utils.support import data_ok

def createComp(data, cls=Company):
    """This function creates a company"""
    data = data_ok(cls, data)
    obj = storage.get_one_by(Company, name=data['name'])
    if obj:
        # check address_id
        address = storage.get_one_by(Address, id=obj.address_id)
        if address:
            contact = storage.get_one_by(Contact, id=address.contact_id)
            if contact.email == data['email'] or contact.phone_number == data['phone']:
                return obj

    # create address
    address = storage.get_one_by(Address, street=data['street'], 
                                 city=data['city'], state=data['state'],
                                 zipcode=data['zipcode'],
                                 country=data['country'])
    if not address:
        data_add = {k: y for k,y in data.items() if k in Address.fields_errMSG.keys()}
        address = Address(**data_add)
        if not address.save():
            return None
        address.save()

    # create contact
    contact = storage.get_one_by(Contact, address_id=address.id,
                                 email=data['email'],
                                 phone_number=data['phone'])
    if contact:
        data_con = {
            'email': data['email'],
            'phone_number': data['phone'],
            'address_id': address.id
        }
        contact = Contact(**data_con)
        if not contact:
            return None
        contact.save()

    # create company
    data['address_id'] = address.id
    company = Company(**data)
    if not company:
        return None
    company.save()
    return company

def create_companies(data_src):
    """This function creates a company
    data: a dictionary with the following keys
    return: a dictionary with the company id

    Format of data:
    {
        "items": [
            {
                "name": "LifeLift",
                "address": {
                    "street": "Madina",
                    "city": "Accra",
                    "state": "Greater Accra",
                    "zipcode": "233",
                    "country": "Ghana"
                },
                "contacts": [
                    {
                    "email": "lifelift@gmail.com",
                    "phone": "0233554481421"
                    }
                ],
                "status": "Active"
            },
        ]
    }
    """

    with open(data_src) as file:
        data_json = json.load(file)
        loaded = data_json['items']

    contact_data = {}
    address_data = {}

    if loaded:
        contact_data = {}
        address_data = {}
        for comp in loaded:
            # create company
            temp = {}
            if 'name' in comp:
                #  address
                if 'address' in comp:
                    for key in Address.fields_errMSG.keys():
                        if key in comp['address']:
                            address_data[key] = comp['address'][key]
                        else:
                            address_data[key] = "#"*6
                    # add address to temp
                    temp.update(address_data)
                
                # contact
                if 'contacts' in comp:
                    for key in ['email', 'phone']:
                        if key in comp['contacts'][0]:
                            contact_data[key] = comp['contacts'][0][key]
                        else:
                            contact_data[key] = '#'*10
                    # add contact to temp
                    temp.update(contact_data)

                if 'status' in comp:
                    temp['status'] = comp['status']
                else:
                    temp['status'] = "active"
                temp['name'] = comp['name']

                # create company

                comp = createComp(temp)
        

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
                    print(f"[{i}] Hospital created: {hos.get('id')}")
                    print("******************************************")
                else:
                    j += 1
                    print(f"[{i}] Hospital not created", temp)
                    print("==========================================")

        print(f"Total hospitals created: {i}")
        print(f"Total hospitals not created: {j}")