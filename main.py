from flask import Flask
import os

from flask import Flask, request
from twilio.twiml.voice_response import Gather, VoiceResponse, Say
from twilio.rest import Client

app = Flask(__name__)

# Twilio credentials
account_sid = os.environ.get('sid')
auth_token = os.environ.get('auth_token')
twilio_number = os.environ.get('my_num')

# Route for the voice webhook
@app.route('/voice', methods=['POST'])
def voice():
    response = VoiceResponse()

    # Gather DTMF input
    gather = Gather(num_digits=1, action='/gather')
    gather.say("Press 1 for option one, or press 2 for option two.")
    response.append(gather)

    return str(response)

# Route for the gather webhook
@app.route('/gather', methods=['POST'])
def gather():
    response = VoiceResponse()

    # Check DTMF input
    digit = request.form['Digits']
    if digit == '1':
        response.say("You pressed option one.")
    elif digit == '2':
        response.say("You pressed option two.")
    else:
        response.say("Invalid input. Please try again.")

    return str(response)

# Route to initiate the call
@app.route('/')
def call():
    # Get the phone number to call
    phone_number = "+919518575475"

    client = Client(account_sid, auth_token)

    # Make the call
    call = client.calls.create(
        url=request.host_url + 'voice',
        to=phone_number,
        from_=twilio_number
    )

    return "Call initiated to {}".format(phone_number)


if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)
