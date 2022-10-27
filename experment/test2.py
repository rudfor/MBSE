import random
import osmnx as ox
import networkx as nx

G = ox.graph_from_place("Leiden, Netherlands", network_type="drive")
fig, ax = ox.plot_graph(G)