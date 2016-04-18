from flaskyBot import app
from flask import render_template, redirect, url_for
from flask.ext.classy import FlaskView
from forms import *

str_name = "давай підберемо Вам щось почитати!"
str_noname = "Привіт! Мене звати Муркі, а Вас як?"
name = None


@app.route('/', methods=['GET', 'POST'])
def index():
    global name
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        return redirect(url_for('ask'))
    return render_template('index.html', form=form, str_noname=str_noname)


@app.route('/ask', methods=['GET', 'POST'])
def ask():
    query = None
    form = AskForm()
    if form.validate_on_submit():
        query = form.query.data
        form.query.data = ''
        return redirect(url_for('result'))
    return render_template('ask.html', form=form, str_name="{}, {}".format(name, str_name))


@app.route('/result', methods=['GET', 'POST'])
def result():
    return """
        <h1> Вітаю, я нічого не знайшов, але все працює як треба!</h1>

    """

class ErrorHandlerView(FlaskView):

    @app.errorhandler(404)
    def page_not_found(self):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(self):
        return render_template('500.html'), 500

ErrorHandlerView.register(app)
