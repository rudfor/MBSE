import random
import osmnx as ox
import networkx as nx


class OsmnxApi:
    def __init__(self, city_country='Leiden, Netherlands', network_type='drive'):
        """
        Sets Defaults and initializes
        """
        self.graph = ox.graph_from_place(city_country, network_type)
        self.list_of_nodes = list(self.graph.nodes())

    def graph(self):
        return self.graph

    def plot_graph(self):
        fig, ax = ox.plot_graph(self.graph)
        return fig, ax

    #    def list_of_nodes(self):
    #        return self.list_of_nodes

    def len_nodes(self):
        return len(self.list_of_nodes)

    def route(self, start_node=None, end_node=None, verbose=False):
        if start_node is None:
            start = random.choice(self.list_of_nodes)
        else:
            start = start_node
        if end_node is None:
            end = random.choice(self.list_of_nodes)
        else:
            end = end_node
        if verbose:
            print(f"{start} - {end}")

        ox.distance.add_edge_lengths(self.graph, precision=10)
        bike_dist = ox.distance.shortest_path(self.graph, start, end, weight='length', cpus=1)
        return start, end, bike_dist

    def route_length(self, bike_dist):
        route_length = int(sum(ox.utils_graph.get_route_edge_attributes(self.graph, bike_dist, "length")))
        return route_length

    def route_length_bike(self, bike_dist):
        route_length = int(sum(ox.utils_graph.get_route_edge_attributes(self.graph, bike_dist, "length")))
        return route_length

    def route_length_drone(self, start, end):
        start_latitude = self.graph.nodes[start]['x']
        start_longitude = self.graph.nodes[start]['y']

        end_latitude = self.graph.nodes[end]['x']
        end_longitude = self.graph.nodes[end]['y']

        drone_distance = ox.distance.great_circle_vec(start_latitude, start_longitude, end_latitude,
                                                      end_longitude, earth_radius=6371009)
        #route_length = int(sum(ox.utils_graph.get_route_edge_attributes(self.graph, bike_dist, "length")))
        return drone_distance

    def plot_route(self, bike_dist):
        ox.plot.plot_graph_route(self.graph, bike_dist, route_color='r', route_linewidth=4, route_alpha=0.5,
                                 orig_dest_size=100, ax=None)


if __name__ == "__main__":
    verbose: False
    print(f'debug run')
    network_type = 'drive'

    city_country = 'Amager, Denmark'
    graph = OsmnxApi(city_country, network_type)
    graph.route(verbose=True)

    print(f'debug run')
    city_countries = ['Lyngby, Denmark', 'Amager, Denmark', 'Leiden, Netherlands']
    for city_country in city_countries:
        graph.route(verbose=True)
        graph = OsmnxApi(city_country, network_type)

    city_country = 'Lyngby, Denmark'
    graph = OsmnxApi(city_country, network_type)
    for node in graph.list_of_nodes:
        print(f"{node}")
        print(node)
