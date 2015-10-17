from extractrefdata import ProjectedStrings, parse
from msgpack import unpackb, packb
import random

# Get the REF data
datas = parse()
dates = parse(field=17)
p = ProjectedStrings(datas)

dblp_data = file("data/allfiles.dat", "rb").read()
dblp_data = unpackb(dblp_data)
all_l = len(dblp_data)

# Select a random target
#target_i = random.choice(range(len( datas )))
#target = datas[target_i]

# Time
old = 0
new_dblp_list = []
print "starting ..."
for l, (authors, title, booktitle, year) in enumerate(dblp_data):
    m = list(p.matches(title, k=2))
    if m == []:
        continue

    if old < 100 * l / all_l:
        old = 100 * l / all_l
        print "%s%%" % (100 * l / all_l)
        #break

    for idx, mx, tit in m:
        frac = float(100 * l) / all_l
        if mx > 0.50: # mx > 0.0:
            new_dblp_list += [(authors, title, booktitle, year)]
            break

print "saving ..."
packed_data = packb(new_dblp_list, use_bin_type=True)
file("data/selectfiles.dat", "wb").write(packed_data)
print "done."

    #if frac > 2:
    #    break