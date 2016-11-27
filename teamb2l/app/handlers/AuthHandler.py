import webapp2
import os
import jinja2
import logging
from ..classes.User import User

from google.appengine.ext import ndb

JINJA_ENVIRONMENT = jinja2.Environment(
loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), '..', 'web', 'views')),
extensions=['jinja2.ext.autoescape'],
autoescape=True)

class RegisterHandler(webapp2.RequestHandler):
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('/auth/register.html')
		self.response.write(template.render())
	def post(self):
		email = self.request.get('email')
		password = self.request.get('password')
		confirm_pass = self.request.get('confirm')

		user = User.query(User.email == email).get()

		logging.info(user)

		# if(user == None):
		# 	user = User(email=email, password=password, permission=0)
		# 	user_key = user.put()
		# 	self.response.set_cookie('user', user_key.urlsafe())
		# 	self.redirect('/')
		# else:
		# 	self.redirect('/')
		if user != None:
			template = JINJA_ENVIRONMENT.get_template('/auth/register.html')
			self.response.write(template.render({'errors': ["Error:  Email already taken"]}))
		elif password != confirm_pass:
			template = JINJA_ENVIRONMENT.get_template('/auth/register.html')
			self.response.write(template.render({'errors': ["Error: Passwords do not match"]}))
		else:
			user = User()
			user.email = email
			user.password = password
			user.permission = int(self.request.get('userType'))
			user_key = user.put()
			self.response.set_cookie('user', user_key.urlsafe())
			postMe = """
<html>
<head></head>
	<body style="background-color:rgb(45, 45, 45);">
	<center><img src="/assets/giphy.gif" alt="Check"><br>
	<font color="Gold" style="font-family:Montserrat;">
	 Registration Successful </font></center></body>
	<meta http-equiv="refresh" content="2;url=/">
</html>
			"""
			self.response.write(postMe)

class LoginHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('/auth/login.html')
        self.response.write(template.render())

    def post(self):
        email = self.request.get('email')
        password = self.request.get('password')
        user = User.query(User.email == email, User.password == password).get()

        if user == None:
            template = JINJA_ENVIRONMENT.get_template('/auth/login.html')
            self.response.write(template.render({'errors': ["Error:  Invalid Email or Password."]}))
        else:
            self.response.set_cookie('user', user.key.urlsafe())
            self.redirect('/')

class LogoutHandler(webapp2.RequestHandler):
	def get(self):
		user_cookie = self.request.cookies.get('user')
		if user_cookie == "":
			self.redirect("/")
		else:
			self.response.delete_cookie('user')
			self.redirect("/login")
	def post(self):
		user_cookie = self.request.cookies.get('user')
		if user_cookie == "":
			self.redirect("/")
		else:
			self.response.delete_cookie('user')
			self.redirect("/login")