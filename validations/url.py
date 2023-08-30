import validators
from validators import ValidationFailure
from flask import jsonify

def is_invalid(long_url):
    result = validators.url(long_url)
    
    if isinstance(result, ValidationFailure):
        response = jsonify({"message": "Invalid url"})
        response.status_code = 400

        return response