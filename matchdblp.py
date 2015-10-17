from extractrefdata import ProjectedStrings, parse
from msgpack import unpackb
import random

# Get the REF data
datas = parse()
p = ProjectedStrings(datas)

dblp_data = file("data/allfiles.dat", "rb").read()
dblp_data = unpackb(dblp_data)
all_l = len(dblp_data)

# Select a random target
#target_i = random.choice(range(len( datas )))
#target = datas[target_i]

# Time
for l, (authors, title, booktitle, year) in enumerate(dblp_data):
    m = list(p.matches(title))
    if m == []:
        continue

    idx, mx, tit = m[0]
    frac = float(100 * l) / all_l
    print "> (%2.2f) %2.2f" % (mx, frac)
    print "%s" % title
    print "%s" % tit
    print

    if frac > 2:
        break
