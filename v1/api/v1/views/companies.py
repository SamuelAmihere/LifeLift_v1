#! /usr/bin/env python3
"""This is the company api"""
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger import Swagger, swag_from
from models.company import Company
from models.contact import Contact
from models.utils.delete_data import delete_company, delete_company_address, delete_company_contact
from models.utils.post_data import post_company
from models.utils.retrieve_data import get_company, get_company_address, get_company_contact
from models.utils.update_data import modify_comp, modify_company_address, modify_company_contact


ignore_keys = ['id', 'created_at', 'updated_at']

@app_views.route('/company', methods=['POST'], strict_slashes=False)
@swag_from('documentation/company/create_company.yml', methods=['POST'])
def create_company():
    """Create a new company"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400

    company = post_company(data)
    if not company:
        return jsonify({"error": "company not created"}), 400
    return jsonify(company), 201

# GETs
@app_views.route('/company/<company_id>', methods=['GET'],
                 strict_slashes=False)
@app_views.route('/company', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/company/company.yml', methods=['GET'])
def company(company_id=None):
    """Get company(s)"""
    if not company_id:
        companies = get_company()
        return jsonify(companies)
    company = get_company(company_id)
    return jsonify(company)

@app_views.route('/company/<company_id>/contact', methods=['GET'],
                    strict_slashes=False)
@swag_from('documentation/company/company_contact.yml', methods=['GET'])
def company_contact(company_id=None):
    """Get company contact"""
    if not company_id:
        return jsonify({"error": "company_id is missing"})
    contact = get_company_contact(company_id)
    return jsonify(contact)

@app_views.route('/company/<company_id>/address', methods=['GET'],
                    strict_slashes=False)
@swag_from('documentation/company/company_address.yml', methods=['GET'])
def company_address(company_id=None):
    """Get company address"""
    if not company_id:
        return jsonify({"error": "company_id is missing"})
    address = get_company_address(company_id)    
    return jsonify(address)

# PUTs
@app_views.route('/company/<company_id>', methods=['PUT'],
                 strict_slashes=False)
@swag_from('documentation/company/update_company.yml', methods=['PUT'])
def update_company(company_id):
    """Update a company"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400

    company = modify_comp(data, company_id)
    return jsonify(company)

@app_views.route('/company/<company_id>/contact', methods=['PUT'],
                    strict_slashes=False)
@swag_from('documentation/company/update_company_contact.yml', methods=['PUT'])
def update_company_contact(company_id):
    """Update a company contact"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400

    contact = modify_company_contact(data, company_id)
    return jsonify(contact)

@app_views.route('/company/<company_id>/address', methods=['PUT'],
                    strict_slashes=False)
@swag_from('documentation/company/update_company_address.yml', methods=['PUT'])
def update_company_address(company_id):
    """Update a company address"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400

    address = modify_company_address(data, company_id)
    return jsonify(address)

# DELETEs
@app_views.route('/company/<company_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/company/remove_company.yml', methods=['DELETE'])
def remove_company(company_id=None):
    """Delete a company"""
    company = get_company(company_id)
    if 'error' in company:
        return company
    return delete_company(company_id)

@app_views.route('/company/<company_id>/contact', methods=['DELETE'],
                    strict_slashes=False)
@swag_from('documentation/company/remove_company_contact.yml', methods=['DELETE'])
def remove_company_contact(company_id=None):
    """Delete a company contact"""
    company = get_company(company_id)
    if 'error' in company:
        return company
    return delete_company_contact(company_id)

@app_views.route('/company/<company_id>/contact/<contact_id>', methods=['DELETE'],
                    strict_slashes=False)

@app_views.route('/company/<company_id>/address', methods=['DELETE'],
                    strict_slashes=False)
@swag_from('documentation/company/remove_company_address.yml', methods=['DELETE'])
def remove_company_address(company_id=None):
    """Delete a company address"""
    company = get_company(company_id)
    if 'error' in company:
        return company
    return delete_company_address(company_id)
