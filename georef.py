from lxml import etree
from pprint import pprint
import requests
import time
import random
import json

tree = etree.parse("MetadataGugelmann.xml")
total = 0
results = []
limit = 10

location_words = [
    'im',
    'in',
    'bei',
    'um',
    'vor',
    'auf'
]

continue_words = [
    'der',
    'die',
    'dem'
]

def ask_nominatim(candidate, the_one):
    print "Candidate: %s" % candidate        
    if not candidate[0].isupper():
        return the_one
    r = requests.get('https://nominatim.openstreetmap.org/search?countrycodes=CH&format=json&q=' + candidate)
    time.sleep(1)
    try:
        geo = r.json()[0]
        if geo['importance'] > 0.3 and (the_one is None or geo['importance'] > the_one['importance']):
            return geo
    except:
        pass
    return the_one


rec_arr = []
for record in tree.findall('record'):
    rec_arr.append(record)

# make a random selection from the input
index = range(0, len(rec_arr))
random.shuffle(index)

for idx in index:
    record = rec_arr[idx]
    if total >= limit:
        break
    candidate = None
    the_one = None
    words = []
    total += 1
    descr = record.find('TitelName')
    if descr is not None:
        words = descr.text.split(' ')

    for i, candidate in enumerate(words):
        the_one = ask_nominatim(candidate, the_one)
        if the_one is None and i > 0:
            the_one = ask_nominatim(words[i-1] + ' ' + candidate, the_one)
        if the_one is None and i < len(words)-1:
            the_one = ask_nominatim(candidate + ' ' + words[i+1], the_one)
        if the_one is None and i > 0:
            the_one = ask_nominatim(candidate + ' ' + words[i-1], the_one)
        if the_one is None and i < len(words)-1:
            the_one = ask_nominatim(words[i+1] + ' ' + candidate, the_one)


    if the_one is not None:
        gmetry = {}
        gmetry['type'] = "Point"
        gmetry['coordinates'] = [ float(the_one['lat']), float(the_one['lon']) ]

        props = {}
        props['name'] = descr.text
        props['location'] = the_one['display_name']

        geores = {}
        geores['type'] = "Feature"
        geores['geometry'] = gmetry
        geores['properties'] = props

        results.append(geores)
        print "FOUND: %s: %s" % (props['name'], props['location'])
    else:
        print "NOT FOUND: %s" % (descr.text)


with open('output.geojson', 'w') as outfile:
    json.dump(results, outfile)

print "Total: %s" % total
print "Matches: %s" % len(results)
