import csv
import numpy as np
import hashlib
from struct import unpack


cache = {}
def hash(x, length=1024):
    try:
        return cache[x]
    except:
        h = unpack("I", hashlib.md5(x).digest()[:4])[0] % length 
        cache[x] = h
        return h


def fingerprint(data, l=(5,10), length=1024):
    data = data.lower().translate(None, '\r\n\t')
    f = np.zeros(length, dtype=bool)
    for i in range(len(data)):
        for lx in range(l[0], l[1]):
            f[hash(data[i:i+lx], length)] = True
    return f


def parse():
    titles = []
    with open('data/REF2014Data.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            x = row[8].lower().translate(None, '\r\n\t') # 5 = title
            # x = x.decode('utf8', 'ignore')
            titles += [ x ]
    return titles


def match(x1, x2):
    return np.float(np.sum(x1 * x2)) / np.sum(x2 | x1)


def test_simple_match():
    x1 = fingerprint("HORNET: High-speed Onion Routing at the Network Layer.")
    x2 = fingerprint("HORNET High-speed xdx Routing Network Layer.")
    x3 = fingerprint("Centrally Banked Cryptocurrencies onion")

    assert match(x1, x2) > match(x1, x3)

def test_match_all():
    ftitles = []
    for t in parse():
        # print t
        ftitles += [(t, fingerprint(t))]

    import random
    random.shuffle(ftitles)

    xx = ftitles[0][1]
    print "Match: ", ftitles[0][0]


    for a, b in sorted(((match(f, xx), t) for (t, f) in ftitles), reverse=True):
        print "%2.2f %s" % (a,b)
