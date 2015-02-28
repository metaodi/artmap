#!/usr/bin/python

# Copyright (c) 2013 Julius Chronak. You can use this source code
# under the terms of the MIT License found in the LICENSE file:
#
# https://raw.github.com/julochrobak/streetscleaner/master/LICENSE

from pprint import pprint

import os.path
import json

sep = ''
with open('output.json', 'w') as out:
    out.write('var elems = {\n')
    out.write(' "type": "FeatureCollection",\n')
    out.write(' "features": [\n')

    for filename in os.listdir('output/'):
        if not filename.endswith(".json"):
            continue

        print(filename)

        with open('output/' + filename) as f:
            try:
                d = json.load(f)
                out.write('\n' + sep)
                json.dump(d, out)
                sep = ','
            except:
                pass
            f.close()
    out.write(' ]}\n')
