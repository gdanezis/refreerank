from extractrefdata import *
from contextlib import contextmanager
from time import clock
import pytest
slowtest = pytest.mark.slowtest

@pytest.fixture
def datas():
    parsed_data = parse()
    return parsed_data


@contextmanager
def timer(reps):
    start = clock()
    yield
    end = clock()
    print "Timing: %2.5f" % ((end - start) / float(reps))


@slowtest
def test_many_fingerprints(datas):
    Fs = fingerprints(datas)

    # Select a random target
    target_i = random.choice(range(len( datas )))
    target = datas[target_i]
    Tf = fingerprint(target)

    #from time import clock
    # Compare all
    with timer(10):
        for _ in xrange(10):
            matches = np.dot(Fs, np.transpose(Tf))
            new_i = np.argmax(matches)

    assert datas[new_i] == datas[target_i]
    assert matches[target_i] > matches[target_i-1]

def test_kdtree(datas):

    from sklearn.neighbors import KDTree

    Fs = fingerprints(datas)
    tree = KDTree(Fs, leaf_size=20)

    # Select a random target
    target_i = random.choice(range(len( datas )))
    target = datas[target_i]
    Tf = fingerprint(target)

    # Match it
    with timer(10):
        for _ in xrange(10):
            dist, ind = tree.query(Tf, k=3)

    assert datas[ind[0][0]] == datas[target_i]


def test_kdtree_projection(datas):

    from sklearn.neighbors import KDTree
    from sklearn import random_projection


    # datas = parse()
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
    with timer(10):
        for _ in xrange(10):
            dist, ind = tree.query(Tf_new, k=3)
    assert datas[ind[0][0]] == datas[target_i]

@slowtest
def test_kdtree_accuracy(datas):

    from sklearn.neighbors import KDTree
    from sklearn import random_projection

    Fs = fingerprints(datas)

    # The random projection
    components = range(1, 20, 1)
    for comp in components:
        transformer = random_projection.GaussianRandomProjection(n_components = comp)
        Fs_new = transformer.fit_transform(Fs)


        tree = KDTree(Fs_new, leaf_size=20)
        times = []
        correct = []
        correct2 = []

        for _ in range(100):
            # Select a random target
            target_i = random.choice(range(len( datas )))
            target = datas[target_i]
            Tf = np.vstack([fingerprint(target)])
            Tf_new = transformer.transform(Tf)

            # Match it
            start = clock()
            dist, ind = tree.query(Tf_new, k=3)

            end = clock()
            times.append(end-start)
            correct.append(datas[ind[0][0]] == datas[target_i])
            correct2.append(target_i in ind[0])

        #pretty print
        print "Componenets: %d Time: %2.5f, Accuracy: %2.5f, Accuracy: %2.5f" % (comp, np.mean(times), np.mean(correct), np.mean(correct2))

@slowtest
def test_distance(datas):
    from sklearn.neighbors import KDTree
    from sklearn import random_projection

    Fs = fingerprints(datas)

    # The random projection
    transformer = random_projection.GaussianRandomProjection(n_components = 7)
    Fs_new = transformer.fit_transform(Fs)
    print Fs_new.shape

    tree = KDTree(Fs_new, leaf_size=20)

    # Select a random target
    correct = []
    wrong = []

    for _ in range(100):
        target_i = random.choice(range(len( datas )))
        target_j = random.choice(range(len( datas )))

        # target i
        target = datas[target_i]
        Tf = np.vstack([fingerprint(target)])
        Tf_new = transformer.transform(Tf)


        # target j
        target2 = datas[target_j]
        Tf2 = np.vstack([fingerprint(target2)])
        Tf_new2 = transformer.transform(Tf2)


        # Match it
        start = clock()
        dist, ind = tree.query(Tf_new.astype(int), k=1)
        dist2, ind2 = tree.query(Tf_new2.astype(int), k=1)

        correct.append(match(Fs[ind[0][0]], Tf[0]))
        wrong.append(match(Fs[ind2[0][0]], Tf[0]))
        end = clock()


    print "Correct: %2.5f (%2.5f), Random: %2.5f (%2.5f)" % (np.mean(correct), np.std(correct), np.mean(wrong), np.std(wrong))



def test_match_many(datas):

    from sklearn.neighbors import KDTree
    from time import clock

    # datas = parse()
    Fs = fingerprints(datas)
    tree = KDTree(Fs, leaf_size=20)

    # Select a random target
    target_i = random.choice(range(len( datas )))
    targets = Fs[target_i:target_i+10, :]
    print targets.shape

    # Match it
    with timer(10):

        for _ in xrange(10):
            dist, ind = tree.query(targets, k=1)


    assert datas[ind[0][0]] == datas[target_i]

def test_match_class(datas):

    p = ProjectedStrings(datas)

    # Select a random target
    target_i = random.choice(range(len( datas )))
    target = datas[target_i]

    # Time
    with timer(10):

        for _ in xrange(10):
            _, _, matched_target = list(p.matches(target))[0]


    assert target == matched_target


def test_simple_match():
    x1 = fingerprint("HORNET: High-speed Onion Routing at the Network Layer.")
    x2 = fingerprint("HORNET High-speed xdx Routing Network Layer.")
    x3 = fingerprint("Centrally Banked Cryptocurrencies onion")

    assert match(x1, x2) > match(x1, x3)

def test_match_all(datas):
    ftitles = []
    for t in datas:
        ftitles += [(t, fingerprint(t))]

    random.shuffle(ftitles)

    xx = ftitles[0][1]
