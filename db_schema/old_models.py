from hashlib import md5
from app import db
from app import app
from werkzeug import generate_password_hash, check_password_hash
#from flask.ext.login import Mixin
import re

class User(db.Model):
    '''minimal'''
    __tablename__='users'
    
    user_id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100), unique = True,nullable=False)
    first_name = db.Column(db.String(100),nullable=False)
    last_name = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(100), unique = True,nullable=False)
    pwdhash = db.Column(db.String(100),nullable=False)
    last_sign_out = db.Column(db.DateTime)

    def __init__(self, username, first_name, last_name, email, password):
        self.username = username
        self.first_name = first_name.title()
        self.last_name = last_name.title()
        self.email = email.lower()
        self.set_password(password)

    def set_password(self, password):
        self.pwdhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)

    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.username)
