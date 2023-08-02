from flask import Flask, redirect, render_template, request
import db

app = Flask(__name__)

# connection to the database
conn, cursor = db.db_cursor()

# creation of table url
db.db_creation(cursor)



@app.route("/", methods=['GET', 'POST'])
def index():

   if request.method == "POST":
       '''Transform long in short url'''
       '''Insert it into database'''

       long_url = request.form.get("long_url")

       ### algoritm to transform long url into short url

       ### insert into database
       cursor.execute('''INSERT INTO url (long_url, short_url)
                           VALUES(?,?)''', long_url, short_url)
       
       ### return short url to the user - should I use AJAX here?
       return render_template("short.html", short_url=short_url)
   
 
   #GET - show homepage
   return render_template("index.html")

 
#Closing the cursor
cursor.close()


if __name__ == '__main__':
    app.run()