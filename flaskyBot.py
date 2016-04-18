from flask import Flask
from flask.ext.bootstrap import Bootstrap


app = Flask(__name__)
app.config.from_object('config')
bootstrap = Bootstrap(app)

from views import *

if __name__ == '__main__':
     app.run()