from extractrefdata import ProjectedStrings, parse
from msgpack import unpackb, packb
from parse_authors import parse_authors
from itertools import groupby
from collections import Counter
import csv
import re


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

    ref_descriptions = parse(field = 30)
    ref_topics = []
    for descriptor in ref_descriptions:
        topic = re.search("<([0-9]+)>", descriptor)
        if topic is not None:
            ref_topics.append(int(topic.group(1)))
        else:
            ref_topics.append(None)

    ref_papers = sorted(zip(ref_inst, ref_title, ref_venue, ref_year, ref_topics)[1:]) # sort by ref_inst

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


    P = ProjectedStrings(dblp_titles, l = (3,5), n_comp=30)
    P.threshold = 0.3

    matched_papers = {}
    matched_people = {}

    author_list = []
    paper_list = []

    for k, g in groupby(ref_papers, FIRST):
        print
        print k, inst_titles[k]
        matched_papers[k] = [0, 0]
        inst_authors = Counter()
        for inst, titl, venu, yr, topic in g:
            matched_papers[k][0] += 1
            #if len(list(P.matches(titl))) == 0:
            #    unmatched_papers[k][1] += 1
            matches_flag = list(P.matches(titl))
            if len(matches_flag) > 0:
                matched_papers[k][1] += 1
                paper_list.append((k, titl, dblp_data[matches_flag[0][0]]))
            #print ">", titl
            for i, mx, title in matches_flag:
                #matched_papers[k][1] += 1
                #print "(%2.2f) %s" % (mx, title)
                #print ", ".join(dblp_data[i][0])
                inst_authors.update(dblp_data[i][0])
            #print

        diverse_names = sum([diversify_name(a) for a in inst_authors], [])
        just_names = [n1 for n1, _ in diverse_names]

        Pauths = ProjectedStrings(just_names, l=(1,3),  n_comp=30)
        Pauths.threshold = 0.45

        matched_people[k] = [0, 0]
        for _, surname, initials in author_map[k]:
            matched_people[k][0] += 1
            # Normalize a bit
            surname1 = surname.lower().translate(None, ' .-,').strip()
            initials1 = initials.lower().translate(None, ' .-,').strip()
            new_name = initials1 + " " + surname1
            matches = sorted(list(Pauths.matches(new_name, k=5)), key=lambda x:x[1], reverse=True)

            # Find a way to break high-ties
            strong_matches = [(idx, mx * inst_authors[diverse_names[idx][1]], diverse_names[idx][1]) for (idx, mx, name) in matches if mx > 0.40]
            strong_matches = [(idx, mx, name) for (idx, mx, name) in strong_matches if mx > 0.55]
            strong_matches = sorted(strong_matches, key=lambda x:x[1], reverse=True)

            if len(strong_matches) > 0:
                matched_people[k][1] += 1
                author_list.append((k, "%s %s" % (initials, surname), strong_matches[0][2]))
                print "%2.2f | %s %s | %s" % (strong_matches[0][1], initials, surname, strong_matches[0][2])
            else:
                print "%s | %s %s | %s" % ("***", initials, surname, "")
                print matches

    print "Packing data"
    packed_authors = packb(author_list, use_bin_type=True)
    file("data/author_list.dat", "wb").write(packed_authors)

    packed_papers = packb(paper_list, use_bin_type=True)
    file("data/paper_list.dat", "wb").write(packed_papers)

    fo = open("results/match_quality.txt", "w")
    print  >>fo, "People and Papers matched"
    for k, (v1, v2) in matched_people.iteritems():
        (m1, m2) = matched_papers[k]
        print >> fo, "%2.2f%% | %2.2f%% | %s" % ( 100* float(v2) / float(v1), 100* float(m2) / float(m1), inst_titles[k])
    # print inst_authors

        #print
        #print k, inst_titles[k]
        #print inst_authors
        #for a in inst_authors:
        #   print diversify_name(a)
        #print ["%s %s" % (a, b) for _, b, a in author_map[k]]
            #print titl, list(P.matches(titl))

if __name__ == "__main__":
    test_main()
