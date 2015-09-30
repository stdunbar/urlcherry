# Digital Globe Code

This is a simple URL shortening app for Digital Globe.

To interact with the system, you can use the existing Dockerfile
to bring up a Docker container.  If running a local Docker container,
checkout this directory and build it:

`docker build -t somename/mywebapp:latest .`

The tag above can be whatever you'd like.

Then, run something like:

`docker run -p 9090:8080 -i -t somename/mywebapp:latest`

## Interacting with the web service
The web service follows a basic REST pattern, using GET, POST, and DELETE.
The base URL will look like http://www.mysite.com/generator

* POST - Start by POST'ing a long URL to get the short URL back.  The POST should 
contain a JSON object that looks like:

`{"longUrl": "http://www.google.com"}`

Note that the service is not expecting any other URL parameters.  This method
returns a JSON object that contains the short URL:

`{"shortUrl": "http://www.mysite.com/4h38dgg4qh2nf"}`

* GET - Use the GET method in the /generator namespace to get the long URL
from the short one.  The URL will be look like:

`http://www.mysite.com/generator/4h38dgg4qh2nf`

where the last part of the URL is the encoded section of the short URL.
This will return the long URL:

`{"longUrl": "http://www.google.com"}`

* DELETE - If you no longer need your short url you can delete it.  Use
the DELETE method and call:

`http://www.mysite.com/generator/4h38dgg4qh2nf`

You will get back a JSON response with a status in it.  

`{"status": "deleted"}`

if there is a match to delete, or

`{"status": "no match to short url"}`

if the system cannot find a match


