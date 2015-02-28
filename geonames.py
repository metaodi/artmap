import overpass
from pprint import pprint

api = overpass.API()

def check_municipality(candidate):
    return api.Get("node['name'='Salt Lake City']")

