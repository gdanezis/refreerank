from itertools import groupby
from collections import defaultdict, Counter

from msgpack import unpackb, packb
from matchauthors import parse_institutions

import numpy as np
import networkx as nx

# Open the UK authors and papers
def load_all_data():
    # (inst, ref_author, dblp_author)
    authors_list = unpackb(file("data/author_list.dat", "rb").read())
    authors_map = dict((name, inst) for inst, _, name in authors_list)
    # print authors_map

    # (inst, ref_title, dblpentry)
    papers_list = sorted(unpackb(file("data/paper_list.dat", "rb").read()))

    inst_papers_selected = {}
    for inst, g in groupby(papers_list, key=lambda x:x[0]):
        inst_papers_selected[inst] = {}

        for _,_,(authors, title, booktitle, year) in g:
            for a in authors:
                if a in authors_map and authors_map[a] == inst:
                    # Check we have this author
                    if a not in inst_papers_selected[inst]:
                        inst_papers_selected[inst][a] = []

                    inst_papers_selected[inst][a] += [(authors, title, booktitle, year)]


    # Extract all other papers from UK authors.
    dblp_data = file("data/allfiles.dat", "rb").read()
    dblp_data = unpackb(dblp_data)
    all_l = len(dblp_data)

    # Pretty names for institutions
    institutions = parse_institutions("data/Institution.csv")
    author_papers = defaultdict(list)
    inst_papers = defaultdict(list)

    baseline_venue_count = Counter()
    for authors, title, booktitle, year in dblp_data:
        for a in authors:
            if a in authors_map:
                # Check in
                inst_papers[authors_map[a]] += [ (tuple(authors), title, booktitle, year) ]
                author_papers[a] += [(tuple(authors), title, booktitle, year)]
                baseline_venue_count.update([booktitle])

    return (authors_list, authors_map, papers_list, inst_papers_selected, institutions, author_papers, inst_papers, baseline_venue_count)

# Out of institution statistics
def out_of_institution(papers_list, authors_map):
    count_authors = Counter()
    count_inst = Counter()
    count_venues = Counter()
    for (inst,_,(authors, _, venue, _)) in papers_list:
        count_venues.update([venue])
        for a in authors:
            if a in authors_map and authors_map[a] != inst:
                count_authors.update([a])
                count_inst.update([authors_map[a]])

    return (count_authors, count_inst, count_venues)

def rank_digraph(authors_map, inst_papers_selected, author_papers):

    G = nx.DiGraph()

    # The directed graph approach
    for author, inst in authors_map.iteritems():
        # No papers from this author found :-(
        if author not in inst_papers_selected[inst]:
            continue

        # Otherwise list the venues selected
        included_venues = []
        included_papers = set()
        for (_, title, venue, _) in inst_papers_selected[inst][author]:
            included_papers.add(title)
            included_venues += [venue]
            G.add_node(venue)

        not_included_venues = []
        for (_, title, venue, _) in author_papers[author]:
            if title in included_papers:
                continue

            if venue not in included_venues:
                not_included_venues += [venue]
                G.add_node(venue)

        if len(not_included_venues) * len(included_venues) == 0:
            continue

        w = 1.0 / (len(not_included_venues) * len(included_venues))
        for source in not_included_venues:
            for destination in included_venues:
                if G.has_edge(source, destination):
                    G[source][destination]['weight'] += w # 1.0
                else:
                    G.add_edge(source, destination)
                    G[source][destination]['weight'] = w # 1.0

    return G


def get_stationary_distribution(G):
    all_nodes = G.nodes()
    node_map = dict((n,i) for i, n in enumerate(all_nodes))

    matrix = np.zeros((len(all_nodes), len(all_nodes)))

    for n1, n2 in G.edges():
        matrix[node_map[n1], node_map[n2]] = G[n1][n2]['weight']


    norm = np.sum(matrix, axis=1)
    norm[norm == 0.0] = 1.0
    norm = np.array([norm]).transpose()
    matrix = matrix.astype(float) / norm

    ones = np.sum(matrix, axis=1)
    ones[np.isnan(ones)] = 0.0
    dist = ones / np.sum(ones)

    for _ in range(50):
        dist = dist.dot(matrix)

    return (all_nodes, dist)

def main():
    (authors_list, authors_map, papers_list, inst_papers_selected, institutions, author_papers, inst_papers, baseline_venue_count) = load_all_data()
    (count_authors, count_inst, count_venues) = out_of_institution(papers_list, authors_map)

    G = rank_digraph(authors_map, inst_papers_selected, author_papers)
    (all_nodes, dist) = get_stationary_distribution(G)

    # Institutions lists by papers used by other institutions

    frankothers = file("data/rank_institution_by_others.txt", "w")
    print >>frankothers, "Rank Institutions by number of papers used by *others* in the REF"
    for inst, cnt in count_inst.most_common():
        # if inst is not None:
        print >>frankothers, "%3d %s" % (cnt, institutions[inst])

    print

    # List venues by a ratio of ref / accepted
    lst = []
    for venue, cnt in count_venues.most_common():
        # if inst is not None:
        if baseline_venue_count[venue] > 0:
            lst += [((float(cnt) * 100 / baseline_venue_count[venue], venue))]
            # print "%2.2f %s" % (float(cnt) * 100 / baseline_venue_count[venue], venue)

    frankvenratio = file("data/rank_venue_by_ref_paper_ratio.txt", "w")
    print >>frankvenratio, "Rank venues by ratio of REF submitted papers vs. available papers"
    for cnt, venue in sorted(lst, reverse=True):
        if baseline_venue_count[venue] > 4:
            print >>frankvenratio, "%2.2f %3d %s" % (cnt, count_venues[venue], venue)



    frankvenratio = file("data/rank_venue_stationary.txt", "w")
    print >>frankvenratio, "Rank venues by the rank of the stationary distribution in the selection graph"
    venues = sorted([(ni, dist[i]) for i, ni in enumerate(all_nodes)], reverse=True, key=lambda x:x[1])
    for venue, cnt in venues:
        if cnt > 0.0:
            print >>frankvenratio, "%2.2f %s" % (1000 * cnt, venue)

    # Score institutions by quality-research mass
    venues_juice = dict(venues)
    inst_juice_by_author = defaultdict(float)
    for a in author_papers:
        for authors, title, booktitle, year in author_papers[a]:
            if booktitle in venues_juice:
                inst_juice_by_author[authors_map[a]] += (venues_juice[booktitle] / len(authors)) / len(inst_papers_selected[inst])


    frankvenratio = file("data/rank_institution_stationary.txt", "w")
    print >>frankvenratio, "Rank institutions by the rank of the stationary distribution in the selection graph of the venues their staff publish"
    for i, inst in enumerate(sorted(institutions, reverse=True, key=lambda inst: inst_juice_by_author[inst])):
        print >>frankvenratio,"%4d %2.5f %s" % (i, inst_juice_by_author[inst] , institutions[inst])

if __name__ == "__main__":
    main()
