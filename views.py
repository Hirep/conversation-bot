from flaskyBot import app
from flask import render_template
from flask.ext.classy import FlaskView
from forms import *


class IndexView(FlaskView):
	def index(self):
		return "hello"


class FormView(FlaskView):

    def bindex(self):
        form = LoginForm()
        return render_template('index.html', page_title='test', form=form)

    def index(self):
        #    form = ContactForm()
        # return render_template('test.html')
        return "hello"


class TestView(FlaskView):
    pass


IndexView.register(app)
TestView.register(app)
FormView.register(app)
