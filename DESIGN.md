### How it should work
* A web page should display options for the user to shorten, update, delete or retrieve an url.
* On the server side, upon a request to shorten a url, the application should first connect (and, if necessary, creating it) to a MySql database.
* Then, transform the long url into a short one (by which method: hash function (it could, teorically, create two identical hashs?), iterating through IDs, random IDs??)
* Insert both urls on the database and returning to the web server the short url.
* When a call is made to the short url, the application should look into the database for the correspondent long url and redirect the web request to the long URL page.
* A request to update or delete the short url should connect to the database and do the necessary modifications.
