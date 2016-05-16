

from flask  import Flask, render_template, request, session, g
from manf   import Manf
from asset  import AssetNotFoundError
from common_html    import html

from common_html    import html
from google_auth    import LoginFailure, LogoutFailure
from manf   import Manf
from util_funcs     import GoodJsonResponse, BadJsonResponse, GenerateRandomCharString
from time import time
import sys

# Prepare server instance
server = Flask(__name__)
server.secret_key = GenerateRandomCharString(32)

# Prepare manf instance
if "angela" in sys.argv:
    manf    = Manf(db_addr=("localhost", 27027)) # We're running on angela server, DB is local not remote
else:
    manf    = Manf()

class RequiresAuthentication(object):

    def __init__(self, f):
        self.f = f
        self.__name__ = f.__name__

    def __call__(self, *args, **kwargs):

        if manf.auth.is_authenticated():
            return self.f()
        else:
            return "Can't access this page, login first (decorator)"


@server.before_request
def before_request():
    g.request_start_time = time()

@server.teardown_request
def teardown_request(execption):
    if g.get('request_start_time'):
        duration = (time() - g.request_start_time) * 1000
        if duration > manf.settings.request_time_warning:
            server.logger.warning("Slow request [{}] : {}ms".format(request.path, duration))

@server.route("/")
def hello():
    return "Hello World"

@server.route("/part/epn/<epn>")
def part(epn):

    try:
        part = manf.factory.fetch_part(epn)

    except manf.NotFoundError:
        return "Cannot find part "+str(epn)

    except:
        raise

    else:
        obj = part.get_dict()
        return render_template( 'part.html', data=part.get_json(), data_obj=part.get_dict(), constants=manf.constants.get_dict(), html=html )

@server.route("/part/new")
def new_part():
    return "Make a new part"


@server.route("/part/list")
def part_list():

    part_list = manf.database.find_many(filter={'_type':'*PART'}, projection=['@part']).as_list()

    return render_template('part_list.html', data=part_list, html=html)

@server.route("/part/ajax/update", methods=["PUT", "POST"])
def part_update():

    try:
        data = request.get_json()
        part = manf.factory.create_part(id=data['_id'])
        part.dict_update(data)

    except:
        raise

    return "stuff"






@server.route("/bom/name/<name>")
def bom(name):

    try:
        bom = manf.factory.fetch_bom(name)

    except manf.NotFoundError:
        return "Cannot find bom "+str(name)

    except:
        raise

    else:
        rtn_string = """<table border="1px">
                          <tr><td>NAME</td><td>{}</td></tr>
                          <tr><td>DESCRIPTION</td><td>{}</td></tr>
                          <tr><td>REVISION</td><td>{}</td></tr>
                          <tr><td>ID</td><td>{}</td></tr>
                          <tr><td> </td></tr>
                          <tr><td> </td></tr>
                          <tr><td> </td></tr>
                          <tr><td>REF</td><td>VALUE</td><td>EPN</td><td>MANUFACTURER</td><td>MPN</td>
                    """.format(bom.name, bom.description, bom.revision, bom.id)

        data = bom.data

        if data:
            for item in data:
                part = manf.factory.create_part(id=item['DB_ID'])
                rtn_string += "<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(item['REF'], item['VALUE'], part.EPN, part.manufacturer, part.MPN)

        return rtn_string + "</table>"

@server.route("/bom/list")
def bom_list():

    bom_list = manf.database.find_many(filter={"_type":"*BOM"}, projection=["@bom"]).as_list()

    return render_template('bom_list.html', data=bom_list, html=html)

@server.route("/asset/ajax", methods=['PUT', 'POST'])
def asset_update():
    data = request.get_json()

    asset = manf.database.get_asset(data["_id"])

    if asset:

        for key in data['_keys']:
            asset.set_field(key, data[key])

    return "Good"

@server.route("/login")
def login():

    if not manf.auth.is_authenticated():
        manf.auth.start_login()
        print "Local state: {}".format(session.get("auth_state"))
        return render_template("login.html", CLIENT_ID=manf.auth.client_id, STATE=session.get("auth_state"))

    else:
        return "Already logged in buddy"

@server.route("/login/ajax/connect", methods=['POST'])
def login_connect():

    try:
        manf.auth.process_login(request)

    except LoginFailure as failure:
        print failure.reason
        return BadJsonResponse(failure.reason)

    else:

        if session.get('relogin') is True:
            return GoodJsonResponse('Current user is already connected.')

        else:
            return GoodJsonResponse('Successfully connected user.')

@server.route("/logout")
def logout():
    return logout_disconnect()

@server.route("/logout/ajax/disconnect", methods=['POST'])
def logout_disconnect():
    """Revoke current user's token and reset their session."""
    try:
        manf.auth.revoke()

    # Catch LogoutFailure error, and return a bad response with the failure reason
    except LogoutFailure as failure:
        return BadJsonResponse(failure.reason)

    # Re-raise any other exceptions
    except:
        raise

    # Log out succeeded, return a good response
    else:
        return GoodJsonResponse("Successfully disconnected.")

@server.route("/secret")
@RequiresAuthentication
def secret():
    return "This is a secret page"

@server.route("/index")
def index():

    items = manf.modules.index.list_all(filter={"_type" : "*PART"}, projection=['@part.EPN' ,'@part.COMPONENT_TYPE', '@part.DESCRIPTION'] )

    items = [item['@part'] for item in items]


    return render_template('index.html', items=items)

if __name__ == "__main__":

    server.debug = True

    if "angela" in sys.argv:
        server.run(host="45.58.35.135", port=80) # We're running on angela server, server has external IP on port 80
    else:
        server.run(host="localhost", port=4567)
