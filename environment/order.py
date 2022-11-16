from enum import Enum


class Order:
    id_counter = 0

    def __init__(self, destination, time_ordered, weight, distance, destination_node, order_type):
        self.destination = destination
        self.time_ordered = time_ordered
        self.weight = weight
        self.distance = distance
        self.destination_node = destination_node
        self.id = Order.id_counter
        Order.id_counter += 1
        self.order_type = order_type

        match order_type:
            case OrderType.Coffee:
                self.delivery_time_threshold = 15
            case OrderType.WarmMeal:
                self.delivery_time_threshold = 30
            case OrderType.ColdMeal:
                self.delivery_time_threshold = 60

    def time_to_threshold(self, current_time):
        return self.time_ordered + self.delivery_time_threshold - current_time

    def __str__(self):
        return f"id {self.id}, {self.distance} m away, ordered at {self.time_ordered:.2f} min, " \
               f"threshold of {self.delivery_time_threshold} min"


class OrderType(Enum):
    Coffee = 1
    WarmMeal = 2
    ColdMeal = 3
