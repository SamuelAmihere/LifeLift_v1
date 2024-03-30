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

host = os.environ.get('LFTLIFT_HOST', '0.0.0.0')
port = os.environ.get('LFTLIFT_PORT')

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


# Admin page
@app.route('/admin', methods=['GET'])
@login_required
def admin():
    """Admin page"""
    cache_id = (str(uuid.uuid4()))
    
    return (render_template('admin.html',
                            cache_id=cache_id
                            ))#GOOGLEMAP_API_KEY=GOOGLEMAP_API_KEY

# Home page
@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def home():
    """Home page"""
    cache_id = (str(uuid.uuid4()))
    
    return (render_template('home.html',
                            cache_id = cache_id
                            ))#GOOGLEMAP_API_KEY=GOOGLEMAP_API_KEY

# Emergency request
@app.route('/req', methods=['GET', 'POST'])
def emergency_request():
    """Emergency request page"""
    cache_id = (str(uuid.uuid4()))
    if request.method == 'POST':
        pass

    return (render_template("request.html", cache_id=cache_id))#GOOGLEMAP_API_KEY=GOOGLEMAP_API_KEY

# Health tip page
@app.route('/ht', methods=['GET'])
@login_required
def health_tip():
    """Health tip page"""
    cache_id = (str(uuid.uuid4()))
    return (render_template('health_tip.html',
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
        pass
    return (render_template('login.html',
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
        pass

    elif request.method == 'GET':
        return (render_template('register.html',
                                cache_id=cache_id))#GOOGLEMAP_API_KEY=GOOGLEMAP_API_KEY,
    else:
        abort(405, description="Method not allowed")


@app.errorhandler(404)
def not_found(error):
    """Return 404 error"""
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    app.config['SESSION_TYPE'] = 'filesystem'
    app.debug = True
    app.run(host=host, port=port)