import numpy

from environment.order import Order
from utility.point import Point


class OrderGenerator:
    def __init__(self, osmnx_map):
        self.map = osmnx_map

    # Return a list of orders when time dt has elapsed
    # def advance(self, dt):
    #     return []

    def generate_order(self):
        order_start, order_end = self.map.next_destination()
        distance = self.map.path_length(order_start, order_end)
        return Order(Point(order_start, order_end), None, None, distance)

    def generate_time_until_order(self):
        return numpy.random.normal(loc=10, scale=2.0, size=None)