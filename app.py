from tkinter import font
import streamlit as st
import pandas as pd
import numpy as np
import re
import graph_visual as gs

def preprocess(vertex, edges):
	vertex_list= re.split('\s',vertex)
	edge_list = [tuple(re.split('\s',edge)) for edge in edges.split('.')]
	return vertex_list, edge_list

st.title('Graph')
# ---SIDEBAR-----
sideber_title = st.sidebar.title('Setting')

graph_style_option = st.sidebar.selectbox(label = 'Style', 
								options= [
										'Directed', 
										'Undirected'
										],
								)
st.sidebar.header('Input')
vertexs_input = st.sidebar.text_input('Vertex',)
st.sidebar.caption('''a b c''')
edges_input = st.sidebar.text_input('Edges',)
st.sidebar.caption('''a b.c a''')
solve = st.sidebar.button('SOLVE')
if solve:
	vertex_list, edge_list = preprocess(vertexs_input,edges_input)
	gs.visual(vertex_list, edge_list, graph_style_option)
	st.image('node.png')
