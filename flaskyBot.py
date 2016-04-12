from flask import Flask
from flask.ext.classy import FlaskView


quotes = [
    "A noble spirit embiggens the smallest man! ~ Jebediah Springfield",
    "If there is a way to do it better... find it. ~ Thomas Edison",
    "No one knows what he can do till he tries. ~ Publilius Syrus"
]

app = Flask(__name__)

class QuotesView(FlaskView):
    def index(self):
        return "<br>".join(quotes)
        
    def get(self, id):
        print("here")
        id = int(id)
        if id < len(quotes) - 1:
            return quotes[id]
        else:
            return "Not Found", 404

QuotesView.register(app)

if __name__ == '__main__':
    app.run()