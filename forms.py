# -*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class NameForm(Form):
    name = StringField(u'Як Вас звати?', validators=[DataRequired()])
    submit = SubmitField(u'Ок')

class AskForm(Form):
    query = StringField(u'Можливо середньовічну казку чи наукову фантастику?', validators=[DataRequired()])
    submit = SubmitField(u'Шукати')

class ContactForm(Form):
    name = StringField("Name of student")

class LogForm(Form):
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)
