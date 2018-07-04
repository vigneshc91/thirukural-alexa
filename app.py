from flask import Flask
from flask_assistant import Assistant, tell, ask
from flask_assistant import context_manager
from flask_ask import Ask, statement, question, session
from thirukural import Thirukural
from constants import AppConstants
import logging
import json

app = Flask(__name__)
app.config['ASSIST_ACTIONS_ON_GOOGLE'] = True
app.config['ASK_APPLICATION_ID'] = AppConstants.ALEXA_SKILL_ID
logging.getLogger('flask_assistant').setLevel(logging.DEBUG)
assist = Assistant(app, route='/')
ask = Ask(app, '/')

kural = Thirukural()

@app.route('/')
def index():
    return 'welcome to Thirukural.'

# Google Assistant
@assist.action('welcome')
def hello_world():
    speech = 'Welcome to thirukural, You can ask for a thirukural'
    return ask(speech)

@assist.action('thirukural')
def thirukuralIntent():
    text = kural.getThirukural()
    speech = text['Translation'] + ". Do you want to know the meaning of that or read the next."
    context_manager.set('kural-detail', 'kural', json.dumps(text))
    return ask(speech)

@assist.action('next')
def thirukuralNextIntent():
    text = kural.getThirukural()
    speech = text['Translation'] + ". Do you want to know the meaning of that or read the next."
    context_manager.set('kural-detail', 'kural', json.dumps(text))
    return ask(speech)

@assist.action('detail')
def thirukuralDetail():
    kural = context_manager.get('kural-detail').get('kural')
    kural = json.loads(kural)
    speech = kural['explanation']
    return ask(speech)

# Amazon Alexa
@ask.launch
def launched():
    text = render_template('welcome')
    return question(text)

@ask.intent('AMAZON.HelpIntent')
def help():
    text = render_template('help')
    return question(text)

@ask.intent('AMAZON.CancelIntent')
@ask.intent('AMAZON.StopIntent')
def stop():
    text = render_template('cancel')
    return statement(text)

@ask.intent('thirukural')
def thirukuralAlexaIntent():
    text = kural.getThirukural()
    speech = text['Translation'] + ". Do you want to know the meaning of that or read the next."
    session.attributes['kural'] = json.dumps(text)
    return question(speech)

@ask.intent('next')
def thirukuralNextAlexaIntent():
    text = kural.getThirukural()
    speech = text['Translation'] + ". Do you want to know the meaning of that or read the next."
    session.attributes['kural'] = json.dumps(text)
    return question(speech)

@ask.intent('detail')
def thirukuralDetailAlexa():
    if 'kural' in session.attributes:
        kural = session.attributes['kural']
        kural = json.loads(kural)
        speech = kural['explanation']
    else:
        speech = 'You must ask a kural to know about the detail'
    return question(speech)

if __name__ == '__main__':
    app.run(debug=True)