def get_a_tour(graph):#return possible circuit

    nodes_degree = {}       # Creating a {node: degree} dictionary for current graph.
    for edge in graph:
        a, b = edge[0], edge[1]
        nodes_degree[a] = nodes_degree.get(a, 0) + 1
        nodes_degree[b] = nodes_degree.get(b, 0) + 1

    tour =[]        # Finding a circuit in the current graph.
    loop = enumerate(nodes_degree)
    while True:
        try:
            l = loop.__next__()
            index = l[0]
            node = l[1]
            degree = nodes_degree[node]
            try:
                if (tour[-1], node) in graph or (node, tour[-1]) in graph:
                    tour.append(node)
                    try:
                        graph.remove((tour[-2], tour[-1]))
                        nodes_degree[tour[-1]] -= 1     # Updating degree of nodes in the graph, not required but for the sake of completeness.
                        nodes_degree[tour[-2]] -= 1     # Can also be used to check the correctness of program. In the end all degrees must zero.
                    except ValueError:
                        graph.remove((tour[-1], tour[-2]))
                        nodes_degree[tour[-1]] -= 1
                        nodes_degree[tour[-2]] -= 1
            except IndexError:
                tour.append(node)
        except StopIteration:
            loop = enumerate(nodes_degree)

        if len(tour) > 2:
            if tour[0] == tour[-1]:
                return tour

def get_eulerian_circuit(graph):
    tour = get_a_tour(graph)

    if graph:   # If stuck at the beginning, finding additional tour in the graph.
        loop = enumerate(tour[: -1])
        l = loop.__next__()
        i = l[0]
        node = l[1]
        try:
            while True:
                if node in list(zip(*graph))[0] or node in list(zip(*graph))[1]:
                    t = get_a_tour(graph)    # Retreivng the additional tour
                    j = t.index(node)
                    tour = tour[ : i] + t[j:-1] + t[ :j+1] + tour[i+1: ]        # Joining the two tours.
                    if not graph:       # Found Eulerian Tour
                        return tour     # Returning the Eulerian Tour
                    loop = enumerate(tour[: -1])        # Stuck -> Looping back to search for another tour.
                l = loop.__next__()
                i = l[0]
                node = l[1]
        except StopIteration:   # Seems like the vertices in the current tour cannot connect to rest of the edges in the graph.
            print("Your graph doesn't seem to be connected")
            return []
    else:       # Found the Eulerian Tour in the very first call
        return tour

def solve(graph, start):
    #demo
    graph = [(1, 2), (2, 3), (3, 1), (3, 4), (4, 3)]
    # creating a {node: degree} dictionary
    nodes_degree = {}
    for edge in graph:
        a, b = edge[0], edge[1]
        nodes_degree[a] = nodes_degree.get(a, 0) + 1
        nodes_degree[b] = nodes_degree.get(b, 0) + 1

    #checking degree
    degrees = nodes_degree.values() # remember it return a view
    for degree in degrees:
        if degree % 2:
            # print("Eulerian Circuit is impossible.")
            # exit()
            return []

    #finding Eulerian Tour
    tour = get_eulerian_circuit(graph)
    # print(tour)
    return tour
    
if __name__ =='__main__':
    # pass
    graph = [(1, 2), (1, 3), (2, 3), (2, 4), (2, 6), (3, 4), (3, 5), (4, 5), (4, 6)]
    # graph = [(1, 2), (1, 3), (2, 3)]
    # graph = [(1, 2), (1, 3), (2, 3), (2, 4), (2, 6), (3, 4), (3, 5), (4, 5), (4, 6), (9, 10), (10, 11), (11, 9)]
    # graph = [(1, 2), (1, 3), (2, 3), (2, 4), (2, 6), (3, 4), (3, 5), (4, 5), (4, 6), (2, 7), (7, 8), (8, 2)]
    # graph = [(1, 2), (1, 3), (2, 3), (2, 4), (2, 6), (3, 4), (3, 5), (4, 5), (4, 6), (1, 5), (5, 6), (1, 6)]
    # graph = [(1, 2), (2, 3), (3, 1), (3, 4), (4, 3)]
    # graph = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
    # graph = [(2, 6), (4, 2), (5, 4), (6, 5), (6, 8), (7, 9), (8, 7), (9, 6)]
    #graph = [(1, 2), (3, 1), (2, 3), (3, 4), (4, 3)]
    print(solve(graph,None))