from pony import orm
from flask import Flask, redirect, render_template, request, jsonify
from datetime import datetime, date
import uuid
from validations import data, url
from database import db_config


app = Flask(__name__)


@app.route("/", methods=['GET'])
def index():

   #show homepage
   return render_template("index.html")


@app.route("/", methods=['POST'])
@orm.db_session
def shorten_url():
   
    '''Transform long url in short url'''
    '''Insert it into database'''

    # Get data from json
    user_data = request.get_json()

    long_url = user_data["long_url"]

    expiration_date = user_data["expiration_date"]

    # Validate URL
    if url.is_not_valid(long_url):
        return url.is_not_valid(long_url)
        
    ### algoritm to transform long url into short url
    short_url = str(uuid.uuid4())

    ### insert into database
    db_config.URL(
        long_url=long_url,
        short_url=short_url,
        creation_date=datetime.now(),
        expiration_date=expiration_date
    )
    orm.commit()

    # return short url to the user
    return jsonify({"short url": short_url})
   

@app.route("/<short_url>")
@orm.db_session
def get_url(short_url):
    """Retrieve long_url from a given short url and redirect the user to the long_url"""
    
    db_data = db_config.URL.get(short_url=short_url)

    # Validate user's input
    if data.db_data_not_found(db_data):
        return data.db_data_not_found(db_data)
    
    if data.is_deleted(db_data):
        return data.is_deleted(db_data)
    
    if data.is_expired(db_data):
        return data.is_expired(db_data)

    if not db_data.expiration_date or db_data.expiration_date > date.today():
        #Update counter
        if not db_data.number_visits:
            db_data.number_visits =+ 1
        else:
            db_data.number_visits = db_data.number_visits + 1

        # Redirect to the long_url
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

    # Get all data from database based on the short url provided
    db_data = db_config.URL.get(short_url=short_url)

    # Validate user's input
    if data.db_data_not_found(db_data):
        return data.db_data_not_found(db_data)
    
    if data.is_deleted(db_data):
        return data.is_deleted(db_data)
    
    if data.is_expired(db_data):
        return data.is_expired(db_data)
    
    if url.is_not_valid(new_long_url):
        return url.is_not_valid(new_long_url)
    
    # Update database
    db_data.long_url = new_long_url
    orm.commit()

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
    if data.db_data_not_found(db_data):
        return data.db_data_not_found(db_data)

    
    # Delete from database
    db_data.is_deleted = 1
    orm.commit()

    # Return message to the user
    return jsonify({"message": "Short URL deleted"})


if __name__ == '__main__':
    app.run(debug=True)