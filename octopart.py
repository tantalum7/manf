
# Library imports
import requests, json


class Octopart(object):

    OCTOPART_URL    = "http://octopart.com/api/v3/parts/search"
    API_KEY         = "d8bd8204"

    @classmethod
    def query(cls, search_term, filters=None):

        # Prepare url (for some reason Octopart doesn't like it when you pass the API key to requests to parse.)
        url = cls.OCTOPART_URL + "?apikey=" + cls.API_KEY

        # Prepare parameters for query
        data = {"queries" : '[{"q":'+str(search_term)+'}]'}

        # Send the request
        resp = requests.get(url, data=data)

        # If the request was successful, return the response json data
        if resp:
            return resp.json()
        else:
            print "Failed"



if __name__ == "__main__":


    print Octopart.query("2n7002")

    print "done"