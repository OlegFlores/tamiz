import matplotlib.pyplot as plt
import networkx as nx
from networkx import DiGraph


def draw_graph(graph: DiGraph, file_name: str):
    padding = 25
    plt.figure(figsize=(10, 8), dpi=90, edgecolor='grey')
    pos = nx.nx_pydot.graphviz_layout(graph, prog='dot', root=0)

    # Add padding to the label positions
    # for node, (x, y) in pos.items():
    #     pos[node] = (x + padding, y + padding)

    nx.draw_networkx_nodes(graph, pos=pos, node_color='lightblue', edgecolors='grey')
    nx.draw_networkx_edges(graph, pos=pos, edge_color='grey')
    nx.draw_networkx_labels(graph, pos=pos, labels=nx.get_node_attributes(graph, 'mnemonic'), font_color='black')
    if len(pos.values()) != 0:
        x_values, y_values = zip(*pos.values())
        plt.xlim(min(x_values) - padding, max(x_values) + padding)
        plt.ylim(min(y_values) - padding, max(y_values) + padding)
        plt.axis('off')
        plt.savefig(file_name)
    plt.clf()
    plt.close()
