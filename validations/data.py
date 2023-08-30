from flask import jsonify
from datetime import date

def is_deleted(db_data):

    if db_data.is_deleted == 1:
        response = jsonify({"message": "URL provided has been deleted"})
        response.status_code = 410
        return response
    

def is_expired(db_data):

    if db_data.expiration_date < date.today():
        response = jsonify({"message": "URL provided has expired"})
        response.status_code = 410
        return response
    

def db_data_not_found(db_data):
    if not db_data:
        response = jsonify({"message": "URL provided not stored in database"})
        response.status_code = 404
        return response