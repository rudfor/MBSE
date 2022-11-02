import numpy

from environment.order import Order
from simulator.config import KITCHEN_NODE
from utility.point import Point


class OrderGenerator:
    def __init__(self, osmnx_map):
        self.map = osmnx_map

    # Return a list of orders when time dt has elapsed
    # def advance(self, dt):
    #     return []

    def generate_order(self, time_ordered):
        order_end = self.map.next_destination()
        distance = self.map.path_length(KITCHEN_NODE, order_end)
        return Order(Point(KITCHEN_NODE, order_end), time_ordered, None, distance)

    def generate_time_until_order(self):
        return numpy.random.normal(loc=10, scale=2.0, size=None)