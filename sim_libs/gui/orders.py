from collections import defaultdict
import tkinter as tk
import random
from sim_libs.gui.customer import Customer as Customer
from sim_libs.gui.config import Config as Config
import time
import simpy



class OrdersLog:
    TEXT_HEIGHT = 20

    def __init__(self, canvas, x_top, y_top):
        self.canvas = canvas
        self.x_top = x_top
        self.y_top = y_top
        self.order_count = 0

    def next_order(self, minutes):
        x = self.x_top
        y = self.y_top + (self.order_count * self.TEXT_HEIGHT)
        self.canvas.create_text(x, y, anchor=tk.SW, text=f"Order in {round(minutes, 1)} m")
        # self.bus_count = self.bus_count + 1
        self.canvas.update()
        self.canvas.yview_moveto( y )

    def order_arrived(self, people):
        x = self.x_top + 135
        y = self.y_top + (self.order_count * self.TEXT_HEIGHT)
        self.canvas.create_text(x, y, anchor=tk.SW, text=f"Orders: {people}", fill="green")
        self.order_count += 1
        self.canvas.update()
        self.canvas.yview_moveto( y )


class Orders:

    @staticmethod
    def order_arrival(env, stat, config, order_log, sellers, scanners, seller_lines, scanner_lines):
        """
            Simulate a bus arriving every BUS_ARRIVAL_MEAN minutes with
            BUS_OCCUPANCY_MEAN people on board

            This is the top-level SimPy event for the simulation: all other events
            originate from a bus arriving
        """
        # Note that these unique IDs for busses and people are not required, but are included for eventual visualizations
        next_order_id = 0
        next_person_id = 0
        while True:
            # next_bus = random.expovariate(1 / BUS_ARRIVAL_MEAN)
            # on_board = int(random.gauss(BUS_OCCUPANCY_MEAN, BUS_OCCUPANCY_STD))
            next_order = config.ORDERS.pop()
            ordered = config.ORDER_SIZE.pop()

            # Wait for the bus
            order_log.next_order(next_order)
            yield env.timeout(next_order)
            order_log.order_arrived(ordered)

            # register_bus_arrival() below is for reporting purposes only
            people_ids = list(range(next_person_id, next_person_id + ordered))
            stat.register_bus_arrival(env.now, next_order_id, people_ids)
            next_person_id += ordered
            next_order_id += 1

            while len(people_ids) > 0:
                remaining = len(people_ids)
                group_size = min(round(random.gauss(config.PURCHASE_GROUP_SIZE_MEAN, config.PURCHASE_GROUP_SIZE_STD)), remaining)
                people_processed = people_ids[-group_size:] # Grab the last `group_size` elements
                people_ids = people_ids[:-group_size] # Reset people_ids to only those remaining

                # Randomly determine if this group is going to the sellers or straight to the scanners
                if random.random() > config.PURCHASE_RATIO_MEAN:
                    env.process(Customer.scanning_customer(env, stat, config, scanners, people_processed, scanner_lines,
                                                           config.TIME_TO_WALK_TO_SELLERS_MEAN + config.TIME_TO_WALK_TO_SCANNERS_MEAN,
                                                           config.TIME_TO_WALK_TO_SELLERS_STD + config.TIME_TO_WALK_TO_SCANNERS_STD))
                else:
                    env.process(Customer.purchasing_customer(env, stat, config, sellers, scanners, people_processed,
                                                             seller_lines, scanner_lines))
