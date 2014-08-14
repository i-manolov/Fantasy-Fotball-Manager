from flask_wtf import Form
from wtforms import TextField, BooleanField, TextAreaField, PasswordField, SubmitField, validators
from app.models import User


class LoginForm(Form):
    username = TextField('Username', validators=[validators.Required()])
    password = PasswordField('Password',validators=[validators.Required("Please enter a password.")])
    submit = SubmitField("Submit")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        '''custom validator methods for LoginForm. used in views.py
        form.validate_on_submit()'''
        if not Form.validate(self):
            return False
        user = User.query.filter_by(user_name = self.username.data.lower()).first()
        if user and user.check_password(self.password.data):
            return True
        else:
            self.password.errors.append("invalid password")

class SignUpForm(Form):
    username = TextField('Username', validators=[validators.Regexp(r'^[a-z0-9_-]{3,16}$', message = "Username must be 3 to 16 characters long")])
    first_name = TextField('First name', validators=[validators.Length(min =4 , max = 25, message = "Firstname must be 4 to 25 characters long")])
    last_name = TextField('Last Name', validators=[validators.Length(min =4 , max = 25, message = "Lastname must be 4 to 25 characters long")])
    email = TextField('Email', validators=[validators.Regexp(r'^([a-z0-9_\.-]+)@([\da-z\.-]+)\.([a-z\.]{2,6})$' ,message = "Not a valid email address")])
    password = PasswordField('Password', validators=[validators.Regexp(r'^[a-z0-9_-]{3,18}$' ,message = "Password must be 3 to 18 characters long" )])
    submit = SubmitField("Submit")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False
        # check if email is taken and if password is correct
        email = User.query.filter_by(email = self.email.data.lower()).first()

        username = User.query.filter_by(user_name = self.username.data.lower()).first()
        if email:
            self.email.errors.append("That email is already taken")
        if username:
            self.username.errors.append("This username is already taken")
        else:
            return True


class ChangePasswordForm(Form):
    username = TextField('Username', validators=[validators.Required()])
    password= PasswordField('NewPassword', validators=[validators.Regexp(r'^[a-z0-9_-]{3,18}$' ,message = "Password must be 3 to 18 characters long" )])
    submit=SubmitField("Submit",validators=[validators.Required()])
    
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
    
    
    def validate (self):
        if not Form.validate(self):
            return False 
        
        user = User.query.filter_by(user_name=self.username.data.lower()).first()
        
        if user :
            
            return ("Succesfully updated")
        
        else:
            self.password.errors.append(" Not able to update password")

















        
