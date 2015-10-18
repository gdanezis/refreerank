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

        if w > 5:
            G2.add_node(u)
            G2.add_node(v)
            if w_diff > 0:
                G2.add_edge(u, v, weight=w_diff)

    G3 = nx.DiGraph()


    for n in G2.nodes():
        out_edges = sorted(G2.out_edges(n), key=lambda x: G2[x[0]][x[1]]['weight'], reverse=True)[:1]
        for (u, v) in out_edges:
            G3.add_node(u)
            G3.add_node(v)
            G3.add_edge(u, v, weight=G2[u][v]['weight'])


    G5 = G3.copy()

    for n in G3.nodes():
        in_edges = G3.in_edges(n)
        in_weight = 0
        for (u1, v1) in in_edges:
            in_weight += G3[u1][v1]['weight']
        out_edges = G3.out_edges(n)
        out_weight = 0
        for (u2, v2) in out_edges:
            out_weight += G3[u2][v2]['weight']
        if 3*out_weight < in_weight:
            G5.remove_edges_from(out_edges)

    G4 = G5.to_undirected()


    components = nx.connected_components(G4)
    for i, comp in enumerate(components):
        if len(comp) > 2:

            Gi = G5.subgraph(comp)
            # plot hairy ball
            pos=nx.to_agraph(Gi)
            pos.graph_attr['size']='10,10!'
            pos.graph_attr['ratio']='fill'
            pos.layout(prog='neato')
            pos.draw("hairyballs_%s.png" % i)
            print i



if __name__ == "__main__":
    main()