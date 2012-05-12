import webapp2
import cgi
import datetime
import urllib
import os
import jinjia2

from google.appengine.ext import db
from google.appengine.api import users
import model

class MainPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()

        if user:
            self.response.out.write('Hello' + user.nickname())
        else:
            self.redirect(users.create_login_url(self.request.uri))

app = webapp2.WSGIApplication([('/h', MainPage)],
                              debug = True)
