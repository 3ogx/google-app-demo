#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import cgi
import webapp2
import datetime
import urllib
import os
import jinja2

from google.appengine.ext import db
from google.appengine.api import users
from model import UserModel
from model import Greeting


# template
jinja_enviroment = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__))
    )

# data model
# class Greeting(db.Model):
#     """Model an individual Guestbook entry with an author, content and date """
#     author = db.UserProperty()
#     content = db.StringProperty(multiline=True)
#     date = db.DateTimeProperty(auto_now_add=True)

# process filter
def guestbook_key(guestbook_name = None):
    return db.Key.from_path('Guestbook', guestbook_name or 'default_guestbook')

# main function
class MainHandler(webapp2.RequestHandler):
    def get(self):
        guestbook_name = self.request.get('guestbook_name')
        greetings_string = Greeting.all().ancestor(
            guestbook_key(guestbook_name)).order('-date')
        greetings = greetings_string.fetch(10)

        """
        greetings = db.GqlQuery(
            "SELECT * "
            "FROM Greeting "
            "WHERE ANCESTOR IS :1 "
            "ORDER BY date DESC LIMIT 10",
            guestbook_key(guestbook_name)
            )
            """
        '''
        for greeting in greetings:
            if greeting.author:
                self.response.out.write('<b>%s</b> wrote: ' % greeting.author.nickname())
            else:
                self.response.out.write('wrote:')

            self.response.out.write('<blockquote>%s</blockquote>' % cgi.escape(greeting.content))
            '''

        '''
        self.response.out.write("""
                <form action="/sign?%s" method="post">
                  <div></div>
                  <div><textarea name="content" row="3" conspan="6"></textarea></div>
                  <div><input type="submit" value="sign guestbook" /></div>
                </form>
                <hr />
                <hr />sfssd
                <form>
                  guestbook Name: <input type="text" value="%s" name="guestbook_name" />
                  <input type="submit" value="switch" />
                </form>
              </body>
            </html>
        """ % (urllib.urlencode({'guestbook_name':guestbook_name}), cgi.escape(guestbook_name)))
        '''

        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = "Logout"
            # self.response.out.write('Hello' + user.nickname())
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'login'
            # self.redirect(users.create_login_url(self.request.uri))

        template_values = {
            'greetings' : greetings,
            'url' : url,
            'url_linktext' : url_linktext
        }
        template = jinja_enviroment.get_template('index.html')
        self.response.out.write(template.render(template_values))

class Guestbook(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        guestbook_name = self.request.get('guestbook_name')
        greeting = Greeting(parent = guestbook_key(guestbook_name))

        if user:
            self.response.out.write('<html><body>You wrote:<pre>')
            self.response.out.write(cgi.escape(self.request.get('content')))
            self.response.out.write('</pre></body></html>')

            greeting.author = user
            greeting.content = self.request.get('content')
            greeting.put()
            self.redirect('/?' + urllib.urlencode({'guestbook_name':guestbook_name}))
        else:
            self.redirect(users.create_login_url(self.request.uri))

    def get(self):
        self.redirect('/')

app = webapp2.WSGIApplication([('/', MainHandler),
                               ('/sign', Guestbook)
                               ],
                              debug=True)
