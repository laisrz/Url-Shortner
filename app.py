from pony import orm
from flask import Flask, redirect, render_template, request, jsonify
from datetime import date
from database import db_config, db_operations
import validators
from validators import ValidationFailure


app = Flask(__name__, static_url_path='/static')


@app.route("/", methods=['GET'])
def index():

   #show homepage
   return render_template("index.html")


@app.route("/", methods=['POST'])
@orm.db_session
def shorten_url():
   
    '''Transform original url in short url'''
    '''Insert it into database'''

    # Get data from json
    user_data = request.get_json()

    long_url = user_data["original_url"]

    expiration_date = user_data["expiration_date"]

    # Validate URL
    result = validators.url(long_url)
    
    if isinstance(result, ValidationFailure):
        response = jsonify({"message": "Invalid url"})
        response.status_code = 400
        return response
    
    ### insert into database
    short_url = db_operations.insert_new(db_config, long_url, expiration_date)

    # return short url to the user
    return jsonify({"short url": short_url})
   

@app.route("/<short_url>")
@orm.db_session
def get_url(short_url):
    """Retrieve long_url from a given short url and redirect the user to the long_url"""
    
    db_data = db_config.URL.get(short_url=short_url)

    # Validate user's input
    if not db_data:
        response = jsonify({"message": "URL provided not stored in database"})
        response.status_code = 404
        return response
    
    if db_data.is_deleted == 1:
        response = jsonify({"message": "URL provided has been deleted"})
        response.status_code = 410
        return response
    
    if db_data.expiration_date < date.today():
        response = jsonify({"message": "URL provided has expired"})
        response.status_code = 410
        return response

    # Redirect to the long_url
    if not db_data.expiration_date or db_data.expiration_date > date.today():
        #Update counter
        if not db_data.number_visits:
            db_data.number_visits =+ 1
        else:
            db_data.number_visits = db_data.number_visits + 1

        
        return redirect(db_data.long_url)
    

@app.route("/", methods=['PUT'])
@orm.db_session
def update_url():
    '''Update short url to redirect to a different long URL'''
    '''Should we implement a login for the user be able to do this??'''

    # Get data from json
    user_data = request.get_json()
    short_url = user_data["short_url"]
    new_long_url = user_data["long_url"]
    expiration_date = user_data["expiration_date"]

    # Get all data from database based on the short url provided
    db_data = db_config.URL.get(short_url=short_url)

    # Validate user's input
    if not db_data:
        response = jsonify({"message": "URL provided not stored in database"})
        response.status_code = 404
        return response
    
    if db_data.is_deleted == 1:
        response = jsonify({"message": "URL provided has been deleted"})
        response.status_code = 410
        return response
    
    if db_data.expiration_date < date.today():
        response = jsonify({"message": "URL provided has expired"})
        response.status_code = 410
        return response
    
    # Validate url
    result = validators.url(new_long_url)
    
    if isinstance(result, ValidationFailure):
        response = jsonify({"message": "Invalid url"})
        response.status_code = 400
        return response
    
    # Update database
    db_operations.update(db_config, short_url, new_long_url, expiration_date)

    # Return message to the user
    return jsonify({"message": "URL sucessfully updated", "short_url": short_url})


@app.route("/", methods=['DELETE'])
@orm.db_session
def delete_url():
    '''Delete short url'''
    
    # get data from json
    user_data = request.get_json()

    short_url = user_data["short_url"]

    # Fetch id of short url to be deleted
    db_data = db_config.URL.get(short_url=short_url)

    # Validate user's input
    if not db_data:
        response = jsonify({"message": "URL provided not stored in database"})
        response.status_code = 404
        return response

    # Delete from database
    db_operations.delete(db_config, short_url)

    # Return message to the user
    return jsonify({"message": "Short URL deleted"})


if __name__ == '__main__':
    app.run(debug=True)