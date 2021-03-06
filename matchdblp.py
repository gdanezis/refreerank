from extractrefdata import ProjectedStrings, parse
from msgpack import unpackb, packb
import random
from collections import defaultdict

# Get the REF data
datas = parse()
dates = parse(field=17)
p = ProjectedStrings(datas, l=(3, 5))
p.threshold = 0.30

dblp_data = file("data/allfiles.dat", "rb").read()
dblp_data = unpackb(dblp_data)
all_l = len(dblp_data)

venue_stats = defaultdict(int)

# Time
old = 0
new_dblp_list = []
print "starting ..."
for l, (authors, title, booktitle, year) in enumerate(dblp_data):

    # Gather some generic statistics about the venue_stats
    if 2009 <= int(year) <= 2014:
        venue_stats[booktitle] += 1

    m = list(p.matches(title, k=10))
    if m == []:
        continue

    # Print a progress meter
    if old < 100 * l / all_l:
        old = 100 * l / all_l
        print "%s%%" % (100 * l / all_l)

    # Select the record if it matches a REF title
    for idx, mx, tit in m:
        frac = float(100 * l) / all_l
        if mx > 0.35: # mx > 0.0:
            new_dblp_list += [(authors, title, booktitle, year)]
            break

print "saving ..."

packed_data = packb(new_dblp_list, use_bin_type=True)
file("data/selectfiles.dat", "wb").write(packed_data)

packed_data = packb(dict(venue_stats), use_bin_type=True)
file("data/venuestats.dat", "wb").write(packed_data)

print "done."
