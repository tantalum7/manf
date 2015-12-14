

from flask  import Flask, render_template, request
from manf   import Manf


server = Flask(__name__)
manf   = Manf()



@server.route("/")
def hello():
    return "Hello World"

@server.route("/asset")
@server.route("/asset/<id>")
def asset(id):
    return render_template('asset.html', id=9)

@server.route("/asset/ajax", methods=['PUT'])
def asset_update():
    data = request.get_json()

    asset = manf.database.query(data["_id"], 1)

    if not asset:
        #asset = manf.database.c
        pass

        for key in data['_keys']:
            asset.set_field(key, data[key])

    return "Good"

if __name__ == "__main__":

    server.debug = True
    server.run()


