from flask import Flask, redirect, render_template, request, jsonify
from flask_mysqldb import MySQL
from datetime import datetime
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

    # get data from json
    data = request.get_json()

    long_url = data["long_url"]

    expiration_date = data["expiration_date"]

    ### validate the url


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
    pass


@app.route("/", methods=['PUT'])
def update_url():
    pass


@app.route("/", methods=['DELETE'])
def delete_url():
    pass



if __name__ == '__main__':
    app.run(debug=True)