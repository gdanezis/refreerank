import csv
import numpy as np
import hashlib
from struct import unpack
import random


cache = {}
def hash(x, length=1024):
    try:
        return cache[x]
    except:
        h = unpack("I", hashlib.md5(x).digest()[:4])[0] % length
        cache[x] = h
        return h
    pass

def fingerprint(data, l=(5,10), length=1024):
    data = data.lower().translate(None, '\r\n\t')
    f = np.zeros(length, dtype=bool)
    for i in range(len(data)):
        for lx in range(l[0], l[1]):
            f[hash(data[i:i+lx], length)] = True
    return f


def fingerprints(data_strings, l=(5,10), length=1024):
    fings = []
    for d in data_strings:
        fings += [ fingerprint(d, l, length) ]

    return np.vstack(fings).astype(int)


def parse():
    titles = []
    with open('data/REF2014Data.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            x = row[5].lower().translate(None, '\r\n\t') # 5 = title
            # x = x.decode('utf8', 'ignore')
            titles += [ x ]
    return titles


def match(x1, x2):
    return np.float(np.sum(x1 * x2)) / np.sum(x2 | x1)


def test_many_fingerprints():
    datas = parse()
    Fs = fingerprints(datas)

    # Select a random target
    target_i = random.choice(range(len( datas )))
    target = datas[target_i]
    Tf = fingerprint(target)

    from time import clock
    # Compare all
    start = clock()
    for _ in xrange(10):
        matches = np.dot(Fs, np.transpose(Tf))
        new_i = np.argmax(matches)
    end = clock()
    print "Timing: %2.5f" % ((end - start) / 10.0)

    assert datas[new_i] == datas[target_i]
    assert matches[target_i] > matches[target_i-1]

def test_kdtree():

    from sklearn.neighbors import KDTree
    from time import clock

    datas = parse()
    Fs = fingerprints(datas)
    tree = KDTree(Fs, leaf_size=20)

    # Select a random target
    target_i = random.choice(range(len( datas )))
    target = datas[target_i]
    Tf = fingerprint(target)

    # Match it
    start = clock()
    for _ in xrange(10):
        dist, ind = tree.query(Tf.astype(int), k=3)
        # print ind, target_i
    end = clock()
    print "Timing: %2.5f" % ((end - start) / 10.0)

    assert datas[ind[0][0]] == datas[target_i]


def test_kdtree_projection():

    from sklearn.neighbors import KDTree
    from sklearn import random_projection
    from time import clock

    datas = parse()
    Fs = fingerprints(datas)

    # The random projection
    transformer = random_projection.GaussianRandomProjection(n_components = 128)
    Fs_new = transformer.fit_transform(Fs)
    print Fs_new.shape

    tree = KDTree(Fs_new, leaf_size=20)

    # Select a random target
    target_i = random.choice(range(len( datas )))
    target = datas[target_i]
    Tf = np.vstack([fingerprint(target)])
    Tf_new = transformer.transform(Tf)

    # Match it
    start = clock()
    for _ in xrange(10):
        dist, ind = tree.query(Tf_new.astype(int), k=3)
        # print ind, target_i
    end = clock()
    print "Timing: %2.5f" % ((end - start) / 10.0)

    assert datas[ind[0][0]] == datas[target_i]


def test_kdtree_accuracy():

    from sklearn.neighbors import KDTree
    from sklearn import random_projection
    from time import clock

    datas = parse()
    Fs = fingerprints(datas)

    # The random projection
    components = range(1, 50, 1)
    for comp in components:
        transformer = random_projection.GaussianRandomProjection(n_components = comp)
        Fs_new = transformer.fit_transform(Fs)
        #print Fs_new.shape

        tree = KDTree(Fs_new, leaf_size=20)
        times = []
        correct = []
        correct2 = []

        for _ in range(1000):
            # Select a random target
            target_i = random.choice(range(len( datas )))
            target = datas[target_i]
            Tf = np.vstack([fingerprint(target)])
            Tf_new = transformer.transform(Tf)

            # Match it
            start = clock()
            #for _ in xrange(10):
            dist, ind = tree.query(Tf_new.astype(int), k=10)
                # print ind, target_i
            end = clock()
            times.append(end-start)
            correct.append(datas[ind[0][0]] == datas[target_i])
            correct2.append(target_i in ind[0])

        #pretty print
        print "Componenets: %d Time: %2.5f, Accuracy: %2.5f, Accuracy: %2.5f" % (comp, np.mean(times), np.mean(correct), np.mean(correct2))
            #print "Timing: %2.5f" % ((end - start) / 10.0)

    #assert datas[ind[0][0]] == datas[target_i]

def test_match_many():

    from sklearn.neighbors import KDTree
    from time import clock

    datas = parse()
    Fs = fingerprints(datas)
    tree = KDTree(Fs, leaf_size=20)

    # Select a random target
    target_i = random.choice(range(len( datas )))
    targets = Fs[target_i:target_i+10, :]
    print targets.shape

    # Match it
    start = clock()
    for _ in xrange(10):
        dist, ind = tree.query(targets, k=1)
        # print ind, target_i
    end = clock()
    print "Timing: %2.5f" % ((end - start) / 10.0)

    assert datas[ind[0][0]] == datas[target_i]


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

    random.shuffle(ftitles)

    xx = ftitles[0][1]
    #print "Match: ", ftitles[0][0]


   #for a, b in sorted(((match(f, xx), t) for (t, f) in ftitles), reverse=True):
        #print "%2.2f %s" % (a,b)
