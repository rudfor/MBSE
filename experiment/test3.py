import random
import osmnx as ox
import networkx as nx


# G = ox.graph_from_place("Leiden, Netherlands", network_type="drive")
# # fig, ax = ox.plot_graph(G)
#
# list_of_nodes = list(G.nodes())
# start = random.choice(list_of_nodes)
# end = random.choice(list_of_nodes)
#
# ox.distance.add_edge_lengths(G, precision=10)
# bike_dist = ox.distance.shortest_path(G, start, end, weight='length', cpus=1)
# ox.plot.plot_graph_route(G, bike_dist, route_color='r', route_linewidth=4, route_alpha=0.5, orig_dest_size=100, ax=None)
#
# route_length = int(sum(ox.utils_graph.get_route_edge_attributes(G, bike_dist, "length")))
# print(route_length, "meters by bike")


class Map:
    def __init__(self):
        self.G = ox.graph_from_place("Leiden, Netherlands", network_type="drive")
        ox.distance.add_edge_lengths(self.G, precision=10)
        self.nodes = list(self.G.nodes())

    def plot_path(self, start, end):
        shortest_path = ox.distance.shortest_path(self.G, start, end, weight='length', cpus=1)
        ox.plot.plot_graph_route(self.G, shortest_path, route_color='r', route_linewidth=4, route_alpha=0.5,
                                 orig_dest_size=100,
                                 ax=None)

    def next_destination(self):
        start = random.choice(self.nodes)
        end = random.choice(self.nodes)

        return start, end

    def path_length(self, start, end):
        shortest_path = ox.distance.shortest_path(self.G, start, end, weight='length', cpus=1)
        path_length = int(sum(ox.utils_graph.get_route_edge_attributes(self.G, shortest_path, "length")))

        return path_length
