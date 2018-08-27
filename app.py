from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
from thirukural import Thirukural
from constants import AppConstants
import logging
import json

app = Flask(__name__)
app.config['ASK_APPLICATION_ID'] = AppConstants.ALEXA_SKILL_ID

kural = Thirukural()

@app.route('/')
def index():
    return 'welcome to Thirukural.'

# Amazon Alexa
alexa = Ask(app, '/')

@alexa.launch
def launched():
    text = render_template('welcome')
    return question(text)

@alexa.intent('AMAZON.HelpIntent')
def help():
    text = render_template('help')
    return question(text)

@alexa.intent('AMAZON.CancelIntent')
@alexa.intent('AMAZON.StopIntent')
def stop():
    text = render_template('cancel')
    return statement(text)

@alexa.intent('Thirukural')
def thirukuralAlexaIntent():
    text = kural.getThirukural()
    speech = text['Translation'] + ". Do you want to know the meaning of that, or read the next."
    session.attributes['kural'] = json.dumps(text)
    return question(speech)

@alexa.intent('Next')
def thirukuralNextAlexaIntent():
    text = kural.getThirukural()
    speech = text['Translation'] + ". Do you want to know the meaning of that, or read the next."
    session.attributes['kural'] = json.dumps(text)
    return question(speech)

@alexa.intent('Detail')
def thirukuralDetailAlexa():
    if 'kural' in session.attributes:
        kural = session.attributes['kural']
        kural = json.loads(kural)
        speech = kural['explanation'] + '. You can say next to know the next kural.'
    else:
        speech = 'You must ask a kural to know about the detail'
    return question(speech)

if __name__ == '__main__':
    app.run(debug=True)