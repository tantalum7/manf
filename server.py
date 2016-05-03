

from flask  import Flask, render_template, request
from manf   import Manf
from asset  import AssetNotFoundError

server = Flask(__name__)
manf   = Manf()



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
        return render_template( 'asset.html', data=part.get_json() )


@server.route("/part/new")
def new_part():
    return "Make a new part"

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


