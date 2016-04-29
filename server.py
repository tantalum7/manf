

from flask  import Flask, render_template, request
from manf   import Manf
from asset  import AssetNotFoundError

server = Flask(__name__)
manf   = Manf()



@server.route("/")
def hello():
    return "Hello World"

@server.route("/asset")
@server.route("/asset/<id>")
def asset(id):

    try:
        asset = manf.database.get_asset(id)

    except AssetNotFoundError:
        asset = manf.database.create_asset({"_id" : id})

    except:
        raise

    d = asset.get_json()

    return render_template('asset.html', data=asset.get_json())

@server.route("/asset/ajax", methods=['PUT', 'POST'])
def asset_update():
    data = request.get_json()

    asset = manf.database.get_asset(data["_id"])

    if asset:

        for key in data['_keys']:
            asset.set_field(key, data[key])

    return "Good"

@server.route("/index")
def index():

    items = manf.modules.index.list_all(filter={"_type" : "*PART"}, projection=['@part.EPN' ,'@part.COMPONENT_TYPE', '@part.DESCRIPTION'] )

    items = [item['@part'] for item in items]


    return render_template('index.html', items=items)

if __name__ == "__main__":

    server.debug = True
    server.run()


