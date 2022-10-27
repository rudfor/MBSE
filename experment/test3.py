import random
import osmnx as ox
import networkx as nx

G = ox.graph_from_place("Leiden, Netherlands", network_type="drive")
fig, ax = ox.plot_graph(G)

list_of_nodes = list(G.nodes())
start = random.choice(list_of_nodes)
end = random.choice(list_of_nodes)

ox.distance.add_edge_lengths(G, precision=10)
bike_dist = ox.distance.shortest_path(G, start, end, weight='length', cpus=1)
ox.plot.plot_graph_route(G, bike_dist, route_color='r', route_linewidth=4, route_alpha=0.5, orig_dest_size=100, ax=None)

route_length = int(sum(ox.utils_graph.get_route_edge_attributes(G, bike_dist, "length")))
print(route_length,"meters by bike")

