#!/usr/bin/python3
""" Index """
from models.hosp_operator import Hospital
from models.review import Review
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/', methods=['GET'])
def status():
    """ Status of API """
    return jsonify({"status": "OK"})


# @app_views.route('/hospitals', methods=['GET'], strict_slashes=False)
# def number_objects():
#     """ Retrieves the number of each objects by type """

#     num_objs = {"hospital": storage.count(Hospital)}
#     return jsonify(num_objs)