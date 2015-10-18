from itertools import groupby
from collections import defaultdict, Counter

from msgpack import unpackb, packb
from matchauthors import parse_institutions

# Open the UK authors and papers

# (inst, ref_author, dblp_author)
authors_list = unpackb(file("data/author_list.dat", "rb").read())
authors_map = dict((name, inst) for inst, _, name in authors_list)
# print authors_map

# (inst, ref_title, dblpentry)
papers_list = sorted(unpackb(file("data/paper_list.dat", "rb").read()))

inst_papers_selected = {}
for inst, g in groupby(papers_list, key=lambda x:x[0]):
    inst_papers_selected[inst] = [(tuple(authors), title, booktitle, year) for _,_,(authors, title, booktitle, year) in g]

# Extract all other papers from UK authors.
dblp_data = file("data/allfiles.dat", "rb").read()
dblp_data = unpackb(dblp_data)
all_l = len(dblp_data)

# Pretty names for institutions
institutions = parse_institutions("data/Institution.csv")

inst_papers = defaultdict(list)
for authors, title, booktitle, year in dblp_data:
    # if any((a in authors_map) for a in authors):
    #    pass
    for a in authors:
        if a in authors_map:

            # Check in
            #inst = authors_map[a]
            #if inst not in inst_papers:
            #    inst_papers[inst] = []

            inst_papers[authors_map[a]] += [ (tuple(authors), title, booktitle, year) ]

# Some silly statistics
count_authors = Counter()
count_inst = Counter()
for (inst,_,(authors, _, _, _)) in papers_list:
    for a in authors:
        if a in authors_map and authors_map[a] != inst:
            count_authors.update([a])
            count_inst.update([authors_map[a]])

for author, cnt in count_authors.most_common():
    inst = ""
    if author in authors_map:
        inst = "(%s)" % institutions[authors_map[author]]
    # if inst is not None:
    print "%3d %s %s" % (cnt, author, inst)

print

for inst, cnt in count_inst.most_common():
    # if inst is not None:
    print "%3d %s" % (cnt, institutions[inst])
