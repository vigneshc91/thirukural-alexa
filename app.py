from flask import Flask
from flask_assistant import Assistant, tell, ask
from flask_assistant import context_manager
from thirukural import Thirukural
import logging


app = Flask(__name__)
app.config['ASSIST_ACTIONS_ON_GOOGLE'] = True
logging.getLogger('flask_assistant').setLevel(logging.DEBUG)
assist = Assistant(app, route='/')

kural = Thirukural()

@assist.action('welcome')
def hello_world():
    speech = 'Welcome to thirukural, You can ask for a thirukural'
    return ask(speech)

@assist.action('thirukural')
def thirukuralIntent():
    text = kural.getThirukural()
    speech = text['Translation']
    return ask(speech)

@assist.action('next')
def thirukuralNextIntent():
    text = kural.getThirukural()
    speech = text['Translation']
    return ask(speech)

if __name__ == '__main__':
    app.run(debug=True)