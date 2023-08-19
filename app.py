from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL
from pony.orm import *
from datetime import datetime, date
import uuid
import validators
from validators import ValidationFailure


app = Flask(__name__)


# Configurating database
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'urlshortener'
 
mysql = MySQL(app)


@app.route("/", methods=['GET'])
def index():

   #show homepage
   return render_template("index.html")


@app.route("/", methods=['POST'])
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

    #Creation of a cursor to database
    cursor = mysql.connection.cursor()

    ### insert into database
    cursor.execute('''INSERT INTO url (long_url, short_url, creation_date, expiration_date)
                           VALUES(%s, %s, %s, %s)''', 
                           (long_url, short_url, datetime.now(), expiration_date))
    mysql.connection.commit()

    #Closing the cursor
    cursor.close()

    # return short url to the user
    return jsonify({"short url": short_url})
   

@app.route("/")
def get_url():
    '''Retrieve short url'''
    
    # get data from json
    data = request.get_json()

    long_url = data["long_url"]

    # Creation of a cursor to database
    cursor = mysql.connection.cursor()

    # Fetch id of short url to be deleted
    id = cursor.execute("SELECT id FROM url WHERE long_url = ?", long_url)

    if not id:
        return jsonify({"message": "URL cannot be retrieved"})

    # Check whether URL has been deleted
    is_deleted = cursor.execute("SELECT is_deleted FROM url WHERE id = ?", id)

    if is_deleted == 1:
        return jsonify({"message": "URL cannot be retrieved"})
    
    # Check whether URL has been expired
    expiration_date = cursor.execute("SELECT expiration_date FROM url WHERE id = ?", id)

    if expiration_date < date.today():
        return jsonify({"message": "URL has been expired"})

    # Get shor_url from database
    short_url = cursor.execute("SELECT short_url FROM url WHERE id = ?", id)

    # Closing the cursor
    cursor.close()

    # Return message to the user
    return jsonify({"short_url": short_url})


@app.route("/", methods=['PUT'])
def update_url():
    pass


@app.route("/", methods=['DELETE'])
def delete_url():
    '''Delete short url'''
    
    # get data from json
    data = request.get_json()

    short_url = data["short_url"]

    # Creation of a cursor to database
    cursor = mysql.connection.cursor()

    # Fetch id of short url to be deleted
    id = cursor.execute("SELECT id FROM url WHERE short_url = ?", short_url)

    # Delete from database
    cursor.execute("UPDATE url SET is_deleted = ? WHERE id = ?", (1, [id]))
    mysql.connection.commit()

    # Closing the cursor
    cursor.close()

    # Return message to the user
    return jsonify({"message": "Short URL deleted"})



if __name__ == '__main__':
    app.run(debug=True)