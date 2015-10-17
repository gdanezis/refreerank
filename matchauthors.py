from extractrefdata import ProjectedStrings, parse
from msgpack import unpackb, packb

# extract REF data
ref_inst = parse(field = 0)
ref_title = parse(field = 5)
ref_venue = parse(field = 6)
ref_year = parse(field = 17)

ref_papers = zip(ref_inst, ref_title, ref_venue, ref_year)

# Extract DBLP selected data
dblp_data = file("data/selectfiles.dat", "rb").read()
dblp_data = unpackb(dblp_data)
all_l = len(dblp_data)
