from flask import Flask
from flask_mysqldb import MySQL


app = Flask(__name__)

# Configurating database
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'urlshortener'
 
mysql = MySQL(app)



def db_cursor():
    '''Creation of a connection and cursor to database'''

    cursor = mysql.connection.cursor()
    conn = mysql.connection.commit()
 
    return conn, cursor


def db_creation(cursor):
    '''Creation of table url'''

    cursor.execute(""" CREATE TABLE IF NOT EXISTS url(
                    id INTEGER NOT NULL PRIMARY KEY,
                    long_url TEXT NOT NULL,
                    short_url TEXT NOT NULL
                 )""")


