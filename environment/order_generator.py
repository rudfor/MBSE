import random

import numpy

from environment.order import Order, OrderType
from simulator.config import KITCHEN_NODE_ID
from utility.point import Point
from utility.argparser import args

class OrderGenerator:
    def __init__(self, osmnx_map):
        self.map = osmnx_map
        if not args.RNDM:
            numpy.random.seed(args.SEED)

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
        p = Point(order_end_node['x'], order_end_node['y'])
        order_type = random.choice([OrderType.Coffee, OrderType.WarmMeal, OrderType.ColdMeal])
        return Order(p, time_ordered, None, distance, order_end, order_type)

    def generate_time_until_order(self, order_factor):
        return max(0, numpy.random.exponential(scale=args.BASE_ORDER_INTERARRIVAL_TIME * order_factor))
