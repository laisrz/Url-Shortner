from flask import Flask, redirect, render_template, request, jsonify
from pony.orm import *
from datetime import datetime, date
import uuid
import validators
from validators import ValidationFailure


app = Flask(__name__)


# Configurating database
db = Database()

# Creating entities
class URL(db.Entity):
    _table_ = 'url'
    id = PrimaryKey(int, auto=True)
    long_url = Required(str)
    short_url = Required(str)
    creation_date = Required(datetime)
    expiration_date = Optional(date)
    number_visits = Optional(int)
    is_deleted = Required(bool, default=0)

# Database binding
db.bind(
        provider='mysql',
        host='localhost',
        user='root',
        passwd='',
        db='urlshortener'
    )

# Mapping entities to database tables
db.generate_mapping(create_tables=True)

set_sql_debug(True)


@app.route("/", methods=['GET'])
def index():

   #show homepage
   return render_template("index.html")


@app.route("/", methods=['POST'])
@db_session
def shorten_url():
   
    '''Transform long url in short url'''
    '''Insert it into database'''

    # Get data from json
    data = request.get_json()

    long_url = data["long_url"]

    expiration_date = data["expiration_date"]

    # Validate URL
    result = validators.url(long_url)
    if isinstance(result, ValidationFailure):
        return jsonify({"message": "Invalid url"})

    ### algoritm to transform long url into short url
    short_url = str(uuid.uuid4())

	

    ### insert into database
    URL(
        long_url=long_url,
        short_url=short_url,
        creation_date=datetime.now(),
        expiration_date=expiration_date
    )
    commit()

    # return short url to the user
    return jsonify({"short url": short_url})
   

@app.route("/<short_url>")
@db_session
def get_url(short_url):
    """Retrieve long_url from a given short url and redirect the user to the long_url"""
    
    url_data = URL.get(short_url=short_url)

    # Validate user's input
    if url_data == None:
        return jsonify({"message": "URL provided not stored in database"})
    
    if url_data.is_deleted == 1:
        return jsonify({"message": "URL provided has been deleted"})
    
    if url_data.expiration_date == None or url_data.expiration_date > date.today():
        #Update counter
        url_data.number_visits =+ 1

        # Redirect to the long_url
        return redirect(url_data.long_url)
    
    if url_data.expiration_date < date.today():
        return jsonify({"message": "URL provided has expired"})


@app.route("/", methods=['PUT'])
def update_url():
    pass


@app.route("/", methods=['DELETE'])
@db_session
def delete_url():
    '''Delete short url'''
    
    # get data from json
    data = request.get_json()

    short_url = data["short_url"]

    # Fetch id of short url to be deleted
    url_data = URL.get(short_url=short_url)

    # Validate user's input
    if url_data == None:
        return jsonify({"message": "URL provided not stored in database"})
    
    # Delete from database
    url_data.is_deleted = 1
    commit()

    # Return message to the user
    return jsonify({"message": "Short URL deleted"})




if __name__ == '__main__':
    app.run(debug=True)