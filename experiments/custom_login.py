

import json


from flask import Flask
from flask import make_response
from flask import render_template
from flask import request
from flask import send_file
from flask import session

from google_auth import GoogleAuth, LoginFailure
import httplib2

APPLICATION_NAME = 'Google+ Python Quickstart'


app = Flask(__name__)
app.secret_key = 'abcdefghijklmnopqrstuvwxyz111111'


@app.route('/', methods=['GET'])
def index():

    app.google_auth.start_login(session)

    response = make_response(
        render_template('index.html',
                        CLIENT_ID=app.google_auth.client_id,
                        STATE=session['state'],
                        APPLICATION_NAME="manf-demo1"))
    response.headers['Content-Type'] = 'text/html'
    return response

@app.route('/signin_button.png', methods=['GET'])
def signin_button():
    """Returns the button image for sign-in."""
    return send_file("templates/signin_button.png", mimetype='image/gif')

@app.route('/connect', methods=['POST'])
def connect():
    """Exchange the one-time authorization code for a token and
    store the token in the session."""
    # Ensure that the request is not a forgery and that the user sending
    # this connect request is the expected user.
    if request.args.get('state', '') != session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Normally, the state is a one-time token; however, in this example,
    # we want the user to be able to connect and disconnect
    # without reloading the page.  Thus, for demonstration, we don't
    # implement this best practice.
    # del session['state']

    try:
        app.google_auth.process_login(session, request.data)

    except LoginFailure as failure:

        response = make_response( json.dumps(failure.reason), failure.code )
        response.headers['Content-Type'] = 'application/json'
        return response

    else:

        if session.get('relogin') is True:
            response = make_response(json.dumps('Current user is already connected.'),
                                 200)
            response.headers['Content-Type'] = 'application/json'
            return response

        else:
            response = make_response(json.dumps('Successfully connected user.'), 200)
            response.headers['Content-Type'] = 'application/json'
            return response


@app.route('/disconnect', methods=['POST'])
def disconnect():
    """Revoke current user's token and reset their session."""

    # Only disconnect a connected user.
    credentials = session.get('credentials')
    if credentials is None:
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Execute HTTP GET request to revoke current token.
    access_token = credentials.access_token
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        # Reset the user's session.
        del session['credentials']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/people', methods=['GET'])
def people():
    """Get list of people user has shared with this app."""
    credentials = session.get('credentials')
    # Only fetch a list of people for connected users.
    if credentials is None:
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    try:
        # Create a new authorized API client.
        http = httplib2.Http()
        http = credentials.authorize(http)
        # Get a list of people that this user has shared with this app.
        google_request = SERVICE.people().list(userId='me', collection='visible')
        result = google_request.execute(http=http)

        response = make_response(json.dumps(result), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    except AccessTokenRefreshError:
        response = make_response(json.dumps('Failed to refresh access token.'), 500)
        response.headers['Content-Type'] = 'application/json'
        return response


if __name__ == '__main__':
    app.google_auth = GoogleAuth("client_secrets.json")
    app.debug = True
    app.run(host="localhost", port=4567)