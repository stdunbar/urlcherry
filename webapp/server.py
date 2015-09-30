import os, os.path
import random
import sqlite3
import string
import time

import cherrypy

DB_STRING = "url.db"
BASE_HOST_NAME = "http://www.mysite.com/"

class ShortUrlGenerator(object):
   @cherrypy.expose
   def index(self):
       return file('index.html')

class ShortUrlWebService(object):
    exposed = True

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.popargs('generator')
    def GET(self, generator):

        with sqlite3.connect(DB_STRING) as c:
            r = c.execute("select long_url from short_urls where short_url = ?", [generator])
            longUrl = r.fetchone()
            return {"longUrl": longUrl[0]}

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    @cherrypy.tools.accept(media='application/json')
    def POST(self):
        data = cherrypy.request.json;

        """
            does the long url already exist?
        """
        with sqlite3.connect(DB_STRING) as c:
            r = c.execute("select short_url from short_urls where long_url = ?",
                          [data["longUrl"]])
            thisShortUrl = r.fetchone();
            if thisShortUrl != None:
                return {"shortUrl": BASE_HOST_NAME + thisShortUrl[0]}

        """
            no, so hash the long url and base 36 encode it
        """
        shortUrl = encodeBase36(hash(data["longUrl"]))
        with sqlite3.connect(DB_STRING) as c:
            c.execute("insert into short_urls values (?, ?)",
                      [data["longUrl"], shortUrl])
        return {"shortUrl": BASE_HOST_NAME + shortUrl}

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.popargs('generator')
    def DELETE(self, generator):
        with sqlite3.connect(DB_STRING) as c:
            rowCount = c.execute("delete from short_urls where short_url=?",
                      [generator]).rowcount

        if rowCount > 0:
            return {"status": "deleted"}
        else:
            return {"status": "no match to short url"}


def setup_database():
    """
    Create the `short_urls` table in the database
    on server startup if the table doesn't already
    exist
    """
    with sqlite3.connect(DB_STRING) as con:
        con.execute("create table if not exists short_urls (long_url, short_url)")

ALPHABET = "0123456789bcdfghjklmnpqrstvwxyz"

def encodeBase36(n):
    if n == 0:
        return ALPHABET[0]

    # We're only dealing with nonnegative integers.

    if n < 0:
        raise Exception() # Raise a better exception than this in real life.


    result = ""

    while (n > 0):
        result = ALPHABET[n % len(ALPHABET)] + result
        n /= len(ALPHABET)

    return result

if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/generator': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        },
        '/css': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './css'
        }
    }
    cherrypy.engine.subscribe('start', setup_database)

webapp = ShortUrlGenerator()
webapp.generator = ShortUrlWebService()
cherrypy.config.update({'server.socket_host': '0.0.0.0'})
cherrypy.quickstart(webapp, '/', conf)
