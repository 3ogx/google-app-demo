# Google App Doc
----

## Files
#### 文件目录
+ `app.yaml`
+ `main.py`
+ `index.html`
+ `favicon.ico`

## Users
#### 获取当前用户
	from google.appengine.ext import users
	user = users.get_current_user()
	if user:
		self.response.out.write(user.nickname())
	else:
		self.redirect(users.create_login_url(self.request.uri))

## Model
#### 

> from google.appengine.ext import db

	from google.appengine.ext import db
	
	class Greeting(db.Model):
		author = db.UserProperty()
		content = db.StringProperty(multiline = True)
		date = db.DateTimeProperty(auto_now_add = True)
		
## GqlQuery
+ `greetings = db.GqlQuery("select * from Greeting where ANCESTOR is :1 order by date desc limit 10", name)`
	
+ `greetings = Greeting.all().ancestor('name').order('-date)`