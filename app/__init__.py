import os
from config import basedir
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask_oauth import OAuth
from werkzeug.contrib.fixers import ProxyFix


app = Flask(__name__)
app.config.from_object('config')

app.wsgi_app = ProxyFix(app.wsgi_app)

# Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = "you need to login"
login_manager.session_protection = "basic"




db = SQLAlchemy(app)
oauth = OAuth()
yahoo = oauth.remote_app('yahoo',
        base_url = 'https://fantasysports.yahooapis.com/fantasy/v2/',
        request_token_url = 'https://api.login.yahoo.com/oauth/v2/get_request_token',
        access_token_url = 'https://api.login.yahoo.com/oauth/v2/get_token',
        authorize_url = 'https://api.login.yahoo.com/oauth/v2/request_auth',
        consumer_key = 'dj0yJmk9ZUNVYWFZcW9pRUhBJmQ9WVdrOVZYQnVjbFo2TjJrbWNHbzlNQS0tJnM9Y29uc3VtZXJzZWNyZXQmeD02ZA--',
        consumer_secret = '91096b3d5dfa2045ead373faba062aa6c23c4e23'
        )



from app import views, models
