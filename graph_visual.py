import networkx as nx
import matplotlib.pyplot as plt



def visual(v, e, style):
	
	if style == 'Undirected':
		G = nx.MultiGraph()
	else: 
		G = nx.MultiDiGraph()
		
	G.add_nodes_from(v)
	G.add_edges_from(e)
	nx.draw(G, with_labels = True, pos=nx.spring_layout(G))

	plt.savefig('node.png')
	return None

if __name__ == "__main__":
	V = ['a','b','c','d']
	E = [('a','b'),
		('a','c'),
		('d','a')
		]
	visual(V, E)
	plt.show()