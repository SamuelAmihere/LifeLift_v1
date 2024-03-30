#!/usr/bin/python3
""" Blueprint for Lifelift API """
from flask import Blueprint
from flask import jsonify


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')



# @app_views.route('/', methods=['GET'])
# def home():
#     """ Status of API """
#     return jsonify({"status": "OK"})

from .index import *
# from .hospitals import *
# from api.v1.views.ambulances import *
# from api.v1.views.patients import *
# from api.v1.views.users import *
# from api.v1.views.health_messages import *
# from api.v1.views.active_ambulances import *