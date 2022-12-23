


################################
# tmp_matrix ={'0':{'1':2.5,'2':2.0,'3':2.1},
#                 '1':{'0':2.5,'4':1.0},
#                 '2':{'0':2.0,'4':0.6,'5':1.5},
#                 '3':{'0':2.1,'5':2.5},
#                 '4':{'1':1.0,'2':0.6},
#                 '5':{'3':2.5,'2':1.5},
#                 }
# vertex = ['0','1','2','3','4','5']
def solve(vertex,matrix, start ):
    st = start
    visited = []
    i = 0
    flag = 'init'
    parent = {_:None for _ in vertex}
    step = []
    length = {_:99999 for _ in vertex}
    length[st] = 0
    while len(visited) < len(vertex) - 1:
        # print(st)
        visited.append(st)
        for v, w in matrix[st].items():
            if v in visited:
                continue
            if not parent[v]:
                parent[v] = st
                length[v] = length[st] + w
            else:
                if length[st] + w < length[v]:
                    length[v] = length[st] + w
                    parent[v] = st
        # print(st,length)
        # print(set(vertex) - set(visited))
        x = None
        minimum= 9999999
        for v in set(vertex) - set(visited) :
            if minimum > length[v]:
                minimum = w
                x = v
        step.append((parent[x],x))
        st = x
    return step
if __name__ == '__main__':
    tmp_matrix = {}
    tmp_matrix.update({'a':{'b':2, 'd':6}})
    tmp_matrix.update({'b' : {'a':2,'c':3, 'd':8, 'e':5}})
    tmp_matrix.update({'c' : {'b':3, 'e': 7}})
    tmp_matrix.update({'d' : {'a':6, 'b': 8, 'e':9}})
    tmp_matrix.update({'e' : {'b':5, 'c':7, 'd':9}})
    vertex = ['a','b','c','d','e']
    print(solve(vertex, tmp_matrix, 'a'))
# print(step)

        
        

        



