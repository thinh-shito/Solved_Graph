import pandas as pd
import streamlit as st
import networkx as nx



def __init__( vertices, tmp_matrix):
    V = vertices # No. of vertices
    graph =[]
    Edge = tmp_matrix.keys()

    for i in tmp_matrix.keys():
        for j in tmp_matrix[i].keys():
            graph.append((i, j, tmp_matrix[i][j]))

def find( parent, i):
    # print(parent[i])
    # print(i,"   ", parent[i])
    if parent[i] != i:
        parent[i] = find(parent, parent[i])
    return parent[i]


def union( parent, rank, x, y):
    if rank[x] < rank[y]:
        parent[x] = y
    elif rank[x] > rank[y]:
        parent[y] = x
    else:
        parent[y] = x
        rank[x] += 1

def solve(graph):
    edges = []
    nodes = graph.nodes
    for i in nodes:
        for j in nodes:
            try:
                edges.append((i, j, graph[i][j]['weight']))
            except:
                continue
    edges = sorted(edges, key=lambda item: item[2])
    # G, edge_label, edge_color = graph
    i = 0
    e = 0
    parent = {}
    rank = {}
    result = []
    for node in nodes:
        parent[node] = node
        rank[node] = 0
    # print(parent)
    while len(result) < len(nodes) - 1:
        u, v, w = edges[i]
        # print(u,v,w,i)
        i = i + 1
        x = find(parent, u)
        y = find(parent, v)
        if x != y:
            e = e + 1
            result.append((u,v))
            union(parent, rank, x, y)
    return result


# Driver's code
if __name__ == '__main__':

    tmp_matrix ={}
    tmp_matrix.update({'a':{'b':2, 'd':6}})
    tmp_matrix.update({'b' : {'a':2,'c':3, 'd':8, 'e':5}})
    tmp_matrix.update({'c' : {'b':3, 'e': 7}})
    tmp_matrix.update({'d' : {'a':6, 'b': 8, 'e':9}})
    tmp_matrix.update({'e' : {'b':5, 'c':7, 'd':9}})
    ################################
    v = ['a','b','c','d','e']

    graph = nx.DiGraph()
    graph.add_nodes_from(v)
    for u, v_list in tmp_matrix.items():
        for v,w in v_list.items():
            graph.add_edge(u, v,weight =  w, color = 'b')
    print(graph.edges())
