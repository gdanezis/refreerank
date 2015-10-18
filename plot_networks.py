from extractUKdblp import load_all_data, out_of_institution, rank_digraph, get_stationary_distribution
import networkx as nx
import pygraphviz as pgv
import matplotlib.pyplot as plt

def main():
    (authors_list, authors_map, papers_list, inst_papers_selected, institutions, author_papers, inst_papers, baseline_venue_count) = load_all_data()
    (count_authors, count_inst, count_venues) = out_of_institution(papers_list, authors_map)

    G = rank_digraph(authors_map, inst_papers_selected, author_papers, weighting=False)

    G2 = nx.DiGraph()


    # get rid of weakly connected nodes
    for (u, v) in G.edges():
        w =  G[u][v]['weight']
        w_diff = w
        if G.has_edge(v, u):
            w_diff = w - G[v][u]['weight']
            w +=  G[v][u]['weight']

        if w > 30:
            G2.add_node(u)
            G2.add_node(v)
            if w_diff > 0:
                G2.add_edge(u, v, weight=w_diff)

    # plot hairy ball
    pos=nx.to_agraph(G2)
    pos.layout()
    pos.draw("hairyballs.png")



if __name__ == "__main__":
    main()