import numpy

from environment.order import Order
from simulator.config import KITCHEN_NODE_ID
from utility.point import Point


class OrderGenerator:
    def __init__(self, osmnx_map):
        self.map = osmnx_map
        numpy.random.seed(2223)

    # Return a list of orders when time dt has elapsed
    # def advance(self, dt):
    #     return []

    def generate_order(self, time_ordered):
        order_end = None
        distance = None
        # TODO: if no shortest path, make drone take that order
        while distance is None:
            order_end = self.map.next_destination()
            distance = self.map.path_length(KITCHEN_NODE_ID, order_end)

        order_end_node = self.map.get_node(order_end)
        return Order(Point(order_end_node['x'], order_end_node['y']), time_ordered, None, distance, order_end)

    def generate_time_until_order(self):
        return max(0, numpy.random.normal(loc=10, scale=2.0, size=None))
