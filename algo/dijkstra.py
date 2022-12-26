
import networkx as nx
import pandas as pd

################################
# tmp_matrix ={'0':{'1':2.5,'2':2.0,'3':2.1},
#                 '1':{'0':2.5,'4':1.0},
#                 '2':{'0':2.0,'4':0.6,'5':1.5},
#                 '3':{'0':2.1,'5':2.5},
#                 '4':{'1':1.0,'2':0.6},
#                 '5':{'3':2.5,'2':1.5},
#                 }
# vertex = ['0','1','2','3','4','5']
INF = 99999999
def solve(graph, start):
    st = start
    visited = []
    
    i = 0
    flag = 'init'
    nodes = graph.nodes
    parent = {_:None for _ in nodes}
    step = []
    length = {_:INF for _ in nodes}
    # tmp = {_:'\(inf,_\)' for _ in nodes}
    # df =[]
    length[st] = 0
    while len(visited) < len(nodes) - 1:
        # print(st)
        
        visited.append(st)
        for v, value in dict(graph[st]).items():
            w = int(value['weight'])
            if v in visited:
                continue
            # if not parent[v]:
            #     parent[v] = st
            #     length[v] = length[st] + w
            # else:
            if length[st] + w < length[v]:
                length[v] = length[st] + w
                parent[v] = st
        # print(st,length)
        # print(set(nodes) - set(visited))
        x = None
        minimum= INF
        # tmp.update({_ : '_'for _ in visited})
        for v in set(nodes) - set(visited) :
            if minimum > length[v]:
                minimum = length[v]
                x = v
            # if length[v] != INF:
                # tmp[v] = f'\({length[v]},{parent[v]}\)'
        # df.append(tmp.copy())
        step.append((parent[x],x))
        st = x
    # table = pd.DataFrame(df, index = visited)
    
    return step, length
if __name__ == '__main__':
    tmp_matrix = {}
    tmp_matrix.update({'a':{'b':2, 'd':6}})
    tmp_matrix.update({'b' : {'a':2,'c':3, 'd':8, 'e':5}})
    tmp_matrix.update({'c' : {'b':3, 'e': 7}})
    tmp_matrix.update({'d' : {'a':6, 'b': 8, 'e':9}})
    tmp_matrix.update({'e' : {'b':5, 'c':7, 'd':9}})
    vertex = ['a','b','c','d','e']
    graph = nx.DiGraph()
    graph.add_nodes_from(vertex)
    for u, v_list in tmp_matrix.items():
        for v,w in v_list.items():
            graph.add_edge(u, v,weight =  w, color = 'b')
    print(solve(graph, 'a'))
# print(step)

        
        

        



