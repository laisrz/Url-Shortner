# URL Shortner

Let's build our own URL shortening service. Think bit.ly or tinyurl.com services.

Basically it is a service that let people turn long and confuse URLs in nice and short URLs that are easy to share.

## Requirements

We need to let people enter the URL somewhere. For this, we need an API endpoint that accepts a URL and returns a short URL. People should be able to:

* Shorten a URL
* Delete a URL
* Update a URL
* Retrieve a URL

## Technologies Used

* Flask
* PonyORM/MySQL

## API Endpoints

- `GET "/"`- to access the homepage with instructions on how to perform all available operations in the API: shorten, delete,
update and retrieve an url
- `POST "/"`- to provide information in order to shorten an url. Returns the shortened url
- `GET "/<short_url>"` - to get the original url from the shortened url
- `PUT "/"` - to update a shortened url to point to a different long url
- `DELETE "/"` - to delete a shortened url

## Setup Instructions

  ### Configure a Virtual Environment
  * In order to setup a virtual environment and install the packages needed to run this project, you'll need to have pip
    installed. Pip is the primary Python package manager. The Python installers for Windows include pip, but you can confirm
    you have the latest version:

    $ py -m pip install --upgrade pip
    $ py -m pip --version

  * Now, you'll need to create a virtual environment. In the project’s directory run:

    Windows:
    $ py -m venv env

    Unix/macOS:
    $ python3 -m venv env

  * Activate the virtual environment:
    
    Windows:
    $ .\env\Scripts\activate

    Unix/macOS:
    $ source env/bin/activate
    
  ### Install dependencies
  In Windows, run:
  $ py -m pip install -r requirements.txt

  In Unix/macOS:
  $ python3 -m pip install -r requirements.txt

  Obs: for additional information, look into: https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/
  
  ### Setup MYSQL Server
  1. Download XAMPP (software tool that handles MySQL administration over the web): https://www.apachefriends.org/download.html
  2. Start the following two processes once XAMPP has been installed and loaded:
     * Apache
     * MySQL
  3. Go to https://localhost in your browser and click on phpMyAdmin on the upper right.
  4. Create a new database named: "urlshortener"
  5. Go to the project's directory and open the file db_config.py on the database module. Update the information of the user and password of the mysql database.

Obs: for additional information: https://hevodata.com/learn/flask-mysql/

## Run the Application

  1. Start the Flask development server, by running, in the project’s directory:
     $ flask run
     
  2. Open a web browser and navigate to http://localhost:5000 to access the URL Shortener.








  
