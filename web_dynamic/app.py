#! /usr/bin/env python3
"""This is flask app"""
import hashlib
import os
from random import random
import sys
import uuid
from datetime import datetime

from flask import Flask, abort, flash, jsonify, make_response
from flask import render_template, redirect, request, url_for, session
from flask_cors import CORS, cross_origin
from flasgger import Swagger
from flask_session import Session
import requests
from models import company, storage
from models import storage_type
from models.ambu_operator import AmbulanceOwner
from models.hosp_operator import Hospital
from models.incident import Incident
from models.location import Address
from models.system_user import Patient, Person, Staff
from models.user import User
from models.utils.create_companies import create_hospitals
from models.utils.google import nearby_hospitals, read_hospital_data_json
from models.utils.retrieve_data import close_hosp
from models.utils.sign_up import SignUp
from models.utils.create_table import CreateExternalUser, CreateUser, auth_user
from models.company import Company
from models.utils.support import redirect_usertype
from flask_login import LoginManager, current_user, login_required, login_user, logout_user

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
CORS(app, support_credentials=True)
Swagger(app)
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)
login_manager.session_protection = None

app.url_map.strict_slashes = False

visitors = "visitors.json"

# define global variable
userN = 'user_name'
userT = 'user_type'

GOOGLEMAP_API_KEY = os.getenv('GOOGLEMAP_API_KEY')

# Siging up
details_msg = {
    **Staff.fields_errMSG,
    'password': 'Missing password',
}
details_msg.update(Person.fields_errMSG)
address_msg = Address.fields_errMSG
incident_msg = Incident.fields_errMSG
person_msg = Person.fields_errMSG
patient_msg = Patient.fields_errMSG

# Patient request
request_msg = {**address_msg,
               **person_msg,
               **patient_msg,
               **incident_msg,
               'name': 'Missing name',
               }
# login
login_msg = {
    'user_name': 'Missing user name',
    'mail': 'Missing email',
    'password': 'Missing password',
}

staff_category = {
    'nurse': Hospital,
    'driver': AmbulanceOwner,
    'admin': Hospital,
}

user_nav_acess = {
    'nurse': 'health_tip',
    'driver': 'ambulance',
    'admin': 'admin',
}


data = {} # store the data from the form

# Admin page
@app.route('/admin', methods=['GET'])
@login_required
def admin():
    """Admin page"""
    # if session["user_name"] == None:
    session["user_name"]='amisam2000@gmail.com'
    session["user_type"]='admin'
    hosp = requests.get('http://localhost:5005/api/v1/hospitals').json()
    patients = requests.get('http://localhost:5005/api/v1/patients').json()
    cache_id = (str(uuid.uuid4()))
    
    pat = []
    for p in patients:
        lat = request.args.get('lat')
        lng = request.args.get('lng')
        top = 3 if not request.args.get('top') else request.args.get('top')

        if lat != None and lng != None and p.get("id") != None:
            p['hospitals'] = close_hosp(p.get("id") , lat, lng, hosp=hosp, top=top).get(p.get("id"))
        elif lat == None and lng == None and p.get("id")  != None:
            p['hospitals'] = close_hosp(p.get("id"), hosp=hosp, top=top).get(p.get("id"))
        elif lat != None and lng != None and p.get("id")  == None:
            p['hospitals'] = close_hosp(lat, lng, hosp=hosp, top=top).get(p.get("id"))
        pat.append(p)
    return (render_template('admin.html',
                            hospitals=hosp,
                            patients=pat,
                            requests_count=pat[-1].get('No'),
                            cache_id=cache_id
                            ))#GOOGLEMAP_API_KEY=GOOGLEMAP_API_KEY

# Home page
@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def home():
    """Home page"""

    results = requests.get('http://localhost:5005/api/v1/hospitals').json()
    pat = requests.get('http://localhost:5005/api/v1/patients').json()
    cache_id = (str(uuid.uuid4()))
    
    return (render_template('home.html',
                            hospitals=results,
                            patients=pat,
                            incident_type=['Health', 'Accident', 'Fire', 'Robbery', 'Others'],
                            user_nav_acess=user_nav_acess,
                            cache_id = cache_id
                            ))#GOOGLEMAP_API_KEY=GOOGLEMAP_API_KEY

# Google map page
@app.route('/map', methods=['GET'])
def map():
    """Google map page"""
    GOOGLEMAP_API_KEY = os.getenv('GOOGLEMAP_API_KEY')
    return (render_template('googlemap.html', ))#GOOGLEMAP_API_KEY=GOOGLEMAP_API_KEY

# Ambulance page
@app.route('/ambulance', methods=['GET'])
def ambulance():
    """Ambulance page"""
    return (render_template('ambu.html', ))#GOOGLEMAP_API_KEY=GOOGLEMAP_API_KEY

# Emergency request
@app.route('/emergency_request', methods=['POST'])
def emergency_request():
    """Emergency request page"""
    cache_id = (str(uuid.uuid4()))
    if request.method == 'POST':
        # check if the request is from a form or json
        if request.is_json:
            print("Type:lat: ", type(float(request.json.get('lat'))))
            data['lat'] = float(request.json.get('lat'))
            data['lng'] = float(request.json.get('lng'))
        if request.form:
            for key in request_msg:
                try:
                    data[key] = request.form.get(key).strip()
                except AttributeError:
                    data[key] = request.form.get(key)
            
            data_final = {}
            for k, v in data.items():
                if v == "" or v == None:
                    continue
                try:
                    if 'phone' in k:
                        data_final[k] = v
                    else:
                        data_final[k] = float(v)
                except ValueError:
                    data_final[k] = v
      
            # update the data
            data_final['status'] = 'pending'
            data_final['city'] = 'Accra'
            data_final['state'] = 'Greater Accra'
            data_final['country'] = 'Ghana'
            data_final['zipcode'] = '00233'

            # Add fields for Alert
            data_final['alert_type'] = data_final['incident_type']
            data_final['alert_status'] = 'pending'

            # singUp_data = SignUp(data_final)
            # all_data = singUp_data.get_data()
            # # create patient
            
            print("========Final Data===========")
            print("Data: ", data_final)
        
            user_creator = CreateExternalUser()
            patient = user_creator.create_patient(data_final)
            if patient == None:
                return (render_template('home.html', error="Error creating patient", cache_id=cache_id))
            
    return (redirect(url_for('home')))

# Hospital page
@app.route('/hospital', methods=['GET'])
# @login_required
def hospital():
    """Hospital page"""
    return (render_template('hosp.html' ))#GOOGLEMAP_API_KEY=GOOGLEMAP_API_KEY

# Health tip page
@app.route('/health_tip', methods=['GET'])
@login_required
def health_tip():
    """Health tip page"""
    topic = [
        {'topic': 'First Aid', 'id':'ythrhyh4545hgegr'},
        {'topic': 'Malaria', 'id':'ythrhyh4545hgegr'},
        {'topic': 'Cholera', 'id':'ythrhyh4545hgegr'},
        {'topic': 'Diabetes', 'id':'ythrhyh4545hgegr'},
        {'topic': 'Hypertension', 'id':'ythrhyh4545hgegr'}]
    cache_id = (str(uuid.uuid4()))
    return (render_template('health_tip.html',
                            healthTopic=topic,
                            user_nav_acess=user_nav_acess,
                            cache_id=cache_id))

# login page
@login_manager.user_loader
def load_user(user_id):
    return storage.get_one_by(User, id=user_id)

@app.route('/login', methods=['GET', 'POST'])
# @login_required
def login():
    """Login page"""
    cache_id = (str(uuid.uuid4()))
    if current_user.is_authenticated:
        print("========User===========")
        print("User: ", current_user)
        return redirect_usertype(current_user.user_type)  # Redirect to the index page if user is already logged in

    if request.method == 'POST':
        data = {}
        for key in login_msg:
            if request.form.get(key) is None:
                abort(400, description=login_msg[key])
            data[key] = request.form.get(key)
        
        # authenticate user
        email = str(data['user_name']) + '@' + str(data['mail'])

        pwd = data['password']
        
        user = auth_user(email, pwd)
        error = {}
        if user == 0:
            error["email"] = "*Incorrect Email"
        elif user == 1:
            error["user_name"] = "*User does not exist"
        elif user == 2:
            error["password"] = "*Incorrect Password"
        else:
            pass
        if len(error) > 0:
                print("========Error===========")
                print("Error: ", error)
                return (render_template('login.html',
                                        user_nav_acess=user_nav_acess,
                                        error_login=error, cache_id=cache_id))#GOOGLEMAP_API_KEY=GOOGLEMAP_API_KEY,
        else:
            next = request.args.get('next')
            login_user(user)
            return redirect_usertype(current_user.user_type)
    
    return (render_template('login.html',
                            user_nav_acess=user_nav_acess,
                            cache_id=cache_id
                            ))#GOOGLEMAP_API_KEY=GOOGLEMAP_API_KEY


# logout page
@app.route('/logout', methods=['GET'])
@login_required
def logout():
    """Logout page"""
    logout_user()
    # flash("You were logged out.", "success")
    return redirect(url_for('home'))

# register page
@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register page"""
    cache_id = (str(uuid.uuid4()))
    usertType = ['admin', 'company', 'nurse', 'driver']
    gender = ['male', 'female']
    
    other_info = {
        'city': 'Accra',
        'state': 'Greater Accra',
        'country': 'Ghana',
        'zipcode': '00233',
        'status': 'active',
    }

    registration = {
        "success": None,
        "error": None,
        "user_exits": None
        }
    # error_registration = None
    if request.method == 'POST':


        data = {}

        for key in details_msg:
            # Update data with other info
            
            # if request.form.get(key) is None or request.form.get(key) == "":

            #     return (render_template('register.html',
            #                             registration=registration,
            #                             field_error=details_msg[key],
            #                             GOOGLEMAP_API_KEY=GOOGLEMAP_API_KEY,
            #                             usertType=usertType, gender=gender))
            # check if the field is empty
            if request.form.get(key) == "":
                return (render_template('register.html',
                                        registration=registration,
                                        field_error=details_msg[key],
                                        usertType=usertType,
                                        cache_id=cache_id,
                                        ))#GOOGLEMAP_API_KEY=GOOGLEMAP_API_KEY,
            data[key] = request.form.get(key.strip())

        data['user_name'] = data['email'].split('@')[0]
        data['user_type'] = request.form.get('userType')

        data
        data.update(other_info)

        print("========Data===========")
        print("Data: ", data)
        print("==============================")



        # create user
        user_creator = CreateUser()
        


        my_user = user_creator.create_user(data=data)

        if not my_user:
            registration['error'] = "Registration Unsuccessful. <b> Login or use another email address</b>"
            return (render_template('register.html',
                                        registration=registration,
                                        user_nav_acess=user_nav_acess,
                                        usertType=usertType,
                                        gender=gender,
                                        cache_id=cache_id))#GOOGLEMAP_API_KEY=GOOGLEMAP_API_KEY,
        if my_user:
            # Registration successful
            registration['success'] = "Account Created Successfully"
            print("========User created===========")
            return (render_template('register.html',
                                    registration=registration,
                                    user_nav_acess=user_nav_acess,
                                    usertType=usertType,
                                    gender=gender,
                                    cache_id=cache_id))#GOOGLEMAP_API_KEY=GOOGLEMAP_API_KEY,

    elif request.method == 'GET':
        companies = storage.all(Company)
        return (render_template('register.html',
                                registration=registration,
                                company=[company.to_dict() for company in companies.values()],
                                user_nav_acess=user_nav_acess,
                                usertType=usertType, gender=gender,
                                cache_id=cache_id))#GOOGLEMAP_API_KEY=GOOGLEMAP_API_KEY,
    else:
        abort(405, description="Method not allowed")


@app.route('/person/', methods=['POST', 'GET'])
def create_person():
    """Create a new user"""

    if request.method == 'POST':
        print("========Posting===========")
        print("request.form: ", request.form.get('email'))

        email = request.form['email']
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        phone = request.form.get('phone_number')
        gender = request.json.get('gender')
        
        for field in [email, first_name, last_name, phone, gender]:
            if field is None:
                abort(400, description="Missing field")
            for key in details_msg:
                if request.form.get.get(key) is None:
                    abort(400, description=details_msg[key])

        person_obj = storage.get_by(Person, 'email')
        
        if person_obj.email == email:
            print("========Person exists===========")
            return jsonify(person_obj.to_dict()), 200

        # create new person
        person = Person(email=email, first_name=first_name,
                        last_name=last_name, phone_number=phone)
        person.save()
        print("========Person creted===========")  
    return jsonify(person.to_dict()), 201

# get all people
@app.route('/people', methods=['GET'])
def get_people():
    """Get all users"""
    people = storage.all(Person)

    if people is None:
        abort(404)
    people = [person.to_dict() for person in people.values()]
    return jsonify(people), 200


@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Get a user"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())



# get all users
@app.route('/users', methods=['GET'])
def get_users():
    """Get all users"""
    users = storage.all(User)
    users = [{userN: user.to_dict().get(userN), userT: user.to_dict().get(userT)}\
             for user in users.values()]
    return jsonify(users)




# get all companies: Hospitals, AmbulanceOperators
# get Hospitals
@app.route('/hospitals', methods=['GET'])
def get_hospitals():
    """Get all hospitals"""
    cache_id = (str(uuid.uuid4()))
    if request.method == 'POST':

        pid = request.json.get('patient_id')

        hospitals = requests.get(f'http://localhost:5005/api/v1/patients/{pid}/hospitals').json()
        print("========Hospitals===========")
        print("Hospitals: ", hospitals)
    return (render_template('admin.html',
                            hospitals=hospitals,
                            cache_id=cache_id
                            ))#GOOGLEMAP_API_KEY=GOOGLEMAP_API_KEY

@app.errorhandler(404)
def not_found(error):
    """Return 404 error"""
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == "__main__":
    app.config['SESSION_TYPE'] = 'filesystem'
    app.debug = True
    app.run(host="localhost", port=5000)