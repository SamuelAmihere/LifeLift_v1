#!/usr/bin/python3
""" Blueprint for Lifelift API """
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.hospitals import *
from api.v1.views.companies import *
from api.v1.views.contacts import *
from api.v1.views.location import *
# from api.v1.views.ambulances import *
from api.v1.views.patients import *
from api.v1.views.incident import *
from api.v1.views.user import *
# from api.v1.views.health_messages import *
# from api.v1.views.active_ambulances import *