import random
import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt

from simulator.config import KITCHEN_NODE_ID
from system.bike import Bike
from system.courier import CourierState
from system.drone import Drone

class Map:
    def __init__(self):
        self.G = ox.graph_from_place("Leiden, Netherlands", network_type="drive")
        ox.distance.add_edge_lengths(self.G, precision=10)
        # Hack to make osmnx not crash
        self.G.add_edge(KITCHEN_NODE_ID, KITCHEN_NODE_ID, **{'length': 0})
        self.nodes = list(self.G.nodes())

    def plot_courier_paths(self, couriers):
        fig = None
        ax = None
        # Draw bike paths
        bike_paths = []
        bike_paths_colors = []
        for courier in couriers:
            if not isinstance(courier, Bike):
                continue

            if courier.is_standby():
                bike_paths_colors.append("y")
                bike_path = [KITCHEN_NODE_ID, KITCHEN_NODE_ID]
            else:
                bike_path = ox.distance.shortest_path(self.G, KITCHEN_NODE_ID, courier.order.destination_node,
                                                      weight='length', cpus=1)
                if courier.state == CourierState.ReturningToKitchen:
                    bike_paths_colors.append("r")
                elif courier.state == CourierState.DeliveringOrder:
                    bike_paths_colors.append("b")

            bike_paths.append(bike_path)

        if len(bike_paths) > 0:
            fig, ax = self.plot_bike_paths(bike_paths, bike_paths_colors)

        # Draw drone paths
        for courier in couriers:
            if not isinstance(courier, Drone):
                continue

            drone_path = None
            drone_path_color = None
            if courier.is_standby():
                drone_path_color = "y"
                drone_path = [KITCHEN_NODE_ID, KITCHEN_NODE_ID]
            else:
                drone_path = [KITCHEN_NODE_ID, courier.order.destination_node]
                if courier.state == CourierState.ReturningToKitchen:
                    drone_path_color = "r"
                elif courier.state == CourierState.DeliveringOrder:
                    drone_path_color = "b"

            if ax is None:
                # plot the graph but not the route, and override any user show/close
                # args for now: we'll do that later
                override = {"show", "save", "close"}
                kwargs = {}  # {k: v for k, v in pg_kwargs.items() if k not in override}
                fig, ax = ox.plot.plot_graph(self.G, show=False, save=False, close=False, **kwargs)
            else:
                fig = ax.figure

            route = drone_path
            route_color = drone_path_color

            # Same config as osmnx plotting
            orig_dest_size = 100
            route_alpha = 0.5
            route_linewidth = 4
            # scatterplot origin and destination points (first/last nodes in route)
            x = (self.G.nodes[route[0]]["x"], self.G.nodes[route[-1]]["x"])
            y = (self.G.nodes[route[0]]["y"], self.G.nodes[route[-1]]["y"])
            ax.scatter(x, y, s=orig_dest_size, c=route_color, alpha=route_alpha, edgecolor="none")
            ax.plot(x, y, c=route_color, lw=route_linewidth, alpha=route_alpha)

        ox.plot._save_and_show(fig, ax)

    def plot_bike_paths(self, paths, colors):
        if len(paths) > 1:
            fig, ax = ox.plot.plot_graph_routes(self.G, paths, route_colors=colors, route_linewidth=4, route_alpha=0.5,
                                                orig_dest_size=100, show=False, close=False)
        else:
            fig, ax = ox.plot.plot_graph_route(self.G, paths[0], route_color=colors[0], route_linewidth=4,
                                               route_alpha=0.5,
                                               orig_dest_size=100, show=False, close=False)

        return fig,ax

    def next_destination(self):
        return random.choice(self.nodes)

    def path_length(self, start, end):
        shortest_path = ox.distance.shortest_path(self.G, start, end, weight='length', cpus=1)
        if shortest_path is None:
            return None

        path_length = int(sum(ox.utils_graph.get_route_edge_attributes(self.G, shortest_path, "length")))

        return path_length

    def get_node(self, node_id):
        return self.G.nodes[node_id]
