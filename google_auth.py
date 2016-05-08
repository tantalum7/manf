
# Library imports
import json, random, string
from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError, Credentials
import requests
import httplib2
from flask import session



class _AuthFailure(Exception):
    def __init__(self, code=None, reason=None):
        self.reason = reason
        self.code = code
        session.pop('auth_state', None)
        session.pop('auth_cred_json', None)
        session.pop('auth_gplus_id', None)
        session.pop('auth_relogin', None)

class LoginFailure(_AuthFailure):
    pass

class LogoutFailure(_AuthFailure):
    pass

class NotLoggedInError(Exception):
    pass

class BadCredentialsError(Exception):
    pass


class GoogleAuth(object):

    class RequiresAuthentication(object):
        def __init__(self, f):
            self.f = f
            self.__name__ = f.__name__

        def __call__(self, *args, **kwargs):
            return self.f()

    def __init__(self, client_secrets_json):

        # Init class vars
        self._client_secrets_json = client_secrets_json
        self.client_id = json.loads(open(client_secrets_json, 'r').read())['web']['client_id']

    def start_login(self):
        # Create random state variable to prevent request forgery (server will return it)
        session['auth_state'] = self._generate_random_state_key()

    def process_login(self, response, scope=''):

        try:
            # Upgrade the authorization code into a credentials object
            oauth_flow = flow_from_clientsecrets(self._client_secrets_json, scope=scope)
            oauth_flow.redirect_uri = 'postmessage'
            credentials = oauth_flow.step2_exchange(response.data)

        # Catch flow exchange error and re-raise as generic login failure error
        except FlowExchangeError:
            raise LoginFailure(reason="Failed to upgrade the authorization code")

        # Push any other exception further up
        except:
            raise

        else:
            # Fetch local and remote state variables
            remote_state    = response.args.get('state')
            local_state     = session.get("auth_state", " ")

            # If local and remote state variables don't match, raise a LoginFailure error
            if local_state != remote_state:
                raise LoginFailure( reason="Local state ({}) does not match remote state ({})".format(local_state,
                                                                                                     remote_state) )

            # If the user was already logged in, set the relogin flag true
            if session.get('auth_gplus_id') == credentials.id_token['sub']:
                session['auth_relogin'] = True

            # Grab login data and store in session dict
            session['auth_gplus_id']    = credentials.id_token['sub']
            session['auth_cred_json']   = credentials.to_json()

    def revoke(self):

        # Try and get credentials from session
        try:
            credentials = self._get_credentials_from_session()

        # Catch bad credentials error, and raise as a logout failure
        except BadCredentialsError as error:
            raise LogoutFailure(reason=error.message)

        # Catch not logged in error, and raise as logout failure
        except NotLoggedInError:
            raise LogoutFailure(reason="Not logged in")

        # Found good credentials
        else:
            # Send the request to revoke authentication
            result = requests.get( credentials.revoke_uri, params={'token' : credentials.access_token} )

            # Wipe session auth data
            self._wipe_session_auth_data()

            # If the request failed, then raise a LogoutFailure error
            if not result:
                raise LogoutFailure(code=result.status_code, reason=result.text)

    def is_authenticated(self):

        # Attempt to authorise a http request object
        try:
            http = httplib2.Http()
            http = self._get_credentials_from_session().authorize(http)

        # Catch any of the various login failures, wipe session auth data and return false
        except (AccessTokenRefreshError, NotLoggedInError, BadCredentialsError) as error:
            self._wipe_session_auth_data()
            return False

        # Re-raise other exceptions
        except:
            raise

        # Http request object authorise succeeded, user is still authenticated
        else:
            return True


    def _generate_random_state_key(self):
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))

    def _get_credentials_from_session(self):

        # If we can't find the credentials json, then we are probably not logged in
        if session.get('auth_cred_json') is None:
            raise NotLoggedInError()

        # Try and parse credentials json from session
        try:
            credentials = Credentials.new_from_json(session.get("auth_cred_json"))

        # Catch value error (couldn't parse json), and raise a LogoutFailure error
        except ValueError as error:
            raise BadCredentialsError(message=error.message)

        # Managed to fetch and parse the credentials object from json correctly, return the object
        else:
            return credentials

    def _wipe_session_auth_data(self):
        print "Wiping session auth data"
        #session.pop('auth_state', None)
        session.pop('auth_cred_json', None)
        session.pop('auth_gplus_id', None)
        session.pop('auth_relogin', None)