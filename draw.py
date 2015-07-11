from __future__ import print_function, division
import networkx as nx
import d3py


def giant_component(g):
    return max(nx.connected_component_subgraphs(g), key=len)


def make_nx_graph(profiles):
    g = nx.Graph()
    for link in profiles:
        g.add_node(link)
    for link, profile in profiles.items():
        for target_link in profile.links:
            g.add_edge(link, target_link)
    return g


def draw_nx_d3(g):
    with d3py.NetworkXFigure(g, width=1000, height=1000) as p:
        p += d3py.ForceLayout()
        p.show()


def profiles_to_json(profiles, path):
    data = {}
    data['nodes'] = []
    ordered_links = []
    for link, profile in profiles.items():
        in_path = link in path
        is_source = link == path[-1]
        is_target = link == path[0]
        data['nodes'].append({'name': link,
                              'in_path': in_path,
                              'is_source': is_source,
                              'is_target': is_target})
        ordered_links.append(link)
    data['links'] = []
    path_edges = []
    for i in range(len(path) - 1):
        source_i = ordered_links.index(path[i])
        target_i = ordered_links.index(path[i + 1])
        path_edges.append((source_i, target_i))
    non_redundant_edges = []
    for source_link, source_profile in profiles.items():
        source_i = ordered_links.index(source_link)
        for target_link in source_profile.links:
            target_i = ordered_links.index(target_link)
            edge = (source_i, target_i)
            if edge[::-1] not in non_redundant_edges:
                non_redundant_edges.append(edge)
    for edge in non_redundant_edges:
        in_path = edge in path_edges or edge[::-1] in path_edges
        data['links'].append({'source': edge[0], 'target': edge[1],
                              'in_path': in_path})
    return data
