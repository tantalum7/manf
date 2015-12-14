
# Library imports
from flask import Flask

# Project improts
from database   import Database

flask   = Flask(__name__)
#manf    = Manf()

class Manf(object):

    def __init__(self):

        # Init modules
        self.database = Database()


@flask.route("/")
def hello():
    return "Hello World"





if __name__ == "__main__":


    manf = Manf()


