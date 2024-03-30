#! /usr/bin/env python3
""" objects that handle all default RestFul API actions
for Health Messages
"""

from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from
from models.hosp_operator import HealthMessage
from models.hosp_operator import HealthTopic

ignore_keys = ['id', 'created_at', 'updated_at']

@app_views.route('/health_messages', methods=['GET'], strict_slashes=False)
@swag_from('swagger_yaml/health_messages/get_health_messages.yml')
def get_health_messages():
    """ Retrieves the list of all Health Messages """
    health_messages = storage.all(HealthMessage)
    return jsonify([health_message.to_dict() for health_message in health_messages.values()])