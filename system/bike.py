from random import random

from system.courier import Courier, CourierState
from utility.argparser import args
from utility.constants import BIKE_BREAKDOWN_DURATION


def breaks_down():
    return random() < args.BREAKDOWN_RATE


class Bike(Courier):
    def __init__(self, position):
        super().__init__(position, 0)
        self.cost_hour = args.BIKE_HOUR_COST  # DKK
        self.avg_speed = args.BIKE_AVG_SPEED  # m/min # m/s
        self.orders = []
        self.order_distances = []
        self.order_limit = 3
        self.orders_delivered = 0
        self.shortest_route = None
        self.num_orders_taken = 0
        self.has_breakdown = False

    def move(self, delta_time_minutes, traffic_factor, weather_factor):

        if not self.is_standby():
            self.distance_to_destination -= delta_time_minutes * self.avg_speed * traffic_factor * weather_factor

            if self.has_arrived():
                # If there are more orders to deliver
                if self.state == CourierState.DeliveringOrder and self.orders:
                    # Prepare next order in route
                    self.order = self.orders.pop(0)
                    self.distance_to_destination = self.order_distances.pop(0)
                    self.orders_delivered += 1
                else:
                    if self.order_distances:
                        self.distance_to_destination = self.order_distances.pop(0)
                    self.orders_delivered = 0
                    self.orders = []
                    self.num_orders_taken = 0
                    self.update_arrival()

    def is_delivering(self):
        return self.order is not None

    def time_to_destination(self):
        return self.distance_to_destination / self.avg_speed

    def is_standby(self):
        return self.state == CourierState.Standby

    def update_arrival(self):
        if self.state == CourierState.DeliveringOrder:
            self.state = CourierState.ReturningToKitchen
            # self.distance_to_destination = self.order.distance
        elif self.state == CourierState.ReturningToKitchen:
            self.state = CourierState.Standby
            self.distance_to_destination = 0

    def take_order(self, order):
        self.order = order
        self.distance_to_destination = self.order.distance
        self.state = CourierState.DeliveringOrder
        return True

    def hold_order(self, order):
        self.orders.append(order)

    def can_carry_more_orders(self):
        return len(self.orders) < self.order_limit

    def take_orders(self, shortest_route, shortest_route_distances):
        self.num_orders_taken = len(self.orders)
        self.shortest_route = shortest_route
        orders_sorted = []
        for pos in shortest_route[1:-1]:
            orders_sorted.append([o for o in self.orders if o.destination_node == pos][0])
        self.orders = orders_sorted
        self.order = self.orders.pop(0)
        self.order_distances = shortest_route_distances
        self.distance_to_destination = self.order_distances.pop(0)
        self.state = CourierState.DeliveringOrder

        if breaks_down():
            print(f"Bike {self.id} breaks down along route, adding distance to simulate.")
            self.distance_to_destination += BIKE_BREAKDOWN_DURATION * self.avg_speed

    def holds_orders(self):
        return len(self.orders) > 0

    def start_delivery(self):
        self.state = CourierState.DeliveringOrder

    def has_arrived(self):
        return self.distance_to_destination <= 0

    def courier_type(self):
        return "Bike"

    def status(self):
        if self.is_standby():
            return f"{self.courier_type()} {self.id} standby at kitchen"

        if self.state == CourierState.DeliveringOrder:
            state_str = f"delivering order {self.order.id} ({self.orders_delivered + 1}/{self.num_orders_taken})"
        elif self.state == CourierState.ReturningToKitchen:
            state_str = "returning to kitchen"

        status_str = f"{self.courier_type()} {self.id} {state_str} with {self.distance_to_destination:.2f} m " \
                     f"/ {self.time_to_destination():.2f} min left"
        return status_str


