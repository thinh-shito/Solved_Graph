import itertools
def solve(graph, st):
    nodes = graph.nodes
    # result = []
    perm = itertools.permutations(nodes)
    # print(perm)
    listPerm = []
    for item in perm:
        permutation = list(item)
        firstNode = permutation[0]
        permutation = permutation + list(firstNode)
        listPerm.append(permutation)

    flag = False
    for listRes in listPerm:
        lenVector = len(listRes)

        hamilton = True

        for x in range(0, lenVector-1):

            nodeInitial = listRes[x]
            nodeFinal = listRes[x+1]
            if nodeFinal not in graph.adj[nodeInitial]:
                hamilton = False
        if hamilton:
            if listRes[0] == st:
                # print("Hamilton Circuit:", listRes)
                return list(zip(listRes[:-1], listRes[1:]))
            flag = True
    
    return None

if __name__ == '__main__':
    #     start = time.time()
    """g = { "1" : ["2", "5", "6"],
         "2" : ["1", "3", "8"],
         "3" : ["2", "4", "10"],
         "4" : ["3", "5", "12"],
         "5" : ["1", "4", "14"],
         "6" : ["1", "7", "15"],
         "7" : ["6", "8", "17"],
         "8" : ["2", "7", "9"],
         "9" : ["8", "10", "18"],
         "10" : ["3", "9", "11"],
         "11" : ["10", "12", "19"],
         "12" : ["11", "13", "4"],
         "13" : ["12", "14", "20"],
         "14" : ["13", "15", "5"],
         "15" : ["14", "6", "16"],
         "16" : ["15", "17", "20"],
         "17" : ["7", "16", "18"],
         "18" : ["17", "19", "9"],
         "19" : ["18", "20", "11"],
         "20" : ["13", "16", "19"]

       } """

    """g = { "1" : ["2", "4"],
          "2" : ["1", "3"],
          "3" : ["4", "5"],
          "5" : ["3", "4"],
          "4" : ["3"]
          
        }    
     """
    g = {"1": ["2", "3", "4"],
         "2": ["1", "5"],
         "3": ["1", "4", "5"],
         "4": ["1", "3", "6"],
         "5": ["2", "3", "6"],
         "6": ["4", "5"]
         }
    print(solve(g.keys(),g,'1'))