from lxml import etree
from pprint import pprint
import requests
import time
import random

tree = etree.parse("MetadataGugelmann.xml")
total = 0
matches = 0

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

# get 10 random index from 0 to len(rec_arr)
index = range(0, len(rec_arr))
random.shuffle(index)

for idx in index:
    record = rec_arr[idx]
    if total >= 100:
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
        print "Found match %s for %s" % (the_one['display_name'], descr.text)
        matches += 1
    else:
        print "NO match found for %s" % (descr.text)


print "Total: %s" % total
print "Matches: %s" % matches
