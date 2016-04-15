from flaskyBot import app
from flask import render_template
from flask.ext.classy import FlaskView
from forms import *


class IndexView(FlaskView):
    route_base = '/'
    def index(self):
        form = LoginForm()
        if form.validate_on_submit():
            return 'Form successfully submited!'
        return render_template("index.html", page_title= 'test', form= form)


IndexView.register(app)
