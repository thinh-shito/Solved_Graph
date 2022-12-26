from turtle import color
import networkx as nx
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np

HIGHLIGHT = 'red'
HIDE = ''
ARC_RAD = 0.25
def my_draw_networkx_edge_labels(
    G,
    pos,
    edge_labels=None,
    label_pos=0.5,
    font_size=10,
    font_color="k",
    font_family="sans-serif",
    font_weight="normal",
    alpha=None,
    bbox=None,
    horizontalalignment="center",
    verticalalignment="center",
    ax=None,
    rotate=True,
    clip_on=True,
    rad=0
):

    

    if ax is None:
        ax = plt.gca()
    if edge_labels is None:
        labels = {(u, v): d for u, v, d in G.edges(data=True)}
    else:
        labels = edge_labels
    text_items = {}
    for (n1, n2), label in labels.items():
        (x1, y1) = pos[n1]
        (x2, y2) = pos[n2]
        (x, y) = (
            x1 * label_pos + x2 * (1.0 - label_pos),
            y1 * label_pos + y2 * (1.0 - label_pos),
        )
        pos_1 = ax.transData.transform(np.array(pos[n1]))
        pos_2 = ax.transData.transform(np.array(pos[n2]))
        linear_mid = 0.5*pos_1 + 0.5*pos_2
        d_pos = pos_2 - pos_1
        rotation_matrix = np.array([(0,1), (-1,0)])
        ctrl_1 = linear_mid + rad*rotation_matrix@d_pos
        ctrl_mid_1 = 0.5*pos_1 + 0.5*ctrl_1
        ctrl_mid_2 = 0.5*pos_2 + 0.5*ctrl_1
        bezier_mid = 0.5*ctrl_mid_1 + 0.5*ctrl_mid_2
        (x, y) = ax.transData.inverted().transform(bezier_mid)

        if rotate:
            # in degrees
            angle = np.arctan2(y2 - y1, x2 - x1) / (2.0 * np.pi) * 360
            # make label orientation "right-side-up"
            if angle > 90:
                angle -= 180
            if angle < -90:
                angle += 180
            # transform data coordinate angle to screen coordinate angle
            xy = np.array((x, y))
            trans_angle = ax.transData.transform_angles(
                np.array((angle,)), xy.reshape((1, 2))
            )[0]
        else:
            trans_angle = 0.0
        # use default box of white with white border
        if bbox is None:
            bbox = dict(boxstyle="round", ec=(1.0, 1.0, 1.0), fc=(1.0, 1.0, 1.0))
        if not isinstance(label, str):
            label = str(label)  # this makes "1" and 1 labeled the same

        t = ax.text(
            x,
            y,
            label,
            size=font_size,
            color=font_color,
            family=font_family,
            weight=font_weight,
            alpha=alpha,
            horizontalalignment=horizontalalignment,
            verticalalignment=verticalalignment,
            rotation=trans_angle,
            transform=ax.transData,
            bbox=bbox,
            zorder=1,
            clip_on=clip_on,
        )
        text_items[(n1, n2)] = t

    ax.tick_params(
        axis="both",
        which="both",
        bottom=False,
        left=False,
        labelbottom=False,
        labelleft=False,
    )

    return text_items
def draw_edge(G,pos,edge_list,color = 'tab:blue'):

	nx.draw_networkx_edges(G, pos,edgelist = edge_list, 
						width=3, alpha=0.5, edge_color= color,
					)
def draw_curved_edge(G,pos,edge_list,color = 'tab:blue'):

	nx.draw_networkx_edges(G, pos,edgelist = edge_list, 
						width=3, alpha=0.5, edge_color= color,
						connectionstyle=f'arc3, rad = {ARC_RAD}'
					)
def visual(graph):
	
	# pos = nx.nx_agraph.graphviz_layout(graph)
	pos = nx.circular_layout(graph,)  # positions for all nodes - seed for reproducibility
	# nodes
	nx.draw_networkx_nodes(graph, pos, node_size=700,)
	# node labels
	nx.draw_networkx_labels(graph, pos, font_size=14, font_family="sans-serif",)
	# edges

	edge_curved_highlight = []
	edge_straight_highlight = []


	edge_curved_black = []
	edge_straight_black = []
	edge_labels = {}
	curved_edges = []
	straight_edges = []
	if graph.is_directed():
		curved_edges = [edge for edge in graph.edges() if reversed(edge) in graph.edges()]
		straight_edges = list(set (graph.edges()) - set(curved_edges))
	else:
		straight_edges = graph.edges()

	for u, v in graph.edges:
		# print(u)
		edge_labels[(u,v)] = graph[u][v]['weight']
		if graph[u][v]['color'] == 'r':
			if (u,v) in curved_edges : 
				edge_curved_highlight.append((u,v))
			elif (u,v) in straight_edges:
				edge_straight_highlight.append((u,v))
		else:
			if (u,v) in curved_edges : 
				edge_curved_black.append((u,v))
			elif (u,v) in straight_edges:
				edge_straight_black.append((u,v))

	curved_edge_labels = {edge: edge_labels[edge] for edge in curved_edges}
	straight_edge_labels = {edge: edge_labels[edge] for edge in straight_edges}

	if edge_curved_highlight:
		draw_curved_edge(graph,pos,edge_curved_highlight, HIGHLIGHT)
	if edge_curved_black:
		draw_curved_edge(graph,pos,edge_curved_black)
	if edge_straight_highlight:
		draw_edge(graph,pos,edge_straight_highlight, HIGHLIGHT)
	if edge_straight_black:
		draw_edge(graph,pos,edge_straight_black)


	my_draw_networkx_edge_labels(graph, pos, 
							edge_labels=curved_edge_labels,
							rotate=False,rad = ARC_RAD)
	nx.draw_networkx_edge_labels(graph, pos,
							edge_labels=straight_edge_labels,
							rotate=False)
	
	ax = plt.gca()
	ax.margins(0.08)
	plt.axis("off")
	plt.tight_layout()
	plt.savefig('node.png')
	return None

def main(graph):
	# pair,edge_color, G = convert(v, e, style)
	pass

if __name__ == "__main__":
	V = ['a','b','c','d']
	E = {'a': {'b':1,'d':2, 'c': 2},
		'c':{'d':2,}
		}
	graph = nx.Graph()
	graph.add_nodes_from(V)
	for u, v_list in E.items():
		for v,w in v_list.items():
			graph.add_edge(u, v,weight =  w, color = 'b')
	
	print(graph.edges)