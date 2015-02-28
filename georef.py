from lxml import etree
from pprint import pprint

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

for record in tree.findall('record'):
    candidate = None
    total += 1
    descr = record.find('TitelName')
    if descr is not None:
        words = descr.text.split(' ')
        if len(filter(set(words).__contains__, location_words)) > 0: # high confidence
            cont = False
            for i, word in enumerate(words):
                if (word in location_words) or cont:
                    try:
                        if (words[i+1] in continue_words):
                            cont = True
                            continue
                        candidate = words[i+1]
                        break
                    except IndexError:
                        cont = False
                        continue
        else: # low confidence
            pass
            # pprint(descr.text)
    if candidate is not None:
        print "Candidate: %s" % candidate        

print "Total: %s" % total
print "Matches: %s" % matches
