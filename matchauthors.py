from extractrefdata import ProjectedStrings, parse
from msgpack import unpackb, packb
from parse_authors import parse_authors
from itertools import groupby
from collections import Counter
import csv


def parse_institutions(name):
    inst_title = {}
    with open(name, "r") as f:
        parser = csv.reader(f)
        for row in parser:
            inst_title[row[0]] = row[1]
    return inst_title


FIRST = lambda x: x[0]

def diversify_name(name):
    cleaned_name = name.lower().translate(None, ',.-0123456789').strip()
    parsed_name = cleaned_name.split(" ")
    diverse_names = []
    for i in range(len(parsed_name)):
        initials = parsed_name[:i]
        try:
            initials = "".join([x[0] for x in initials])
        except:
            print "whoops!", name
            initials = ""
        full_names = parsed_name[i:]
        diverse_name = " ".join([initials] + full_names)
        diverse_names.append((diverse_name, name))
    return diverse_names

def test_main():
    # extract REF data
    ref_inst = parse(field = 0)
    ref_title = parse(field = 5)
    ref_venue = parse(field = 6)
    ref_year = parse(field = 17)

    ref_papers = sorted(zip(ref_inst, ref_title, ref_venue, ref_year)[1:]) # sort by ref_inst

    # Extract DBLP selected data
    dblp_data = file("data/selectfiles.dat", "rb").read()
    dblp_data = unpackb(dblp_data)
    dblp_titles = [title for (authors, title, booktitle, year) in dblp_data]
    all_l = len(dblp_data)

    # inst titles
    inst_titles = parse_institutions("data/Institution.csv")

    # Extract ref author data
    author_data = sorted(parse_authors("data/Staff.csv"))
    author_map = {}
    for k, g in groupby(author_data, FIRST):
        author_map[k] = list(g)


    P = ProjectedStrings(dblp_titles)
    for k, g in groupby(ref_papers, FIRST):
        print k
        inst_authors = Counter()
        for inst, titl, venu, yr in g:
            for i, _, _ in P.matches(titl):
                inst_authors.update(dblp_data[i][0])

                
        print
        print k, inst_titles[k]
        #print inst_authors
        for a in inst_authors:
           print diversify_name(a)
        print ["%s %s" % (a, b) for _, b, a in author_map[k]]
            #print titl, list(P.matches(titl))

if __name__ == "__main__":
    test_main()