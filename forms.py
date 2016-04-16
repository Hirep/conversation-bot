from flask_wtf import Form
from wtforms import StringField, PasswordField


class ContactForm(Form):
    name = StringField("Name of student")


class LoginForm(Form):
    username = StringField('username')
    password = PasswordField('password')

