#!/usr/bin/env python
#
# author <3ogx>
from google.appengine.ext import db
from google.appengine.api import users

class UserModel(db.Model):
    user_id = db.StringProperty()
    author = db.UserProperty()
    register_time = db.DateTimeProperty(auto_now_add=False)
    login_time = db.DateTimeProperty(auto_now_add=True)


class Greeting(db.Model):
    """Model in individual Guestbook entry with an author"""
    author = db.UserProperty()
    content = db.StringProperty(multiline = True)
    date = db.DateTimeProperty(auto_now_add = True)
