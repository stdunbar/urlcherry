# Digital Globe Code

This is a simple URL shortening app for Digital Globe.

To interact with the system, you can use the existing Dockerfile
to bring up a Docker container.  If running a local Docker container,
checkout this directory and build it:

docker build -t somename/mywebapp:latest .

The tag above can be whatever you'd like.

Then, run something like:

docker run -p 9090:8080 -i -t somename/mywebapp:latest

## Interacting with the web service
The web service follows a basic REST pattern, using GET, POST, and DELETE.
Start by POST'ing a long URL to get the short URL back.  The POST should 
contain a JSON object that looks like:

`{"longUrl": "http://www.google.com"}`
