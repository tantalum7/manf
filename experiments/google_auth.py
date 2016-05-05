
# Library imports
import json, random, string
from apiclient.discovery import build
from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

class LoginFailure(Exception):
    def __init__(self, code=None, reason=None):
        self.reason = reason
        self.code   = code

class GoogleAuth(object):

    def __init__(self, client_secrets_json):

        # Init class vars
        self._client_secrets_json = client_secrets_json
        self.client_id = json.loads(open(client_secrets_json, 'r').read())['web']['client_id']
        self._service   = build('plus', 'v1')

    def start_login(self, session_dict):
        # Create random state variable to prevent request forgery (server will return it)
        session_dict['state'] = self._generate_random_state_key()

    def process_login(self, session_dict, post_data, scope=None):

        try:
            # Upgrade the authorization code into a credentials object
            oauth_flow = flow_from_clientsecrets(self._client_secrets_json, scope='')
            oauth_flow.redirect_uri = 'postmessage'
            credentials = oauth_flow.step2_exchange(post_data)

        # Catch flow exchange error and re-raise as generic login falure error
        except FlowExchangeError:
            raise LoginFailure(code=401, reason="Failed to upgrade the authorization code")

        # Push any other exception further up
        except:
            raise

        else:
            # If the user was already logged in, set the relogin flag true
            if session_dict.get('gplus_id') == credentials.id_token['sub']:
                session_dict['relogin'] = True

            # Grab login data and store in session dict
            session_dict['gplus_id']    = credentials.id_token['sub']
            #session_dict['credentials'] = credentials


    def _generate_random_state_key(self):
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))