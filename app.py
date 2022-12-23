from hashlib import algorithms_available
from unittest import result
import streamlit as st
import pandas as pd
import numpy as np
import random
import re
import time
import graph_visual as gv
import networkx as nx
from algo import krusal, prim, hamilton,dijkstra

GRAPH_ALGO = {'graph travesal': ['dijikstra'],
			'min spanning tree': ['prim', 'krusal'],
			'circuit': ['euler', 'hamilton']
			}

GRAPH_STYLE = {'directed':nx.DiGraph(), 
			'undirected':nx.Graph(),
			}

def preprocess(vertex, edges, graph):
	vertex_list= re.split('\s',vertex.strip())
	graph.add_nodes_from(vertex_list)
	for edge in edges.strip().split('\n'):
		u,v,w = edge.split()
		graph.add_edge(u,v,weight = w, color = 'b')

# st.title('Graph')
# ---SIDEBAR-----
# sideber_title = st.sidebar.title('Setting')

style = st.sidebar.selectbox(label = 'Style', 
						options= GRAPH_STYLE.keys()
						)

graph = GRAPH_STYLE[style]
# Input vertexs and edges 
# st.sidebar.header('Input')
# LAYOUT = {'spring_layout': nx.spring_layout(graph), 
# 		'spectral_layout': nx.spectral_layout(graph),
# 		'shell_layout': nx.shell_layout(graph),
# 		'random_layout':nx.random_layout(graph),
# 		'circular_layout':nx.circular_layout(graph,),
# 		}

vertex_input = st.sidebar.text_input('Vertex')
st.sidebar.caption('''a b c''')


edge_input = st.sidebar.text_area('Edges',)
st.sidebar.caption('''a b 1
				\na c 2''')

#  show graph base
show_img = None
if edge_input:
	show_img = st.empty()
	preprocess(vertex_input,edge_input,graph)
	# G, edge_label, edge_color = gv.main(graph)
	gv.visual(graph)
	show_img.image('node.png')
reshow = st.sidebar.button('reshow',)

subject = st.sidebar.selectbox(label = 'subject',
							options = GRAPH_ALGO.keys()
						)
algo_selection = st.sidebar.selectbox(label = 'Algorithm',
						options= GRAPH_ALGO[subject]
						)
if algo_selection != 'krusal':
	start = st.sidebar.text_input('start')
solve = st.sidebar.button('SOLVE')

if solve:
	st.text('Solution')
	show_img = st.empty()
	result = None
	if algo_selection == 'hamilton':
		result = hamilton.solve(graph, start.strip())
		if not result:
			st.error('ko la hamilton')
	elif algo_selection == 'euler':
		if nx.is_eulerian(graph):
			result = list(nx.eulerian_circuit(graph, source=start.strip()))
		else:
			st.error('ko la euler')
	elif algo_selection == 'krusal':
		result = krusal.solve(graph)

	elif algo_selection == 'prim':
		result = prim.solve(graph, start.strip())
	else:
		result = dijkstra.solve(graph, start.strip())
		# print(result)
	if result:
		for u,v in result:
			# show_img.empty()
			graph[u][v].update({'color':'r'})
			gv.visual(graph)
			# st.image('node.png')
			show_img.image('node.png')
			time.sleep(1)

# st.sidebar.experimental_rerun()