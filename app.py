from hashlib import algorithms_available
from unittest import result
import streamlit as st
import pandas as pd
import numpy as np
import random
import cv2
import re
import time
import graph_visual as gv
import networkx as nx
from algo import krusal, prim, hamilton,dijkstra, euler

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
# Init graph
graph = GRAPH_STYLE[style]

# Input vertexs and edges 
vertex_input = st.sidebar.text_input('Vertex')
st.sidebar.caption('''a b c''')


edge_input = st.sidebar.text_area('Edges',)
st.sidebar.caption('''a b 1
				\na c 2''')

#  show graph base
show_img = st.empty()
if edge_input:
	
	preprocess(vertex_input,edge_input,graph)
	# G, edge_label, edge_color = gv.main(graph)
	gv.visual(graph)
	show_img.image('node.png')
# reshow = st.sidebar.button('reshow',)

subject = st.sidebar.selectbox(label = 'subject',
							options = GRAPH_ALGO.keys()
						)
algo_selection = st.sidebar.selectbox(label = 'Algorithm',
						options= GRAPH_ALGO[subject]
						)
if algo_selection != 'krusal':
	if vertex_input:
		start = st.sidebar.text_input('start',value = random.choice(list(graph.nodes)),)
solve = st.sidebar.button('SOLVE')

try:
	if solve:
		
		length = None
		# df = ''''''
		st.text('Minh hoạ lời giải')
		show_img = st.empty()
		result = None
		if algo_selection == 'hamilton':
			result = hamilton.solve(graph, start.strip())
			if not result:
				st.error('Không có chu trình Hamilton')
		elif algo_selection == 'euler':
			if nx.is_eulerian(graph):
				# result = euler.solve(graph.edges, start.strip())
				result = nx.eulerian_circuit(graph,source =start.strip())
			else:
				st.error('Không có chu trình Euler')
		elif algo_selection == 'krusal':
			result = krusal.solve(graph)

		elif algo_selection == 'prim':
			result = prim.solve(graph, start.strip())
		else:
			result, length= dijkstra.solve(graph, start.strip())
			# for end, l in length.items():
			# 		st.text(f"Đường đi từ {start.strip()} đến {end}: {l}")
			# print(result)
		col1, col2 = st.columns(2)
		
		if result:
			# cache = {}
			# pos = 1
			
			for u,v in result:
				# show_img.empty()
				graph[u][v].update({'color':'r'})
				gv.visual(graph)
				show_img.image('node.png')
				# cache[pos]=(u,v)
				# cache[pos] = cv2.imread('node.png')
				# show_img.image(cache[pos],channels="BGR")
				# pos += 1
				
				time.sleep(1)

			# string = st.text_area('Enter text', height=275,)
			if length:
				for end, l in length.items():
					# st.success(f"Đường đi từ {start.strip()} đến {end}: {l}",
					# 		)
					if not end == start.strip():
						new_title = f'<p style="font-family:Roboto; color:Green; font-size: 24px;">\
									Đường đi từ {start.strip()} đến {end}: {l}\
									</p>'
						st.markdown(new_title, unsafe_allow_html=True)
		
except:
	st.error('!!Không thể giải!!')
			
		st.success('Hoàn thành!')


	# e = RuntimeError('Không thể giải')
	# st.exception(e)
	# st.sidebar.experimental_rerun()