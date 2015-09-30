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
The base URL will look like http://www.mysite.com/api.  Note that if you're
using the docker container above you will want to use a URL that would be
http://localhost:9090/api as the base.

* POST - Start by POST'ing a long URL to get the short URL back.  The POST should 
contain a JSON object that looks like:

`{"longUrl": "http://www.google.com"}`

Note that the service is not expecting any other URL parameters.  This method
returns a JSON object that contains the short URL:

`{"shortUrl": "http://www.mysite.com/api/4h38dgg4qh2nf"}`

* GET - Use the GET method in the /api namespace to get the long URL
from the short one.  The URL will be look like:

`http://www.mysite.com/api/4h38dgg4qh2nf`

where the last part of the URL is the encoded section of the short URL.
This will redirect you to the long URL.

* DELETE - If you no longer need your short url you can delete it.  Use
the DELETE method and call:

`http://www.mysite.com/api/4h38dgg4qh2nf`

You will get back an HTTP status code depending on the result of the
delete.  If the short URL portion can be found then you'll get back an
HTTP status code of "202" - "Accepted".  This means that the system
found your code and deleted it.  If the short URL portion cannot be
found then you'll get back a "204" - "No Content".

## Configuration
Since this code could run on any domain, the "http://www.mysite.com" portion
can be configured to your environment.  For local testing it will likely
be set to "http://localhost:8080".  But, if you wanted to host this service
on, for example, "http://dgi.io", change the "BASE_HOST_NAME" variable at the
top of the server.py file.
