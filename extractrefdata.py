import csv
import hashlib
from struct import unpack
import random

import numpy as np

from sklearn.neighbors import KDTree
from sklearn import random_projection

cache = {}
def hash(x):
    try:
        return cache[x]
    except:
        h = unpack("I", hashlib.md5(x).digest()[:4])[0]
        cache[x] = h
        return h
    pass

def process_string(s):
    data = s.lower().translate(None, ',.: -\r\n\t')
    return data


def fingerprint(data, l=(5,6), length=1024):
    # data = data.lower().translate(None, ' -\r\n\t')
    # data = data.strip(",.")
    data = process_string(data)

    f = np.zeros(length, dtype=bool)
    for i in range(len(data)):
        for lx in range(l[0], l[1]):
            f[hash(data[i:i+lx]) % length] = True
    return f


def fingerprints(data_strings, l=(5,6), length=1024):
    fings = []
    for d in data_strings:
        fings += [ fingerprint(d, l, length) ]

    return np.vstack(fings).astype(int)


def parse(name = 'data/REF2014Data.csv', field = 5):
    titles = []
    with open(name, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            x = row[field]
            # x = process_string(x)

            titles += [ x ]
    return titles


def match(x1, x2):
    return np.float(np.sum(x1 * x2)) / np.sum(x2 | x1)


class ProjectedStrings(object):
    def __init__(self, strings, l=(5,6), n_comp=7):
        self.l = l
        self.datas = strings
        self.fingers = fingerprints(self.datas, l=self.l)
        self.transformer = random_projection.GaussianRandomProjection(n_components = n_comp)
        self.projected_fingers = self.transformer.fit_transform(self.fingers)
        self.kdtree = KDTree(self.projected_fingers, leaf_size=20)

        # Experimentally determined
        self.threshold = 0.15 + 5 * 0.05

    def matches(self, target, k=10):
        f = fingerprint(target, l=self.l)
        target_finger = np.vstack([f])
        target_projected_finger = self.transformer.transform(target_finger)
        _, ind = self.kdtree.query(target_projected_finger, k=k)

        for i in ind[0]:
            mx = match(self.fingers[i], f)
            if  mx > self.threshold:
                yield (i, mx, self.datas[i])
