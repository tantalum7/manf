

import json


from flask import Flask
from flask import make_response
from flask import render_template, redirect
from flask import request
from flask import send_file
from flask import session

from google_auth import GoogleAuth, LoginFailure, LogoutFailure
import httplib2

APPLICATION_NAME = 'Google+ Python Quickstart'


app = Flask(__name__)
app.secret_key = 'abcdefghijklmnopqrstuvwxyz111111'
app.google_auth = GoogleAuth("client_secrets.json")

def BadJsonResponse(data, status_code=401):
    response = make_response(json.dumps(data), status_code)
    response.headers['Content-Type'] = 'application/json'
    return response

def GoodJsonResponse(data, status_code=200):
    response = make_response(json.dumps(data), status_code)
    response.headers['Content-Type'] = 'application/json'
    return response

@app.route('/', methods=['GET'])
def index():

    app.google_auth.start_login()


    return render_template( 'index.html',
                            CLIENT_ID           = app.google_auth.client_id,
                            STATE               = session['auth_state'],
                            APPLICATION_NAME    = "manf-demo1" )

@app.route("/secret")
def secret():

    if app.google_auth.is_authenticated():

        return "You are logged in!"

    else:
        return redirect('/')



@app.route('/signin_button.png', methods=['GET'])
def signin_button():
    """Returns the button image for sign-in."""
    return send_file("templates/signin_button.png", mimetype='image/gif')

@app.route('/connect', methods=['POST'])
def connect():

    try:
        app.google_auth.process_login(request)

    except LoginFailure as failure:
        return BadJsonResponse(failure.reason)

    else:

        if session.get('relogin') is True:
            return GoodJsonResponse('Current user is already connected.')

        else:
            return GoodJsonResponse('Successfully connected user.')

@app.route('/disconnect', methods=['POST'])
def disconnect():
    """Revoke current user's token and reset their session."""
    try:
        app.google_auth.revoke()

    # Catch LogoutFailure error, and return a bad response with the failure reason
    except LogoutFailure as failure:
        return BadJsonResponse(failure.reason)

    # Re-raise any other exceptions
    except:
        raise

    # Log out succeeded, return a good response
    else:
        return GoodJsonResponse("Successfully disconnected.")


if __name__ == '__main__':
    app.debug = True
    app.run(host="localhost", port=4567)