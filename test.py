"""
Eulerian circuits and graphs.
"""
from itertools import combinations

import networkx as nx

from ..utils import arbitrary_element, not_implemented_for

__all__ = [
    "is_eulerian",
    "eulerian_circuit",
    "eulerize",
    "is_semieulerian",
    "has_eulerian_path",
    "eulerian_path",
]


def is_eulerian(G):

    if G.is_directed():

        return all(
            G.in_degree(n) == G.out_degree(n) for n in G
        ) and nx.is_strongly_connected(G)

    return all(d % 2 == 0 for v, d in G.degree()) and nx.is_connected(G)



def is_semieulerian(G):

    return has_eulerian_path(G) and not is_eulerian(G)



def _find_path_start(G):
    """Return a suitable starting vertex for an Eulerian path.

    If no path exists, return None.
    """
    if not has_eulerian_path(G):
        return None

    if is_eulerian(G):
        return arbitrary_element(G)

    if G.is_directed():
        v1, v2 = (v for v in G if G.in_degree(v) != G.out_degree(v))
        # Determines which is the 'start' node (as opposed to the 'end')
        if G.out_degree(v1) > G.in_degree(v1):
            return v1
        else:
            return v2

    else:
        # In an undirected graph randomly choose one of the possibilities
        start = [v for v in G if G.degree(v) % 2 != 0][0]
        return start


def _simplegraph_eulerian_circuit(G, source):
    if G.is_directed():
        degree = G.out_degree
        edges = G.out_edges
    else:
        degree = G.degree
        edges = G.edges
    vertex_stack = [source]
    last_vertex = None
    while vertex_stack:
        current_vertex = vertex_stack[-1]
        if degree(current_vertex) == 0:
            if last_vertex is not None:
                yield (last_vertex, current_vertex)
            last_vertex = current_vertex
            vertex_stack.pop()
        else:
            _, next_vertex = arbitrary_element(edges(current_vertex))
            vertex_stack.append(next_vertex)
            G.remove_edge(current_vertex, next_vertex)


def _multigraph_eulerian_circuit(G, source):
    if G.is_directed():
        degree = G.out_degree
        edges = G.out_edges
    else:
        degree = G.degree
        edges = G.edges
    vertex_stack = [(source, None)]
    last_vertex = None
    last_key = None
    while vertex_stack:
        current_vertex, current_key = vertex_stack[-1]
        if degree(current_vertex) == 0:
            if last_vertex is not None:
                yield (last_vertex, current_vertex, last_key)
            last_vertex, last_key = current_vertex, current_key
            vertex_stack.pop()
        else:
            triple = arbitrary_element(edges(current_vertex, keys=True))
            _, next_vertex, next_key = triple
            vertex_stack.append((next_vertex, next_key))
            G.remove_edge(current_vertex, next_vertex, next_key)


def eulerian_circuit(G, source=None, keys=False):

    if not is_eulerian(G):
        raise nx.NetworkXError("G is not Eulerian.")
    if G.is_directed():
        G = G.reverse()
    else:
        G = G.copy()
    if source is None:
        source = arbitrary_element(G)
    if G.is_multigraph():
        for u, v, k in _multigraph_eulerian_circuit(G, source):
            if keys:
                yield u, v, k
            else:
                yield u, v
    else:
        yield from _simplegraph_eulerian_circuit(G, source)



def has_eulerian_path(G, source=None):

    if nx.is_eulerian(G):
        return True

    if G.is_directed():
        ins = G.in_degree
        outs = G.out_degree
        # Since we know it is not eulerian, outs - ins must be 1 for source
        if source is not None and outs[source] - ins[source] != 1:
            return False

        unbalanced_ins = 0
        unbalanced_outs = 0
        for v in G:
            if ins[v] - outs[v] == 1:
                unbalanced_ins += 1
            elif outs[v] - ins[v] == 1:
                unbalanced_outs += 1
            elif ins[v] != outs[v]:
                return False

        return (
            unbalanced_ins <= 1 and unbalanced_outs <= 1 and nx.is_weakly_connected(G)
        )
    else:
        # We know it is not eulerian, so degree of source must be odd.
        if source is not None and G.degree[source] % 2 != 1:
            return False

        # Sum is 2 since we know it is not eulerian (which implies sum is 0)
        return sum(d % 2 == 1 for v, d in G.degree()) == 2 and nx.is_connected(G)



def eulerian_path(G, source=None, keys=False):

    if not has_eulerian_path(G, source):
        raise nx.NetworkXError("Graph has no Eulerian paths.")
    if G.is_directed():
        G = G.reverse()
        if source is None or nx.is_eulerian(G) is False:
            source = _find_path_start(G)
        if G.is_multigraph():
            for u, v, k in _multigraph_eulerian_circuit(G, source):
                if keys:
                    yield u, v, k
                else:
                    yield u, v
        else:
            yield from _simplegraph_eulerian_circuit(G, source)
    else:
        G = G.copy()
        if source is None:
            source = _find_path_start(G)
        if G.is_multigraph():
            if keys:
                yield from reversed(
                    [(v, u, k) for u, v, k in _multigraph_eulerian_circuit(G, source)]
                )
            else:
                yield from reversed(
                    [(v, u) for u, v, k in _multigraph_eulerian_circuit(G, source)]
                )
        else:
            yield from reversed(
                [(v, u) for u, v in _simplegraph_eulerian_circuit(G, source)]
            )



@not_implemented_for("directed")
def eulerize(G):

    if G.order() == 0:
        raise nx.NetworkXPointlessConcept("Cannot Eulerize null graph")
    if not nx.is_connected(G):
        raise nx.NetworkXError("G is not connected")
    odd_degree_nodes = [n for n, d in G.degree() if d % 2 == 1]
    G = nx.MultiGraph(G)
    if len(odd_degree_nodes) == 0:
        return G


    odd_deg_pairs_paths = [
        (m, {n: nx.shortest_path(G, source=m, target=n)})
        for m, n in combinations(odd_degree_nodes, 2)
    ]


    Gp = nx.Graph()
    for n, Ps in odd_deg_pairs_paths:
        for m, P in Ps.items():
            if n != m:
                Gp.add_edge(m, n, weight=1 / len(P), path=P)


    best_matching = nx.Graph(list(nx.max_weight_matching(Gp)))

    # duplicate each edge along each path in the set of paths in Gp
    for m, n in best_matching.edges():
        path = Gp[m][n]["path"]
        G.add_edges_from(nx.utils.pairwise(path))
    return G
