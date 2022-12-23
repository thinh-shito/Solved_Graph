import pandas as pd
import streamlit as st
import networkx as nx
INF = 9999999



def solve(graph,start):
	V = graph.nodes()
	result = []
	selected = {v : False for v in V}
	no_edge = 0
	selected[start] = True
	T = [start]
	# print for edge and weight
	while len(T) < len(V):

		minimum = INF
		x,y = None, None
		for u in T:
			# if selected[u]:
			print(u)
			for v, value in dict(graph[u]).items():
				if not selected[v]:  
					# not in selected and there is an edge
					w = int(value['weight'])
					if minimum > w:
						minimum = w
						x,y = u,v
						print(x,y)

		# print(str(x) + "-" + str(y) + ":" + str(w))
		result.append((x,y))
		selected[y] = True
		T.append(y)
		no_edge += 1

	return result

if __name__ == '__main__':
	#graph ={}
	# tmp_matrix.update({'a':{'b':2, 'd':6}})
	# tmp_matrix.update({'b' : {'a':2,'c':3, 'd':8, 'e':5}})
	# tmp_matrix.update({'c' : {'b':3, 'e': 7}})
	# tmp_matrix.update({'d' : {'a':6, 'b': 8, 'e':9}})
	# tmp_matrix.update({'e' : {'b':5, 'c':7, 'd':9}})
	# ################################
	# v = ['a','b','c','d','e']
	v = ['1','2','3','4','5','6']
	tmp_matrix = {'1': {'2': 6, '3': 1, '4': 5}, '2': {'1': 6, '3': 5, '5': 3}, '3': {'1': 1, '4': 5, '2': 5, '6': 4, '5': 6}, '4': {'1': 5, '3': 5, '6': 2}, '5': {'3': 6, '2': 3, '6': 6}, '6': {'4': 2, '3': 4, '5': 6}}
	sol = prim(v,tmp_matrix)
	print(sol.solve())

